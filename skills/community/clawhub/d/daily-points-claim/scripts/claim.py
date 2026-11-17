#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日积分自动领取 - 通用执行器（零第三方依赖，仅用标准库）。

用法:
    python claim.py                     # 跑全部启用的站点
    python claim.py --site a,b          # 只跑指定站点
    python claim.py --dry-run           # 只打印将要发送的请求，不发送
    python claim.py --json              # 输出结构化 JSON 摘要（供自动化读取）
    python claim.py --check             # 只校验配置，不发请求
    python claim.py --set-cookie a "x=1; y=2"   # 快速更新某站点的 Cookie

退出码: 0 全部成功或今日已领 / 1 存在失败或未知 / 2 配置错误
"""

import argparse
import gzip
import json
import random
import re
import shutil
import ssl
import sys
import time
import uuid
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib import error, parse, request

BASE_DIR = Path(__file__).resolve().parent
SKILL_DIR = BASE_DIR.parent
DEFAULT_CONFIG = BASE_DIR / "config.json"
LOG_DIR = SKILL_DIR / "logs"
TZ = timezone(timedelta(hours=8))

TPL = re.compile(r"\{\{\s*([A-Za-z0-9_]+(?:\|[a-z]+)?)\s*\}\}")

SUCCESS, ALREADY, FAILED, UNKNOWN, ERROR = "success", "already", "failed", "unknown", "error"


# ---------------------------------------------------------------- 工具函数

def build_context():
    """构建模板变量上下文。所有时间按北京时间取值，避免跨零点领错日期。"""
    n = datetime.now(TZ)
    y = n - timedelta(days=1)
    return {
        "today": n.strftime("%Y-%m-%d"),
        "today_compact": n.strftime("%Y%m%d"),
        "yesterday": y.strftime("%Y-%m-%d"),
        "yesterday_compact": y.strftime("%Y%m%d"),
        "iso": n.isoformat(timespec="seconds"),
        "year": n.strftime("%Y"),
        "month": n.strftime("%m"),
        "day": n.strftime("%d"),
        "timestamp": int(n.timestamp()),
        "timestamp_ms": int(n.timestamp() * 1000),
        "uuid": uuid.uuid4().hex,
        "random": random.randint(100000, 999999),
    }


def render(value, ctx):
    """递归替换 {{var}} / {{var|int}} / {{var|float}} 模板变量。"""
    if isinstance(value, dict):
        return {k: render(v, ctx) for k, v in value.items()}
    if isinstance(value, list):
        return [render(v, ctx) for v in value]
    if not isinstance(value, str):
        return value

    m = TPL.fullmatch(value.strip())
    if m:
        raw = m.group(1)
        key, _, conv = raw.partition("|")
        if key not in ctx:
            return value
        val = ctx[key]
        if conv == "int":
            try:
                return int(val)
            except (TypeError, ValueError):
                return val
        if conv == "float":
            try:
                return float(val)
            except (TypeError, ValueError):
                return val
        return val

    def _sub(mo):
        key = mo.group(1).partition("|")[0]
        return str(ctx.get(key, mo.group(0)))

    return TPL.sub(_sub, value)


def decompress(raw, content_encoding):
    enc = (content_encoding or "").lower()
    try:
        if "gzip" in enc:
            return gzip.decompress(raw)
        if "deflate" in enc:
            try:
                return zlib.decompress(raw)
            except zlib.error:
                return zlib.decompress(raw, -zlib.MAX_WBITS)
    except Exception:
        pass
    return raw


def decode(raw):
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def get_path(payload, path):
    """按 a.b.0.c 形式取值，payload 为 dict/list/str。path 为空时返回整体文本。"""
    if not path:
        if isinstance(payload, str):
            return payload
        return json.dumps(payload, ensure_ascii=False)
    cur = payload
    for part in str(path).split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        else:
            return None
    return cur


def _to_num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def match_one(rule, payload, text):
    path = rule.get("path", "")
    op = (rule.get("op") or "eq").lower()
    expected = rule.get("value")

    actual = get_path(payload, path)
    if actual is None and isinstance(payload, dict):
        # 允许在 JSON 顶层找不到时回退到原始文本匹配
        actual_text = text
    else:
        actual_text = actual if isinstance(actual, str) else json.dumps(actual, ensure_ascii=False)

    if op == "exists":
        return actual is not None
    if op == "not_exists":
        return actual is None
    if op == "eq":
        if actual == expected:
            return True
        return str(actual) == str(expected)
    if op == "ne":
        return not (actual == expected or str(actual) == str(expected))
    if op == "contains":
        return str(expected) in (actual_text or "")
    if op == "not_contains":
        return str(expected) not in (actual_text or "")
    if op == "regex":
        try:
            return re.search(str(expected), actual_text or "") is not None
        except re.error:
            return False
    if op in ("gt", "gte", "lt", "lte"):
        a, b = _to_num(actual), _to_num(expected)
        if a is None or b is None:
            return False
        return {"gt": a > b, "gte": a >= b, "lt": a < b, "lte": a <= b}[op]
    return False


def match_rules(rules, payload, text):
    """规则数组为「与」关系；空数组视为不匹配。"""
    if not rules:
        return False
    return all(match_one(r, payload, text) for r in rules)


# ---------------------------------------------------------------- 网络请求

def build_request_spec(site, ctx):
    cfg = site.get("request") or {}
    if not cfg.get("url"):
        raise ValueError("request.url 不能为空")

    method = (cfg.get("method") or "GET").upper()
    url = render(cfg["url"], ctx)
    headers = {k: str(v) for k, v in render(cfg.get("headers") or {}, ctx).items()}

    body_type = (cfg.get("body_type") or "json").lower()
    body = None
    raw_body = cfg.get("body")

    if method in ("GET", "HEAD", "DELETE") and not raw_body:
        pass
    elif body_type == "json":
        data = render(raw_body if raw_body is not None else {}, ctx)
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if not any(k.lower() == "content-type" for k in headers):
            headers["Content-Type"] = "application/json; charset=utf-8"
    elif body_type == "form":
        data = render(raw_body if raw_body is not None else {}, ctx)
        body = parse.urlencode(data).encode("utf-8")
        if not any(k.lower() == "content-type" for k in headers):
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
    elif body_type == "raw":
        text = render(raw_body if isinstance(raw_body, str) else "", ctx)
        body = str(text).encode("utf-8")
    elif body_type == "none":
        body = None
    else:
        raise ValueError(f"不支持的 body_type: {body_type}")

    return {"method": method, "url": url, "headers": headers, "body": body, "body_type": body_type}


def build_opener(insecure, proxy):
    """显式控制代理。

    默认直连：避免系统 http_proxy（如 Clash）劫持请求，导致本地地址或
    国内站点返回异常。proxy 取值：
      ""      直连（默认）
      "system" 沿用系统/环境变量代理
      "http://127.0.0.1:7890" 指定代理地址
    """
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    handlers = [request.HTTPSHandler(context=ctx)]
    if proxy and proxy.lower() != "system":
        handlers.append(request.ProxyHandler({"http": proxy, "https": proxy}))
    elif not proxy:
        handlers.append(request.ProxyHandler({}))
    return request.build_opener(*handlers)


def send(spec, timeout, insecure, proxy=""):
    opener = build_opener(insecure, proxy)

    req = request.Request(spec["url"], data=spec["body"], headers=spec["headers"], method=spec["method"])
    try:
        with opener.open(req, timeout=timeout) as resp:
            raw = decompress(resp.read(), resp.headers.get("Content-Encoding"))
            return {
                "status": resp.status,
                "text": decode(raw),
                "final_url": resp.geturl(),
                "http_error": False,
            }
    except error.HTTPError as e:
        raw = decompress(e.read(), e.headers.get("Content-Encoding") if e.headers else None)
        return {
            "status": e.code,
            "text": decode(raw),
            "final_url": getattr(e, "url", spec["url"]),
            "http_error": True,
        }


# ---------------------------------------------------------------- 单站点执行

def preview(spec):
    lines = [f"{spec['method']} {spec['url']}"]
    sensitive = ("cookie", "authorization", "token")
    for k, v in spec["headers"].items():
        if k.lower() in sensitive:
            shown = v if len(v) <= 24 else v[:18] + "..." + v[-6:]
            lines.append(f"  {k}: {shown}")
        else:
            lines.append(f"  {k}: {v}")
    if spec["body"]:
        text = decode(spec["body"])
        lines.append(f"  body({spec['body_type']}): {text[:300]}")
    return "\n".join(lines)


def run_site(site, settings, ctx, dry_run):
    sid = site.get("id") or site.get("name") or "unnamed"
    name = site.get("name") or sid
    result = {"id": sid, "name": name, "status": UNKNOWN, "points": None, "message": "", "http_status": None}

    try:
        spec = build_request_spec(site, ctx)
    except Exception as e:
        result.update(status=ERROR, message=f"请求配置错误: {e}")
        return result, None

    if dry_run:
        result.update(status="dry_run", message="仅预览，未发送")
        return result, spec

    timeout = int(settings.get("timeout", 15))
    retries = int(settings.get("retries", 2))
    delay = float(settings.get("retry_delay", 3))
    insecure = bool(settings.get("insecure_skip_verify", False))
    proxy = str(settings.get("proxy", "") or "")

    attempt, resp = 0, None
    while attempt <= retries:
        attempt += 1
        try:
            resp = send(spec, timeout, insecure, proxy)
            # 仅对 5xx / 429 重试，4xx 业务错误直接判定
            if resp["http_error"] and (resp["status"] >= 500 or resp["status"] == 429) and attempt <= retries:
                time.sleep(delay)
                continue
            break
        except Exception as e:
            if attempt <= retries:
                time.sleep(delay)
                continue
            result.update(status=ERROR, message=f"网络异常: {type(e).__name__}: {e}")
            return result, spec

    if resp is None:
        result.update(status=ERROR, message="未获得响应")
        return result, spec

    result["http_status"] = resp["status"]
    text = resp["text"]
    try:
        payload = json.loads(text)
    except (ValueError, TypeError):
        payload = text

    expect = site.get("expect") or {}
    if match_rules(expect.get("already_when"), payload, text):
        result.update(status=ALREADY, message="今日已领取")
    elif match_rules(expect.get("success_when"), payload, text):
        result.update(status=SUCCESS, message="领取成功")
    elif match_rules(expect.get("fail_when"), payload, text):
        result.update(status=FAILED, message="站点返回失败")
    elif resp["http_error"]:
        result.update(status=FAILED, message=f"HTTP {resp['status']}")
    else:
        result.update(status=UNKNOWN, message="未命中任何判定规则，需人工确认")

    if expect.get("points_path"):
        pts = get_path(payload, expect["points_path"])
        if pts is not None:
            result["points"] = pts

    if expect.get("message_path"):
        msg = get_path(payload, expect["message_path"])
        if msg is not None:
            result["message"] = str(msg)

    if result["status"] in (UNKNOWN, FAILED):
        snippet = re.sub(r"\s+", " ", text)[:220]
        result["response_snippet"] = snippet

    return result, spec


# ---------------------------------------------------------------- 日志与输出

def write_log(results, verbose_line):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(TZ)
    jsonl = LOG_DIR / "runs.jsonl"
    with jsonl.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"time": now.isoformat(timespec="seconds"), "results": results}, ensure_ascii=False) + "\n")

    text_log = LOG_DIR / f"{now.strftime('%Y-%m')}.log"
    with text_log.open("a", encoding="utf-8") as f:
        f.write(verbose_line + "\n")


LABEL = {SUCCESS: "[成功]", ALREADY: "[已领]", FAILED: "[失败]", UNKNOWN: "[待确认]", ERROR: "[异常]", "dry_run": "[预览]"}


def emit(results, as_json, quiet=False):
    if as_json:
        summary = {
            "time": datetime.now(TZ).isoformat(timespec="seconds"),
            "total": len(results),
            "success": sum(1 for r in results if r["status"] == SUCCESS),
            "already": sum(1 for r in results if r["status"] == ALREADY),
            "failed": sum(1 for r in results if r["status"] in (FAILED, ERROR)),
            "unknown": sum(1 for r in results if r["status"] == UNKNOWN),
            "results": results,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return summary

    if quiet:
        return None

    print("=" * 56)
    print(f"每日积分领取  {datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)
    for r in results:
        label = LABEL.get(r["status"], r["status"])
        pts = f"  +{r['points']}" if r.get("points") not in (None, "") else ""
        print(f"{label} {r['name']}{pts}  {r['message']}")
        if r.get("response_snippet"):
            print(f"        响应片段: {r['response_snippet']}")
    print("-" * 56)
    print(
        f"共 {len(results)} 项 | 成功 {sum(1 for r in results if r['status'] == SUCCESS)}"
        f" | 已领 {sum(1 for r in results if r['status'] == ALREADY)}"
        f" | 失败 {sum(1 for r in results if r['status'] in (FAILED, ERROR))}"
        f" | 待确认 {sum(1 for r in results if r['status'] == UNKNOWN)}"
    )
    return None


# ---------------------------------------------------------------- 配置

def load_config(path):
    if not path.exists():
        raise FileNotFoundError(f"找不到配置文件: {path}")
    with path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg.get("sites"), list):
        raise ValueError("配置缺少 sites 数组")
    return cfg


def save_config(path, cfg):
    with path.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def check_config(cfg):
    problems = []
    seen = set()
    for i, site in enumerate(cfg.get("sites") or []):
        tag = site.get("id") or f"sites[{i}]"
        if not site.get("id"):
            problems.append(f"{tag}: 缺少 id")
        if site.get("id") in seen:
            problems.append(f"{tag}: id 重复")
        seen.add(site.get("id"))
        if not (site.get("request") or {}).get("url"):
            problems.append(f"{tag}: 缺少 request.url")
        expect = site.get("expect") or {}
        if not expect.get("success_when") and not expect.get("already_when"):
            problems.append(f"{tag}: 至少需要 success_when 或 already_when，否则无法判断结果")
    return problems


def main():
    ap = argparse.ArgumentParser(description="每日积分自动领取执行器")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG), help="配置文件路径")
    ap.add_argument("--site", help="只跑指定站点 id，逗号分隔")
    ap.add_argument("--dry-run", action="store_true", help="只打印请求，不实际发送")
    ap.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    ap.add_argument("--check", action="store_true", help="只校验配置")
    ap.add_argument("--quiet", action="store_true", help="静默模式，只留退出码")
    ap.add_argument("--set-cookie", nargs=2, metavar=("SITE_ID", "COOKIE"), help="更新指定站点的 Cookie 头")
    args = ap.parse_args()

    cfg_path = Path(args.config).expanduser()
    if not cfg_path.exists():
        example = cfg_path.parent / "config.example.json"
        if example.exists():
            shutil.copyfile(example, cfg_path)
            print(f"未找到 {cfg_path.name}，已从 config.example.json 生成。")
            print(f"请先编辑 {cfg_path}，把 Cookie 换成自己的登录态后再运行。")
            return 2
        print(f"找不到配置文件: {cfg_path}", file=sys.stderr)
        return 2

    try:
        cfg = load_config(cfg_path)
    except Exception as e:
        print(f"配置读取失败: {e}", file=sys.stderr)
        return 2

    if args.set_cookie:
        sid, cookie = args.set_cookie
        hit = False
        for site in cfg["sites"]:
            if site.get("id") == sid:
                headers = site.setdefault("request", {}).setdefault("headers", {})
                for key in list(headers):
                    if key.lower() == "cookie":
                        del headers[key]
                headers["Cookie"] = cookie
                hit = True
                break
        if not hit:
            print(f"未找到站点 id: {sid}", file=sys.stderr)
            return 2
        save_config(cfg_path, cfg)
        print(f"已更新 {sid} 的 Cookie")
        return 0

    problems = check_config(cfg)
    if problems:
        print("配置存在问题:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        if args.check:
            return 2

    if args.check:
        enabled = [s for s in cfg["sites"] if s.get("enabled", True)]
        print(f"配置校验通过。站点总数 {len(cfg['sites'])}，启用 {len(enabled)}。")
        for s in cfg["sites"]:
            state = "启用" if s.get("enabled", True) else "停用"
            print(f"  - {s.get('id')} ({s.get('name')}): {state}")
        return 0 if not problems else 2

    sites = [s for s in cfg["sites"] if s.get("enabled", True)]
    if args.site:
        wanted = {x.strip() for x in args.site.split(",") if x.strip()}
        sites = [s for s in sites if s.get("id") in wanted]
        missing = wanted - {s.get("id") for s in sites}
        if missing:
            print(f"这些站点不存在或已停用: {', '.join(sorted(missing))}", file=sys.stderr)

    if not sites:
        print("没有可执行的站点。请先在 config.json 中配置并启用至少一个站点。", file=sys.stderr)
        return 2

    settings = cfg.get("settings") or {}
    ctx = build_context()
    results = []
    log_lines = []

    for site in sites:
        result, spec = run_site(site, settings, ctx, args.dry_run)
        results.append(result)
        label = LABEL.get(result["status"], result["status"])
        log_lines.append(f"[{datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')}] {label} {result['name']} - {result['message']}")
        if args.dry_run and spec:
            print(preview(spec))
            print()

    if not args.dry_run:
        write_log(results, "\n".join(log_lines))

    emit(results, args.json, args.quiet)

    if any(r["status"] in (FAILED, ERROR, UNKNOWN) for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
