#!/usr/bin/env python3
"""ARI CLI for the amazon-voc Skill.

Uses only Python's standard library. Paid collection and AI analysis commands
require an explicit --confirm flag after a free preview/quote.
"""

import argparse
import getpass
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


# VERSION 必须与 _meta.json 的 version 一致：它进 User-Agent，服务端据此统计版本分布
# 并判定最低支持版本。发版时两处一起改。
VERSION = "1.0.9"
# CHANNEL 标记分发渠道（不同市场 listing），由打包脚本按变体烙入；官方母版为空串。
# 非空时 User-Agent 追加 " ch/<渠道>"，服务端据此统计各渠道的注册与用量。
CHANNEL = "amazon-voc"
PROD_BASE = "https://ari.funewa.com"
TIMEOUT_SEC = 120
# SSE 分析在 meta 事件之后、LLM 首 token 之前可能长时间静默（推理模型可达数分钟）。
# urlopen 的 timeout 是「单次 read 拿不到数据」的上限，若沿用 120s，会在服务端已经
# 扣点并归档之后把一次成功的分析误报成网络错误，进而诱导重试 → 二次扣点。
SSE_TIMEOUT_SEC = 600
SITES = ("amz_us", "amz_uk", "amz_de", "amz_jp", "amz_ca", "amz_fr", "amz_es", "amz_it")
ANALYSIS_TYPES = ("voc", "insight", "trend", "variant", "compare")
SSE_TYPES = ("voc", "insight", "compare")  # 走 text/event-stream 的分析类型
# 轮询时值得重试的错误：瞬时故障不应中止一次已经冻结积点的采集等待。
RETRYABLE_CODES = ("NETWORK_ERROR", "HTTP_ERROR", "ARI_RATE_LIMITED",
                   "ARI_INTERNAL_ERROR", "ARI_UPSTREAM_ERROR")
_exit_code = 0
# 服务端在每个 API Key 响应上广播最新版本，任意一条命令都能顺带发现有新版，
# 不必等用户想起来跑 check。
_release = {"latest": "", "url": ""}

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def base_url():
    return (os.environ.get("ARI_BASE_URL") or PROD_BASE).strip().rstrip("/")


def user_agent():
    """版本号后随渠道尾巴（若有）。服务端按第一个空格截断取版本。"""
    ua = "ARI-Review-Skill/" + VERSION
    return ua + " ch/" + CHANNEL if CHANNEL else ua


def links():
    root = (os.environ.get("ARI_WEB_URL") or PROD_BASE).strip().rstrip("/")
    return {
        "apiKeys": root + "/zh/account?ui=d47626f#api-keys",
        "billing": root + "/zh/billing",
        "products": root + "/zh/products",
        "reports": root + "/zh/reports",
    }


def report_url(rid):
    """单份报告的网页深链（图表版 / 导出入口）。from=skill 供网页侧归因。"""
    try:
        rid = int(rid)
    except (TypeError, ValueError):
        return None
    if rid <= 0:
        return None
    root = (os.environ.get("ARI_WEB_URL") or PROD_BASE).strip().rstrip("/")
    return "%s/zh/reports/%d?from=skill" % (root, rid)


def attach_report_urls(out):
    """给 /api/v1/reports 信封的每行补 reportUrl。原样返回 out 便于串联。"""
    data = data_of(out)
    if ok(out) and isinstance(data, dict):
        for r in data.get("reports") or []:
            if isinstance(r, dict) and r.get("id"):
                r["reportUrl"] = report_url(r["id"])
    return out


def config_path():
    return os.path.expanduser("~/.ari/config.json")


def resolve_key():
    """Key 只从 ARI_API_KEY 或用户配置目录读取。

    刻意不回退到 Skill 包目录：那个位置会随 Skill 一起被打包、复制或提交，
    与「Key 只保存在本机用户配置中」的承诺相悖。
    """
    key = os.environ.get("ARI_API_KEY", "").strip()
    if key:
        return key
    path = config_path()
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                key = (json.load(fh).get("api_key") or "").strip()
            if key:
                return key
        except (OSError, json.JSONDecodeError):
            pass
    return None


def require_key():
    key = resolve_key()
    if key:
        return key
    emit(error_obj(
        "ARI_API_KEY_MISSING", 0,
        "未找到 ARI API Key",
        "推荐运行 python ari.py setup 浏览器一键授权；也可 configure 手动粘贴或设置 ARI_API_KEY。",
    ))
    raise SystemExit(2)


def error_obj(code, status, message, hint="", query=None, partial=None):
    out = {
        "success": False,
        "error": {"code": code, "status": status, "message": message, "hint": hint},
        "links": links(),
    }
    if query is not None:
        out["_query"] = query
    if partial:
        out["partial"] = partial
    return out


def version_tuple(v):
    out = []
    for part in str(v or "").split("."):
        try:
            out.append(int(part.strip()))
        except ValueError:
            out.append(0)
    return tuple(out)


def version_cmp(a, b):
    """比较点分版本号，返回 -1/0/1。与服务端 compareVersions 同语义。

    段数不同时短的补 0：裸用元组比较会把 1.0 判成早于 1.0.0（前缀更短即更小），
    从而对已是最新版的用户反复弹升级提示。
    """
    at, bt = version_tuple(a), version_tuple(b)
    n = max(len(at), len(bt))
    at += (0,) * (n - len(at))
    bt += (0,) * (n - len(bt))
    return (at > bt) - (at < bt)


def note_release(headers):
    """记录服务端广播的最新版本（响应头），供 update_info 生成升级提示。"""
    try:
        latest = (headers.get("X-ARI-Skill-Latest") or "").strip()
        url = (headers.get("X-ARI-Skill-Update-Url") or "").strip()
    except Exception:
        return
    if latest:
        _release["latest"] = latest
    if url:
        _release["url"] = url


def update_info():
    """本地版本低于服务端最新版时返回升级提示，否则 None。

    只在「确实更旧」时提示：本地版本更新（开发中）不该反复告警。
    """
    latest = _release.get("latest") or ""
    if not latest or version_cmp(VERSION, latest) >= 0:
        return None
    return {
        "current": VERSION, "latest": latest,
        "url": _release.get("url") or links()["apiKeys"],
        "message": "有新版 Skill（%s → %s）。请通过原安装渠道更新后再使用；"
                   "本 CLI 不会自行下载或执行任何远端代码。" % (VERSION, latest),
    }


def emit(obj, compact=False):
    global _exit_code
    if isinstance(obj, dict) and obj.get("success") is False:
        _exit_code = 1
    if isinstance(obj, dict):
        upd = update_info()
        if upd:
            obj["update"] = upd
    print(json.dumps(
        obj, ensure_ascii=False,
        separators=((",", ":") if compact else (", ", ": ")),
        indent=(None if compact else 2),
    ))


def err_code(out):
    if not isinstance(out, dict):
        return ""
    err = out.get("error")
    if isinstance(err, dict) and err.get("code"):
        return str(err["code"])
    return str(out.get("code") or "")


def err_message(out):
    if not isinstance(out, dict):
        return ""
    err = out.get("error")
    if isinstance(err, dict) and err.get("message"):
        return str(err["message"])
    return str(out.get("message") or "")


def parse_http_error(exc, query):
    note_release(exc.headers)  # 426（版本过旧）等错误响应同样带广播头
    try:
        detail = json.loads(exc.read().decode("utf-8", errors="replace"))
    except Exception:
        detail = {}
    if isinstance(detail, dict) and detail:
        detail["_httpStatus"] = exc.code
        detail["_query"] = query
        detail["links"] = links()
        return detail
    return error_obj("HTTP_ERROR", exc.code, "HTTP %d" % exc.code, query=query)


def as_collecting(out, http_status):
    """把「采集中、暂无足够数据」的 202 转成显式错误码。

    服务端在这种情况下返回 202 + success:true，但信封里既没有报告也没有内容；
    照原样交给上层会被当成一次成功的分析。该分支未扣点，重试是免费的。
    """
    if http_status != 202 or not isinstance(out, dict):
        return None
    data = out.get("data")
    if not isinstance(data, dict) or data.get("status") != "COLLECTING":
        return None
    wait = data.get("retryAfterSeconds") or 30
    return error_obj(
        "ARI_COLLECTING", 202, "该 ASIN 正在采集中，暂无足够数据可分析",
        "本次未扣点。等待约 %s 秒后重试即可（该分支重试免费）。" % wait)


def request_json(method, path, payload=None, params=None):
    query = {
        "method": method,
        "path": path,
        "params": {k: v for k, v in (params or {}).items() if v not in (None, "")},
        "payload": payload,
    }
    url = base_url() + path
    if query["params"]:
        url += "?" + urllib.parse.urlencode(query["params"], doseq=True)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + require_key(),
        "Accept": "application/json",
        "User-Agent": user_agent(),
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            raw = resp.read().decode("utf-8")
            out = json.loads(raw) if raw else {"success": True, "data": None}
            if isinstance(out, dict):
                alt = as_collecting(out, resp.status)
                if alt is not None:
                    alt["_query"] = query
                    return alt
                out["_query"] = query
            return out
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI_BASE_URL", query)


def request_sse(path, payload):
    query = {"method": "POST", "path": path, "params": {}, "payload": payload}
    url = base_url() + path
    headers = {
        "Authorization": "Bearer " + require_key(),
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "User-Agent": user_agent(),
    }
    result = {"meta": None, "content": "", "result": None, "reportId": 0, "creditsUsed": 0}
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=SSE_TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            content_type = resp.headers.get("Content-Type", "")
            if "text/event-stream" not in content_type:
                # 就绪检查等前置校验在开流之前返回普通 JSON。
                raw = resp.read().decode("utf-8")
                out = json.loads(raw) if raw else {"success": True, "data": None}
                alt = as_collecting(out, resp.status)
                if alt is not None:
                    alt["_query"] = query
                    return alt
                out["_query"] = query
                return out

            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data: "):
                    continue
                raw = line[6:].strip()
                if not raw:
                    continue
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                kind = event.get("type")
                if kind == "meta":
                    result["meta"] = {k: v for k, v in event.items() if k != "type"}
                elif kind == "content":
                    result["content"] += event.get("content") or ""
                elif kind == "result":
                    result["result"] = event.get("data")
                    result["reportId"] = event.get("reportId") or 0
                elif kind == "done":
                    result["creditsUsed"] = event.get("creditsUsed") or 0
                elif kind == "error":
                    return error_obj(
                        event.get("code") or "ARI_ANALYSIS_ERROR", 200,
                        event.get("message") or "analysis failed",
                        "已生成的部分内容保留在 partial 中", query, result)
            if result.get("reportId"):
                result["reportUrl"] = report_url(result["reportId"])
            return {"success": True, "data": result, "_query": query, "links": links()}
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        # 流中断（socket 超时 / 连接断开）时服务端往往已经跑完、扣点并归档。
        # 这里绝不能提示「重试」——重跑 --confirm 会为同一份报告扣第二次点。
        return error_obj(
            "ARI_STREAM_INTERRUPTED", 0, "分析流中断：%s" % exc,
            "本次分析可能已扣点并已归档。请先运行 reports --asin <ASIN> --limit 1 "
            "确认是否已生成新报告；确认没有生成后才可重试，不要直接重跑 --confirm。",
            query, result)


def fetch_release():
    """读取公开的版本发布信息（免认证，Key 缺失或失效时也能拿到升级入口）。

    失败一律静默返回 None——查不到新版说明不该影响任何正常命令。
    """
    try:
        req = urllib.request.Request(
            base_url() + "/api/v1/public/config",
            headers={"Accept": "application/json",
                     "User-Agent": user_agent()})
        with urllib.request.urlopen(req, timeout=15) as resp:
            note_release(resp.headers)
            body = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    rel = ((body or {}).get("data") or {}).get("skillRelease")
    if not isinstance(rel, dict):
        return None
    if rel.get("latest"):
        _release["latest"] = str(rel["latest"])
    if rel.get("url"):
        _release["url"] = str(rel["url"])
    return rel


def data_of(out):
    return out.get("data") if isinstance(out, dict) else None


def ok(out):
    return isinstance(out, dict) and out.get("success") is True


def response_failures(node, prefix=""):
    """在 deepdive/charts 这类聚合结果里找出失败的子请求。

    只在「还没看到 success 字段」的层级继续下钻，避免把业务数据误判成响应信封。
    """
    fails = []
    for key, val in node.items():
        if key.startswith("_") or not isinstance(val, dict):
            continue
        name = prefix + key
        if "success" in val:
            if val.get("success") is False:
                fails.append({"part": name, "code": err_code(val),
                              "message": err_message(val)})
        else:
            fails.extend(response_failures(val, name + "."))
    return fails


def emit_bundle(bundle, compact):
    """聚合结果里任一子请求失败，外层就必须是 success:false。

    否则 agent 只看最外层信封就会把「图表 403 / 分析 402」当成完整数据，
    在缺数据的情况下继续写报告。
    """
    fails = response_failures(bundle)
    out = {"success": not fails, "data": bundle, "links": links()}
    if fails:
        out["failedParts"] = fails
        out["error"] = {
            "code": "ARI_PARTIAL_FAILURE", "status": 0,
            "message": "%d 个子请求失败：%s" % (
                len(fails), ", ".join(f["part"] for f in fails)),
            "hint": "只能使用 data 中成功返回的部分；缺失的数据不得推断或补造。",
        }
    emit(out, compact)


def save_key(key):
    """写本机用户配置（0600 直接创建，避免「默认权限 → chmod」之间的可读窗口）。"""
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump({"api_key": key}, fh)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def cmd_configure(args):
    key = getpass.getpass("ARI API Key (ari_live_*): ").strip()
    if not key.startswith("ari_live_"):
        emit(error_obj("ARI_API_KEY_INVALID_FORMAT", 0, "Key 必须以 ari_live_ 开头"), args.compact)
        raise SystemExit(2)
    path = save_key(key)
    emit({"success": True, "data": {
        "configured": True, "path": path,
        "note": "Windows 上 POSIX 权限位不生效，请自行确保该路径不被共享或同步到云端。",
    }}, args.compact)


def request_public(method, path, payload=None, timeout=15):
    """免认证请求（设备码授权等公开端点），错误统一转 error_obj。"""
    query = {"method": method, "path": path, "params": {}, "payload": payload}
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json",
               "User-Agent": user_agent()}
    if data is not None:
        headers["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(base_url() + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            note_release(resp.headers)
            out = json.loads(resp.read().decode("utf-8"))
            if isinstance(out, dict):
                out["_query"] = query
            return out
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI_BASE_URL", query)


def cmd_setup(args):
    """设备码授权：浏览器点一下，Key 自动落到本机，全程无复制粘贴。

    进度提示走 stderr（用户/代理立即可见），stdout 仍只输出最终 JSON。
    刻意不在 CLI 里做注册：注册留在网页（人机验证与邮箱验证防线不动）。
    """
    start = request_public("POST", "/api/v1/auth/device/start", {})
    if not ok(start):
        emit(start, args.compact)
        return
    data = start.get("data") or {}
    code = str(data.get("code") or "")
    verify_url = str(data.get("verifyUrl") or "")
    token = str(data.get("pollToken") or "")
    interval = max(1, int(data.get("interval") or 3))
    expires = int(data.get("expiresIn") or 600)
    if not (code and verify_url and token):
        emit(error_obj("ARI_DEVICE_START_MALFORMED", 0, "服务端响应缺少必要字段"), args.compact)
        return

    print("请在浏览器打开以下链接完成授权（设备码 %s，%d 分钟内有效）：" % (code, expires // 60),
          file=sys.stderr)
    print("  " + verify_url, file=sys.stderr)
    print("未注册会先引导注册（需完成邮箱验证）；授权后本命令自动完成。", file=sys.stderr)

    deadline = time.time() + expires
    while time.time() < deadline:
        time.sleep(interval)
        poll = request_public("POST", "/api/v1/auth/device/poll", {"pollToken": token})
        if not ok(poll):
            if err_code(poll) == "ARI_NOT_FOUND":
                emit(poll, args.compact)
                return
            continue  # 网络抖动/限流：下轮再试
        status = str((poll.get("data") or {}).get("status") or "")
        if status == "APPROVED":
            key = str((poll.get("data") or {}).get("apiKey") or "")
            if not key.startswith("ari_live_"):
                emit(error_obj("ARI_DEVICE_KEY_MALFORMED", 0, "服务端未返回有效 Key"), args.compact)
                return
            path = save_key(key)
            emit({"success": True, "data": {
                "configured": True, "path": path,
                "keyPrefix": key[:len("ari_live_") + 8],
                "note": "API Key 已保存到本机用户配置，其余命令可直接使用。",
            }}, args.compact)
            return
        if status == "CLAIMED":
            emit(error_obj(
                "ARI_DEVICE_ALREADY_CLAIMED", 0, "该会话的 Key 已被领取",
                "若非你本人操作，请到用户中心撤销该 Key 后重新运行 setup。"), args.compact)
            return
        if status == "EXPIRED":
            break
    emit(error_obj(
        "ARI_DEVICE_EXPIRED", 0, "授权未在有效期内完成",
        "重新运行 python ari.py setup 并尽快在浏览器完成授权。"), args.compact)


def cmd_check(args):
    # 先取公开发布信息：Key 无效时也能顺带告诉用户「你的版本旧了、去哪儿更新」。
    release = fetch_release()
    me = request_json("GET", "/api/v1/user/me")
    if not ok(me):
        emit(me, args.compact)
        return
    balance = request_json("GET", "/api/v1/credits/balance")
    if not ok(balance):
        emit(balance, args.compact)
        return
    emit({"success": True, "data": {
        "skillVersion": VERSION,
        "release": release,
        "user": data_of(me),
        "balance": data_of(balance),
    }, "links": links()}, args.compact)


def cmd_products(args):
    emit(request_json("GET", "/api/v1/asins"), args.compact)


def usable_balance(site):
    """返回该站点实际可用于采集的积点。

    赠送的 plan 桶只能在 amz_us 消费，非美站采集仅可使用付费（addon）积点——
    只报「总余额」会让用户在余额看似充足的情况下确认后吃 402。
    返回 (info, err)：err 非 None 时应直接把它 emit 出去。
    """
    bal = request_json("GET", "/api/v1/credits/balance")
    if not ok(bal):
        return None, bal
    d = data_of(bal) or {}
    plan = int((d.get("planCredits") or {}).get("available") or 0)
    addon = int((d.get("addonCredits") or {}).get("available") or 0)
    if site == "amz_us":
        return {"usable": plan + addon, "planCredits": plan, "addonCredits": addon,
                "note": ""}, None
    return {"usable": addon, "planCredits": plan, "addonCredits": addon,
            "note": "非美国站采集仅可使用付费积点（addon），赠送的 plan 积点不可用。"}, None


def wait_task(task_id, interval, timeout):
    """轮询到任务终态。jobs 表的状态集合是 queued/running/done/failed。

    单次瞬时错误不中止等待：此时采集积点已冻结、任务仍在后台跑，
    直接返回会让调用方误以为采集已经结束。
    """
    deadline = time.time() + timeout
    last = None
    transient = 0
    while time.time() < deadline:
        last = request_json("GET", "/api/v1/collection/status/" + urllib.parse.quote(task_id))
        if ok(last):
            transient = 0
            status = str((data_of(last) or {}).get("status") or "").lower()
            if status in ("done", "failed"):
                return last
        elif err_code(last) in RETRYABLE_CODES:
            transient += 1
            if transient >= 3:
                last["hint"] = ("连续 %d 次查询失败；采集任务仍可能在后台运行，"
                                "稍后用 status --task %s 查询。" % (transient, task_id))
                return last
        else:
            return last
        time.sleep(interval)
    return error_obj("WAIT_TIMEOUT", 0, "等待采集超时，任务仍可能在后台运行",
                     "稍后使用 status --task %s 查询" % task_id,
                     partial=data_of(last) if last else None)


def cmd_collect(args):
    pricing = request_json("GET", "/api/v1/billing/pricing")
    if not ok(pricing):
        emit(pricing, args.compact)
        return
    price = int((data_of(pricing) or {}).get("collectPerPage") or 5)
    estimate = args.pages * price
    bal, berr = usable_balance(args.site)
    if berr is not None:
        emit(berr, args.compact)
        return
    payload = {
        "asin": args.asin.upper(), "site": args.site, "pageCount": args.pages,
        "filterByStar": args.star, "sortBy": args.sort, "alias": args.alias,
    }
    if not args.confirm:
        emit({
            "success": True,
            "data": {
                "confirmationRequired": True,
                "estimatedCredits": estimate,
                "estimatedReviews": args.pages * int((data_of(pricing) or {}).get("reviewsPerPage") or 10),
                "usableBalance": bal["usable"],
                "planCredits": bal["planCredits"],
                "addonCredits": bal["addonCredits"],
                "sufficient": bal["usable"] >= estimate,
                "siteNote": bal["note"],
                "message": "确认后用同一命令追加 --confirm；需要等待完成再追加 --wait。",
                "request": payload,
            },
            "links": links(),
        }, args.compact)
        return
    if bal["usable"] < estimate:
        emit(error_obj(
            "ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
            "本次需要 %d 点，%s 站可用 %d 点。%s请充值后重试。"
            % (estimate, args.site, bal["usable"], bal["note"] and bal["note"] + " ")),
            args.compact)
        return
    out = request_json("POST", "/api/v1/collection/submit", payload)
    if args.wait and ok(out):
        task_id = (data_of(out) or {}).get("taskId")
        if task_id:
            submitted = data_of(out)
            final = wait_task(task_id, args.interval, args.timeout)
            if ok(final):
                out = {"success": True, "data": {"submitted": submitted,
                                                 "final": data_of(final)},
                       "links": links()}
            else:
                final["submitted"] = submitted
                out = final
    emit(out, args.compact)


def cmd_status(args):
    emit(request_json("GET", "/api/v1/collection/status/" + urllib.parse.quote(args.task)), args.compact)


def cmd_reviews(args):
    params = {"asin": args.asin.upper(), "site": args.site, "star": args.star,
              "q": args.query, "page": args.page}
    emit(request_json("GET", "/api/v1/reviews", params=params), args.compact)


def chart_bundle(asin, site, days):
    params = {"asin": asin.upper(), "site": site, "days": days}
    return {
        name: request_json("GET", "/api/v1/charts/" + name, params=params)
        for name in ("stars", "trend", "keywords", "flow")
    }


def window_note(days):
    return {"days": days,
            "note": "days=0 表示全部历史；非 0 时图表只统计最近 N 天，"
                    "解读趋势/占比必须带上这个窗口。"}


def cmd_charts(args):
    bundle = chart_bundle(args.asin, args.site, args.days)
    bundle["_window"] = window_note(args.days)
    emit_bundle(bundle, args.compact)


def quote_payload(kind, asin, site, competitor, competitor_site):
    return {
        "type": kind, "asin": (asin or "").upper(), "site": site,
        "competitorAsin": (competitor or "").upper(),
        "competitorSite": competitor_site or site,
    }


def missing_competitor(kind, competitor):
    if kind != "compare" or (competitor or "").strip():
        return None
    return error_obj("ARI_VALIDATION_ERROR", 0, "compare 需要 --competitor <竞品ASIN>",
                     "示例：analyze --type compare --asin <目标ASIN> --competitor <竞品ASIN>")


def backfill_report_id(out, asin):
    """补上 VOC / compare 的 reportId。

    只有 insight 会发 result 事件；VOC 和 compare 的流只有 meta/content/done，
    不带 reportId。分析确实完成（收到 done、creditsUsed 非 0）时回查一次报告列表
    取最新一条，供 report --id 复读。
    """
    data = data_of(out)
    if not ok(out) or not isinstance(data, dict):
        return out
    if data.get("reportId") or not data.get("creditsUsed"):
        return out
    listed = request_json("GET", "/api/v1/reports",
                          params={"asin": (asin or "").upper(), "limit": 1})
    if ok(listed):
        items = (data_of(listed) or {}).get("reports") or []
        if items and items[0].get("id"):
            data["reportId"] = items[0]["id"]
            data["reportIdSource"] = "reports-lookup"
            data["reportUrl"] = report_url(items[0]["id"])
    return out


def run_analysis(kind, asin, site, competitor, competitor_site, language, confirm):
    bad = missing_competitor(kind, competitor)
    if bad is not None:
        return bad
    q_payload = quote_payload(kind, asin, site, competitor, competitor_site)
    quote = request_json("POST", "/api/v1/analysis/quote", q_payload)
    if not ok(quote):
        return quote
    q_data = data_of(quote) or {}
    if not confirm:
        return {"success": True, "data": {"confirmationRequired": True, "quote": q_data,
                                             "message": "用户确认后追加 --confirm 才会生成并扣点。"},
                "links": links()}
    if not q_data.get("sufficient", False):
        return error_obj("ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
                         "需要 %s 点，当前余额 %s；请充值后重试。" %
                         (q_data.get("price"), q_data.get("balance")))

    payload = {"asin": (asin or "").upper(), "site": site, "outputLanguage": language}
    if kind == "compare":
        payload.update({"competitorAsin": (competitor or "").upper(),
                        "competitorSite": competitor_site or site})
    path = "/api/v1/analysis/" + kind
    if kind in SSE_TYPES:
        return backfill_report_id(request_sse(path, payload), asin)
    return request_json("POST", path, payload)


def cmd_quote(args):
    bad = missing_competitor(args.type, args.competitor)
    if bad is not None:
        emit(bad, args.compact)
        return
    emit(request_json("POST", "/api/v1/analysis/quote",
                      quote_payload(args.type, args.asin, args.site,
                                    args.competitor, args.competitor_site)), args.compact)


def cmd_analyze(args):
    emit(run_analysis(args.type, args.asin, args.site, args.competitor,
                      args.competitor_site, args.language, args.confirm), args.compact)


def cmd_reports(args):
    params = {"asin": args.asin, "type": args.type, "starred": "1" if args.starred else "",
              "q": args.query, "limit": args.limit}
    emit(attach_report_urls(request_json("GET", "/api/v1/reports", params=params)), args.compact)


def cmd_report(args):
    out = request_json("GET", "/api/v1/reports/%d" % args.id)
    data = data_of(out)
    if ok(out) and isinstance(data, dict) and data.get("id"):
        data["reportUrl"] = report_url(data["id"])
    emit(out, args.compact)


def cmd_deepdive(args):
    products = request_json("GET", "/api/v1/asins")
    if not ok(products):
        emit(products, args.compact)
        return
    items = (data_of(products) or {}).get("asins") or []
    asin = args.asin.upper()
    target = next((x for x in items if str(x.get("asin", "")).upper() == asin
                   and x.get("site") == args.site), None)
    # asins 列表只含主品（竞品订阅被过滤掉），但 charts/reviews 对竞品同样放行。
    # 因此这里不直接拒绝——否则会把用户引去重复 collect，白扣一次采集费，
    # 还可能撞上套餐的 ASIN 订阅上限。缺主品元数据时把 AI 分析降级为只报价。
    confirm = args.confirm and target is not None
    bundle = {
        "_window": window_note(args.days),
        "product": target,
        "charts": chart_bundle(asin, args.site, args.days),
        "reviews": request_json("GET", "/api/v1/reviews",
                                params={"asin": asin, "site": args.site, "page": 1}),
        "reports": attach_report_urls(request_json(
            "GET", "/api/v1/reports", params={"asin": asin, "limit": args.report_limit})),
        "analysis": run_analysis("voc", asin, args.site, None, None,
                                 args.language, confirm),
    }
    if target is None:
        note = ("%s / %s 不在主品订阅列表中。若它是作为竞品添加的，"
                "charts / reviews / analyze 仍然可用；若从未采集过，"
                "请先运行 collect --asin %s --site %s 取报价。" % (asin, args.site, asin, args.site))
        if args.confirm:
            note += " 因缺少主品订阅，本次 AI 分析已降级为只报价，未扣点。"
        bundle["productNote"] = note
    emit_bundle(bundle, args.compact)


def add_analysis_args(parser, include_type=True):
    if include_type:
        parser.add_argument("--type", required=True, choices=ANALYSIS_TYPES)
    parser.add_argument("--asin", required=True)
    parser.add_argument("--site", default="amz_us", choices=SITES)
    parser.add_argument("--competitor")
    parser.add_argument("--competitor-site", choices=SITES)
    parser.add_argument("--language", default="zh")


def main():
    # --compact 用 parents 挂到每个子命令上，这样放在子命令前后都能识别。
    # default=SUPPRESS 是必须的：否则子解析器会用自己的默认值覆盖掉
    # 已经在顶层解析出来的 --compact。缺省值只能在 parse_args 之后补，
    # 不能用 set_defaults——parents 共享同一个 action 对象，
    # set_defaults 会把 SUPPRESS 改掉，反而把覆盖问题带回来。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--compact", action="store_true",
                        default=argparse.SUPPRESS, help="输出单行 JSON")

    ap = argparse.ArgumentParser(prog="ari.py", parents=[common],
                                 description="ARI Amazon 评论采集与智能分析 CLI")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", parents=[common],
                       help="浏览器一键授权，自动获取并保存 API Key（推荐首次使用）")
    p.set_defaults(fn=cmd_setup)

    p = sub.add_parser("configure", parents=[common], help="隐藏输入并保存 ARI API Key")
    p.set_defaults(fn=cmd_configure)

    p = sub.add_parser("check", parents=[common], help="验证 Key、账户和积点余额")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("products", parents=[common], help="列出当前账户订阅的 ASIN")
    p.set_defaults(fn=cmd_products)

    p = sub.add_parser("collect", parents=[common], help="采集报价或提交采集任务")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--pages", type=int, default=3, choices=range(1, 11), metavar="1..10")
    p.add_argument("--star", default="all_stars",
                   choices=("all_stars", "critical", "positive", "one_star", "two_star",
                            "three_star", "four_star", "five_star"))
    p.add_argument("--sort", default="recent", choices=("recent", "helpful"))
    p.add_argument("--alias", default="")
    p.add_argument("--confirm", action="store_true", help="确认扣点并提交")
    p.add_argument("--wait", action="store_true", help="提交后等待任务完成")
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--timeout", type=int, default=600)
    p.set_defaults(fn=cmd_collect)

    p = sub.add_parser("status", parents=[common], help="查询采集任务状态")
    p.add_argument("--task", required=True)
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("reviews", parents=[common], help="读取已采集评论")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--star", type=int, choices=range(1, 6))
    p.add_argument("--query")
    p.add_argument("--page", type=int, default=1)
    p.set_defaults(fn=cmd_reviews)

    p = sub.add_parser("charts", parents=[common],
                       help="读取免费星级、趋势、关键词和流向数据")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--days", type=int, default=0, help="0=全部历史")
    p.set_defaults(fn=cmd_charts)

    p = sub.add_parser("quote", parents=[common], help="查询 AI 分析报价（不扣点）")
    add_analysis_args(p)
    p.set_defaults(fn=cmd_quote)

    p = sub.add_parser("analyze", parents=[common], help="AI 分析报价或确认生成")
    add_analysis_args(p)
    p.add_argument("--confirm", action="store_true", help="确认按报价扣点并生成")
    p.set_defaults(fn=cmd_analyze)

    p = sub.add_parser("deepdive", parents=[common],
                       help="产品、图表、评论、报告与 VOC 报价/分析")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--days", type=int, default=0, help="0=全部历史，与 charts 保持一致")
    p.add_argument("--report-limit", type=int, default=10)
    p.add_argument("--language", default="zh")
    p.add_argument("--confirm", action="store_true", help="确认 VOC 报价并生成")
    p.set_defaults(fn=cmd_deepdive)

    p = sub.add_parser("reports", parents=[common], help="列出归档报告")
    p.add_argument("--asin")
    p.add_argument("--type")
    p.add_argument("--starred", action="store_true")
    p.add_argument("--query")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_reports)

    p = sub.add_parser("report", parents=[common], help="读取单份归档报告")
    p.add_argument("--id", type=int, required=True)
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    if not hasattr(args, "compact"):
        args.compact = False
    args.fn(args)
    raise SystemExit(_exit_code)


if __name__ == "__main__":
    main()
