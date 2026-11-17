#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抖音评论采集 CLI（纯 Python 签名 + mssdk 真 msToken，零浏览器、零 node）。

功能：
- 输入：抖音视频完整 URL、短链「转发链接」(v.douyin.com/xxx)，或直接传数字 aweme_id。
- 解析出 aweme_id → 调创作者中心评论接口（默认，aid=2906）拉评论。
- 支持分页、JSON / CSV 输出到文件或 stdout。
- 可选：``--analyze`` 触发 jieba 分词 + 停用词过滤 + 词频统计（依赖 jieba）。

重要约束（务必先读 SKILL.md）：
- 创作者评论接口存在**账号域隔离**：必须用**该视频所属账号本人**的 cookie 调用，
  跨账号会返回 ``status_code:5``。cookie 通过 ``--cookie`` 或环境变量 ``DOUYIN_COOKIE`` 传入。
- 抖音公开评论接口（www.douyin.com/aweme/v1/web/comment/list/，aid=6383）自 ~08-20 起
  被加固，对非真实浏览器静默空体；可用 ``--endpoint public`` 试探，但很可能返回空。
- a_bogus 是逆向算法，抖音改签名即失效 → 此时本工具抛错，请改用浏览器方案或等待算法更新。

依赖：httpx（必须）。jieba（仅 ``--analyze`` 时需要）。
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import sys
import urllib.parse

# 把 scripts/ 加入 path，使 sign / mstoken / analyze 可被导入
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 必装依赖 httpx：首次运行时若缺失，自动装到「当前解释器」（避免 pip 装错环境）。
try:
    import httpx  # noqa: E402
except ImportError:  # pragma: no cover - 仅在未装依赖时触发
    import subprocess

    sys.stderr.write(
        "[依赖自检] 未检测到必装依赖 httpx，正在自动安装到当前解释器 "
        f"({sys.executable}) ...\n"
    )
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "httpx>=0.27"]
        )
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(
            f"[错误] httpx 自动安装失败：{exc}\n"
            f"请手动运行：{sys.executable} -m pip install -r "
            f"{os.path.join(_HERE, 'requirements.txt')}\n"
            "或执行技能自带安装器：python install.py\n"
        )
        sys.exit(1)
    import httpx  # noqa: E402

try:  # 关掉 verify=False 的告警噪音
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:  # noqa: BLE001
    pass

from sign import ABogusPureSigner  # noqa: E402
from sign.fingerprint import get_profile  # noqa: E402
from mstoken import get_mstoken  # noqa: E402

logger = logging.getLogger("douyin-comment")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
)
_HEADERS = {
    "user-agent": UA,
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "priority": "u=1, i",
}

# 端点配置：creator=创作者中心（默认，需本人 cookie）；public=公开接口（实验性，可能已被加固）
ENDPOINTS = {
    "creator": {
        "api": ("https://creator.douyin.com/web/api/third_party/aweme/api/"
                "comment/read/aweme/v1/web/comment/list/select/"),
        "aid": "2906",
        "app_id": "2906",
        "channel_id": "618",
        "signer_aid": 2906,
        "referer_tpl": "https://creator.douyin.com/creator-micro/work-management/work-detail/{}",
        "sec_fetch_site": "same-origin",
    },
    "public": {
        "api": "https://www.douyin.com/aweme/v1/web/comment/list/",
        "aid": "6383",
        "app_id": "6383",
        "channel_id": "0",
        "signer_aid": 6383,
        "referer_tpl": "https://www.douyin.com/video/{}",
        "sec_fetch_site": "same-site",
    },
}


# ----------------------------------------------------------------------
# URL / 转发链接 → aweme_id
# ----------------------------------------------------------------------
def resolve_aweme_id(url: str, timeout: float = 15.0) -> str:
    """从完整 URL、短链转发链接或纯数字 id 解析出 aweme_id。

    短链 ``v.douyin.com/xxx`` 会被 301/302 重定向到
    ``https://www.douyin.com/video/<aweme_id>``，跟随重定向即可拿到 id。
    """
    url = (url or "").strip()
    if re.fullmatch(r"\d{10,}", url):
        return url
    if not re.match(r"^https?://", url):
        raise ValueError(f"无法识别的输入（既非 URL 也非纯数字 aweme_id）：{url!r}")

    try:
        r = httpx.get(
            url,
            headers={"user-agent": UA, "accept": "text/html,*/*"},
            timeout=timeout,
            follow_redirects=True,
            verify=False,
        )
        final = str(r.url)
        body = r.text
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"解析链接失败（无法访问 {url}）：{exc}") from exc

    # 1) 先从最终 URL 路径拿 /video/<id> 或 /note/<id>
    m = re.search(r"/(?:video|note)/(\d+)", final)
    if m:
        return m.group(1)
    # 2) 再从页面 HTML 内嵌 JSON 兜底（部分分享页用 sec_item_id，需二次解析）
    for pat in (
        r'aweme_id["\':\s]+(\d{10,})',
        r'"awemeId"\s*:\s*(\d{10,})',
        r'itemId["\':\s]+(\d{10,})',
        r'/"video/(\d{10,})',
    ):
        m = re.search(pat, body)
        if m:
            return m.group(1)
    raise ValueError(
        f"无法从链接解析出 aweme_id：{url} → 最终地址 {final}。"
        "请确认链接指向单个抖音作品（视频/图文），而非主页或直播。"
    )


# ----------------------------------------------------------------------
# cookie / 请求
# ----------------------------------------------------------------------
def parse_cookie(cookie_str: str) -> dict:
    """'k=v; k2=v2' -> {k: v}，按首个 '=' 切分，并对值做 URL 解码。"""
    out: dict = {}
    for part in (cookie_str or "").split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = urllib.parse.unquote(v.strip())
        else:
            out[part] = ""
    return out


def _splice_url(params: dict) -> str:
    """query 串：key=quote(value) 用 & 连接；顺序即签名的一部分，必须稳定。"""
    out = ""
    for key, value in params.items():
        if value is None:
            value = ""
        out += key + "=" + urllib.parse.quote(str(value)) + "&"
    return out[:-1]


def _fake_ms_token(length: int = 128) -> str:
    import random
    base = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789="
    return "".join(random.choice(base) for _ in range(length))


def _www_probe(cookies: dict, timeout: float = 8.0) -> str:
    """探针：用同一份 cookie 打 www.douyin.com 首页，看会话是否对抖音域有效。"""
    try:
        h = dict(_HEADERS)
        h["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
        r = httpx.get("https://www.douyin.com/", headers=h, timeout=timeout,
                     verify=False, follow_redirects=True)
        return f"status={r.status_code} len={len(r.text)}"
    except Exception as exc:  # noqa: BLE001
        return f"exc={type(exc).__name__}:{exc}"


def fetch_raw(aweme_id: str, cookie_str: str, cursor: str = "0",
              count: int = 20, endpoint: str = "creator", timeout: float = 20.0) -> dict:
    """拉单页评论，返回响应体 dict（含 comments / cursor / has_more / total）。"""
    cfg = ENDPOINTS[endpoint]
    signer = ABogusPureSigner(fixed=False, aid=cfg["signer_aid"])
    fp = get_profile()

    params: dict = {}
    params["device_platform"] = "webapp"
    params["aid"] = cfg["aid"]
    params["app_id"] = cfg["app_id"]
    params["channel_id"] = cfg["channel_id"]
    params["aweme_id"] = aweme_id
    params["cursor"] = cursor
    params["count"] = str(count)
    params["sort_options"] = "1"  # 1=按时间最新
    params["screen_width"] = fp["screen_width"]
    params["screen_height"] = fp["screen_height"]
    params["browser_language"] = "zh-CN"
    params["browser_platform"] = fp["platform"]
    params["browser_name"] = fp["browser_name"]
    params["browser_version"] = fp["browser_version"]
    params["browser_online"] = "true"
    params["engine_name"] = "Blink"
    params["engine_version"] = fp["engine_version"]
    params["os_name"] = "Windows"
    params["os_version"] = fp["os_version"]
    params["cpu_core_num"] = fp["cpu_core_num"]
    params["device_memory"] = fp["device_memory"]
    params["platform"] = "PC"
    params["downlink"] = "10"
    params["effective_type"] = "4g"
    params["round_trip_time"] = "0"
    cookies = parse_cookie(cookie_str)
    s_v_web_id = cookies.get("s_v_web_id", "")
    params["webid"] = s_v_web_id or "0"
    params["verifyFp"] = s_v_web_id
    params["fp"] = s_v_web_id

    ms_token = get_mstoken(cookie_str)
    if not ms_token:
        logger.warning("mssdk 换发失败，回退假 msToken（抖音边缘可能直接丢弃请求 → 空响应体）")
        ms_token = _fake_ms_token()
    params["msToken"] = ms_token

    query = _splice_url(params)
    # 签名 URL 的主机必须与端点一致：创作者域签 creator、公开域签 www，
    # 否则抖音服务端校验 host 不匹配会直接丢弃请求（~08-20 加固后更严格）。
    sign_host = "https://creator.douyin.com/" if endpoint == "creator" else "https://www.douyin.com/"
    params["a_bogus"] = signer.sign(f"{sign_host}?{query}")
    final_url = cfg["api"] + "?" + _splice_url(params)

    headers = dict(_HEADERS)
    headers["user-agent"] = fp["ua"]
    headers["referer"] = cfg["referer_tpl"].format(aweme_id)
    headers["sec-fetch-site"] = cfg["sec_fetch_site"]
    headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())

    resp = httpx.get(final_url, headers=headers, timeout=timeout, verify=False)
    status = resp.status_code
    try:
        resp_json = resp.json()
    except Exception as exc:  # noqa: BLE001
        body = resp.text[:240]
        raise RuntimeError(
            f"评论请求失败 aweme_id={aweme_id} endpoint={endpoint}: status={status} "
            f"body={body!r} :: www_probe={_www_probe(cookies)} :: {exc}"
        ) from exc

    sc = resp_json.get("status_code")
    if sc not in (None, 0):
        extra = ""
        if endpoint == "public" and sc == 5:
            extra = "（公开接口疑似被加固，请改用默认 creator 端点 + 本人 cookie）"
        raise RuntimeError(
            f"评论接口拒绝 aweme_id={aweme_id} endpoint={endpoint} status_code={sc} "
            f"msg={resp_json.get('status_msg')}{extra}"
        )
    if not isinstance(resp_json.get("comments"), (list, type(None))):
        raise RuntimeError(
            f"评论响应结构异常 aweme_id={aweme_id}: {list(resp_json.keys())}"
        )
    return resp_json


# ----------------------------------------------------------------------
# 翻页采集
# ----------------------------------------------------------------------
def fetch_all(aweme_id: str, cookie_str: str, *, count: int = 20,
              max_pages: int = 20, endpoint: str = "creator",
              timeout: float = 20.0) -> list:
    """翻页拉取所有评论（含二级回复），返回扁平化后的评论列表。"""
    comments: list = []
    cursor = "0"
    pages = 0
    while True:
        pages += 1
        resp = fetch_raw(aweme_id, cookie_str, cursor=cursor, count=count,
                         endpoint=endpoint, timeout=timeout)
        page_comments = resp.get("comments") or []
        if not page_comments:
            logger.info("第 %d 页无更多评论，停止。", pages)
            break
        for c in page_comments:
            comments.append(_flatten(c))
            subs = c.get("sub_comments") or []
            for sub in subs:
                comments.append(_flatten(sub, parent_cid=c.get("cid")))
        has_more = resp.get("has_more")
        cursor = str(resp.get("cursor") or cursor)
        logger.info("已采集 %d 条（第 %d 页，has_more=%s，total=%s）",
                    len(comments), pages, has_more, resp.get("total"))
        if not has_more:
            break
        if max_pages and pages >= max_pages:
            logger.info("达到 max_pages=%d 上限，停止。", max_pages)
            break
    return comments


def _flatten(c: dict, parent_cid: str | None = None) -> dict:
    user = c.get("user") or {}
    return {
        "cid": c.get("cid"),
        "parent_cid": parent_cid,
        "text": c.get("text", ""),
        "user_id": user.get("uid"),
        "nickname": user.get("nickname"),
        "digg_count": c.get("digg_count"),
        "reply_count": c.get("reply_comment_total") or c.get("reply_count"),
        "ip_label": c.get("ip_label"),
        "create_time": c.get("create_time"),
        "aweme_id": c.get("aweme_id"),
    }


# ----------------------------------------------------------------------
# 输出
# ----------------------------------------------------------------------
def write_output(comments: list, fmt: str, path: str | None) -> None:
    if fmt == "csv":
        fields = ["cid", "parent_cid", "text", "user_id", "nickname",
                  "digg_count", "reply_count", "ip_label", "create_time", "aweme_id"]
        out = ""
        import io
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fields)
        w.writeheader()
        for c in comments:
            w.writerow({k: c.get(k, "") for k in fields})
        out = buf.getvalue()
    else:
        out = json.dumps(comments, ensure_ascii=False, indent=2)

    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        logger.info("已写入 %d 条评论 -> %s", len(comments), path)
    else:
        print(out)


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fetch_comments",
        description="抖音评论采集：URL/转发链接 → 评论 JSON/CSV（支持纯Python签名 与 无头浏览器游客态免登录）",
    )
    p.add_argument("url", help="抖音视频完整URL / 短链转发链接(v.douyin.com) / 纯数字 aweme_id")
    p.add_argument("--cookie", help="抖音 cookie 字符串（本人账号）；也可设环境变量 DOUYIN_COOKIE")
    p.add_argument("--endpoint", choices=["creator", "public"], default="creator",
                   help="creator=创作者中心(默认,需本人cookie)；public=公开接口(实验性,可能已被加固)")
    p.add_argument("--guest", action="store_true",
                   help="游客态：零 cookie 直接打公开接口，仅用于验证可用性（实测抖音已加固，大概率空体）")
    p.add_argument("--browser", action="store_true",
                   help="无头浏览器模式（推荐）：真实 Chromium 打开视频页，绕过纯HTTP空体风控，自动翻页采集。"
                        "默认游客态仅抓前~14-20条；运行 login_helper.py 登录后（--cookie-file 自动读取）可越评论墙拿全部。"
                        "需 playwright：pip install playwright && playwright install chromium")
    p.add_argument("--no-headless", action="store_true", help="浏览器模式关闭无头（可肉眼观察是否被风控弹窗拦截）")
    p.add_argument("--cookie-file", default=None,
                   help="登录态 cookie 文件路径（由 login_helper.py 生成）；缺省自动探测 scripts/douyin_cookie.json。"
                        "提供后浏览器以登录态抓取，可越过评论墙拿到更多评论")
    p.add_argument("--count", type=int, default=20, help="每页条数（默认20）")
    p.add_argument("--max-pages", type=int, default=20, help="HTTP 模式最大翻页数（默认20，0=不设上限）")
    p.add_argument("--max-scrolls", type=int, default=20, help="浏览器模式最大滚动加载次数（默认20）")
    p.add_argument("--format", choices=["json", "csv"], default="json", help="输出格式")
    p.add_argument("--output", help="输出文件路径（缺省打印到 stdout）")
    p.add_argument("--analyze", action="store_true", help="附带 jieba 分词 + 停用词词频分析")
    p.add_argument("--top-n", type=int, default=50, help="词频分析返回前 N 个词（默认50）")
    p.add_argument("--stopwords", help="自定义停用词文件路径（每行一个词）")
    p.add_argument("--min-word-len", type=int, default=2, help="词频分析最小词长（默认2）")
    p.add_argument("-v", "--verbose", action="store_true", help="打印调试日志")
    return p


def _finalize(comments: list, args, aweme_id=None) -> int:
    """共用：写出评论 + 可选的 jieba 词频分析。"""
    if not comments:
        logger.warning(
            "未采集到评论。常见原因：① 浏览器游客态命中抖音评论墙（登录后可见全部）→ 换 --cookie 创作者接口；"
            "② 视频无评论；③ 网络/风控。"
        )
        write_output([], args.format, args.output)
        return 0

    # 词频分析（可选）
    if args.analyze:
        try:
            from analyze import analyze_comments
            words = analyze_comments(
                [c.get("text", "") for c in comments if c.get("text")],
                top_n=args.top_n,
                stopwords_path=args.stopwords,
                min_len=args.min_word_len,
            )
            result = {
                "aweme_id": aweme_id,
                "comment_count": len(comments),
                "word_freq_top": words,
            }
            if args.output:
                base, _ = os.path.splitext(args.output)
                ana_path = base + ".analyze.json"
                with open(ana_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logger.info("词频分析已写入 %s", ana_path)
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except ImportError:
            logger.error("词频分析需要 jieba：pip install jieba（或 scripts/requirements.txt）")
            return 1

    write_output(comments, args.format, args.output)
    return 0


def main(argv=None) -> int:
    args = build_argparser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    # ---- 无头浏览器模式（游客态免登录 / 登录态可越评论墙）----
    if args.browser:
        try:
            from browser_fetch import fetch_with_browser, DEFAULT_COOKIE_FILE
        except ImportError:
            logger.error(
                "无头浏览器模式需要 playwright：\n"
                "  pip install playwright && playwright install chromium\n"
                "（不装也可继续使用默认纯 HTTP 创作者接口方案，但需本人 cookie）"
            )
            return 2
        # cookie 文件：显式 > 自动探测 scripts/douyin_cookie.json > 游客态
        cookie_file = args.cookie_file
        if not cookie_file and os.path.exists(DEFAULT_COOKIE_FILE):
            cookie_file = DEFAULT_COOKIE_FILE
        if cookie_file:
            logger.info("使用登录态 cookie：%s", cookie_file)
        else:
            logger.warning(
                "未检测到 cookie 文件 → 游客态抓取：抖音会弹「评论墙」，通常仅返回前 ~14-20 条样本。"
                "如需更多/全部评论，请先运行 python login_helper.py 登录（--cookie-file 会自动读取）。"
            )
        try:
            comments = fetch_with_browser(
                args.url,
                max_scrolls=args.max_scrolls,
                scroll_pause=1200,
                headless=not args.no_headless,
                cookie_file=cookie_file,
            )
        except Exception as exc:
            logger.error("浏览器采集失败：%s", exc)
            return 1
        try:
            aweme_id = resolve_aweme_id(args.url)
        except Exception:
            aweme_id = None
        return _finalize(comments, args, aweme_id)

    # ---- 纯 HTTP 模式 ----
    cookie = args.cookie or os.environ.get("DOUYIN_COOKIE", "")
    if args.guest:
        # 游客态：允许零 cookie 试探公开接口（实测抖音已加固，大概率空体）
        if args.endpoint == "creator":
            logger.warning("--guest 无 cookie 时 creator 端点必失败，已自动切到 public 端点试探")
            args.endpoint = "public"
        if not cookie:
            logger.warning("游客态：未提供 cookie，将以纯游客身份打公开接口（仅用于验证，通常空体）")
    elif not cookie:
        logger.error("缺少 cookie：请用 --cookie 传入本人账号 cookie，或设置环境变量 DOUYIN_COOKIE；"
                     "仅想验证公开接口可用性可加 --guest（零 cookie）；免登录推荐加 --browser（无头浏览器）")
        return 2

    try:
        aweme_id = resolve_aweme_id(args.url)
    except Exception as exc:
        logger.error("%s", exc)
        return 1
    logger.info("解析到 aweme_id=%s（endpoint=%s）", aweme_id, args.endpoint)

    try:
        comments = fetch_all(
            aweme_id, cookie,
            count=args.count,
            max_pages=args.max_pages,
            endpoint=args.endpoint,
        )
    except Exception as exc:
        logger.error("%s", exc)
        return 1

    return _finalize(comments, args, aweme_id)


if __name__ == "__main__":
    raise SystemExit(main())
