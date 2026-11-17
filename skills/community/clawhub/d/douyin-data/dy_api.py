#!/usr/bin/env python3
"""抖音数据平台客户端（skill 配套 CLI）。

环境变量：
  DY_PLATFORM_BASE_URL  （可选）平台地址，默认 https://zlh.aidata366.com；
                        也可被 login 保存的本机配置文件覆盖
  DY_PLATFORM_API_KEY   （可选）执行 login 后自动保存到本机配置文件；
                        显式设置环境变量时优先级更高
  DY_IDEMPOTENCY_KEY    （可选）整批任务共用的幂等键；--idem 优先
  DY_PLATFORM_PROXY     （可选）显式代理，如 http://127.0.0.1:7890。
                        默认**不读** HTTP_PROXY/HTTPS_PROXY

AI 来源参数（所有 API 命令必填）：--skill-name douyin-data --ai-entry <AI工具标识>
IP 无需传递，由服务端自动获取；首次缺参告警放行，第二次起拒绝。

用法：
  python dy_api.py login --skill-name douyin-data --ai-entry claude-code       # 扫码/链接登录（首次）
  python dy_api.py login_check --access-token <token> --skill-name douyin-data --ai-entry claude-code
  python dy_api.py balance --skill-name douyin-data --ai-entry claude-code
  python dy_api.py video_detail 7579597758630268186 --skill-name douyin-data --ai-entry claude-code
  python dy_api.py video_detail aweme_id=7579597758630268186 --idem task-0001 --skill-name douyin-data --ai-entry claude-code
  python dy_api.py comments aweme_id=7579597758630268186 --out ./comments_p1.json --skill-name douyin-data --ai-entry claude-code
  python dy_api.py search 美食 --out ./search_p1.json --skill-name douyin-data --ai-entry claude-code

退出码：0 成功；2 参数/配置错误；3 鉴权或余额问题；4 本次取数失败；5 网络问题；
        6 等待用户完成授权（login_check 轮询时）。
"""
import json
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request

DEFAULT_BASE = "https://zlh.aidata366.com"
CONFIG_PATH = (os.environ.get("ZLH_CONFIG_PATH")
               or os.path.join(os.path.expanduser("~"), ".zhi_liao_hou", "config.json"))


def _load_config() -> dict:
    """读取 CLI 登录后保存的凭证；失败按未配置处理。"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


_cfg = _load_config()

BASE = (os.environ.get("DY_PLATFORM_BASE_URL", "").strip().rstrip("/")
        or str(_cfg.get("base_url") or "").rstrip("/") or DEFAULT_BASE)
KEY = (os.environ.get("DY_PLATFORM_API_KEY", "").strip()
       or str(_cfg.get("api_key") or "").strip())
SKILL_NAME = "douyin-data"
SKILL_VERSION = "1.0.9"

# 默认不走系统代理：企业网络常设 HTTP_PROXY，urllib 会默默套用导致本地地址也走代理。
PROXY = os.environ.get("DY_PLATFORM_PROXY", "").strip()

DEFAULT_TIMEOUT = 60          # 抖音上游较慢（搜索类实测 5~10s），留足余量
DEFAULT_RETRY = 1
BIG_RESPONSE_BYTES = 100_000  # 超过此大小提示落盘（抖音搜索/主页接口常见 600KB+）

# code -> (是否可重试, 中文说明, 处置建议)
ERRORS = {
    40000: (False, "请求体非法", "修正 payload 后重试；不要原样重发"),
    40100: (False, "API Key 无效", "检查 DY_PLATFORM_API_KEY，或到平台「API Key」页重新创建"),
    40101: (False, "API Key 已停用", "到平台「API Key」页启用或新建 Key"),
    40200: (False, "点数不足", "先查 balance 估算成本，引导用户充值；不要重试"),
    40201: (False, "接口未开放", "该接口已停用，改用其它接口或联系客服"),
    40300: (True, "触发限频", "等待约 60 秒再继续，降低并发"),
    40910: (False, "幂等键冲突", "该键已用于其它接口/参数；换一个新键"),
    40911: (True, "同键请求处理中", "等待 2~3 秒后用同一键重试"),
    40912: (False, "响应过大未缓存",
            "幂等键命中了但原响应超过平台缓存上限（抖音大响应常见）。"
            "本次未扣费，换一个新 --idem 键重新调用即可"),
    50000: (False, "本次取数失败",
            "把 msg 告知用户；下方会显示本次退款点数，未退款表示成本已产生"),
    50001: (False, "数据服务暂不可用", "停止任务并告知用户稍后再试"),
    50002: (True, "数据服务响应超时", "用同一幂等键重试（平台已保留幂等记录）"),
    50003: (True, "平台并发已满", "降低并发后重试"),
}

# 命令 -> 平台接口。params 与平台 doc_json 白名单一致，未声明的参数会被平台丢弃。
ENDPOINTS = {
    "video_detail": {
        "path": "/api/v1/douyin/aweme_detail",
        "one_of": ["aweme_id", "share_text"],
        "required": [],
        "params": ["aweme_id", "share_text"],
        "desc": "视频详情（标题/作者/点赞评论分享数/下载地址）",
    },
    "video_detail_v3": {
        "path": "/api/v1/douyin/aweme_detail_v3",
        "one_of": ["aweme_id", "share_text"],
        "required": [],
        "params": ["aweme_id", "share_text"],
        "desc": "视频详情 v3（字段更全，响应较大）",
    },
    "comments": {
        "path": "/api/v1/douyin/video_comment",
        "one_of": ["aweme_id", "share_text"],
        "required": [],
        "params": ["aweme_id", "share_text", "cursor", "count"],
        "desc": "一级评论（含评论 cid，用于取二级回复）",
    },
    "replies": {
        "path": "/api/v1/douyin/video_sub_comment",
        "required": ["aweme_id", "comment_id"],
        "one_of": [],
        "params": ["aweme_id", "comment_id", "cursor"],
        "desc": "二级评论（某个一级评论下的回复）",
    },
    "user": {
        "path": "/api/v1/douyin/user_data",
        "one_of": ["sec_user_id", "share_text"],
        "required": [],
        "params": ["sec_user_id", "share_text"],
        "desc": "用户信息（昵称/粉丝数/获赞/作品数/简介）",
    },
    "user_posts": {
        "path": "/api/v1/douyin/user_post",
        "one_of": ["sec_user_id", "share_text"],
        "required": [],
        "params": ["sec_user_id", "share_text", "cursor", "count"],
        "desc": "用户主页作品列表（翻页用 max_cursor）",
    },
    "search": {
        "path": "/api/v1/douyin/general_search2",
        "required": ["keyword"],
        "one_of": [],
        "params": ["keyword", "cursor", "sort_type", "publish_time",
                   "filter_duration", "content_type"],
        "desc": "综合搜索（推荐版本，结果在 data.business_data[]）",
    },
    "search_v1": {
        "path": "/api/v1/douyin/general_search",
        "required": ["keyword"],
        "one_of": [],
        "params": ["keyword", "cursor", "sort_type", "publish_time",
                   "filter_duration", "content_type"],
        "desc": "综合搜索 v1（已下架，调用返回 40201；请改用 search）",
    },
    "suggest": {
        "path": "/api/v1/douyin/search_sug",
        "required": ["keyword"],
        "one_of": [],
        "params": ["keyword"],
        "desc": "衍生词搜索（搜索下拉建议词）",
    },
    "share_to_id": {
        "path": "/api/v1/douyin/share_id_to_web_id",
        "required": ["share_link"],
        "one_of": [],
        "params": ["share_link"],
        "desc": "分享短链转视频 ID 与网页链接",
    },
}

FIELDS = {
    "aweme_id": "视频 ID，如 7579597758630268186（从 douyin.com/video/<id> 取）",
    "share_text": "抖音分享文案整段（含短链，可自动解析）",
    "sec_user_id": "用户加密 ID（MS4wLjABAAAA...，从用户主页分享或分享文案取）",
    "share_link": "分享短链，只传纯 URL（如 https://v.douyin.com/xxxx/）；传整段分享文案会报 50000，该失败平台会自动退款",
    "keyword": "搜索关键词",
    "cursor": "翻页游标：首页留空(或 0)，后续传上次响应里的 cursor/max_cursor",
    "count": "每页条数，默认 20",
    "comment_id": "一级评论的 cid（从 comments 响应 comments[].cid 取）",
    "sort_type": "排序：0综合 1最多点赞 2最新（空表示默认）",
    "publish_time": "发布时间筛选：1一天内 7一周内 180半年内（空表示不限）",
    "filter_duration": "时长筛选（空表示不限）",
    "content_type": "内容类型筛选（空表示不限）",
}


def _source_headers() -> dict:
    """AI 显式提供 Skill/入口；版本和客户端标识由 CLI 自动附加。"""
    values = {"skill_name": "", "ai_entry": ""}
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        for key in values:
            flag = "--" + key.replace("_", "-")
            if arg == flag and i + 1 < len(args):
                values[key] = args[i + 1].strip()
            elif arg.startswith(flag + "="):
                values[key] = arg.split("=", 1)[1].strip()
    valid_name = values["skill_name"] == SKILL_NAME
    valid_entry = re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}",
                               values["ai_entry"], re.I) is not None
    if not valid_name or not valid_entry:
        print(f"AI 来源参数提醒：所有 API 命令必须传 --skill-name {SKILL_NAME} "
              "--ai-entry <AI工具标识>；首次缺参告警放行，第二次起拒绝", file=sys.stderr)
    headers = {"X-Skill-Client": "cli", "X-Skill-Version": SKILL_VERSION}
    if valid_name:
        headers["X-Skill-Name"] = SKILL_NAME
    if valid_entry:
        headers["X-AI-Entry"] = values["ai_entry"]
    return headers


def _opener():
    """构造 opener：默认忽略环境代理；显式配置 DY_PLATFORM_PROXY 时才走代理。"""
    if PROXY:
        handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
    else:
        handler = urllib.request.ProxyHandler({})
    return urllib.request.build_opener(handler)


def _request(path: str, payload: dict | None, idem_key: str | None, timeout: int):
    """发一次请求，返回 (http_status, body_dict|None, raw_text)。网络错误抛 OSError。"""
    url = BASE + path
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("X-Api-Key", KEY)
    req.add_header("Accept", "application/json")
    for name, value in _source_headers().items():
        req.add_header(name, value)
    if data:
        req.add_header("Content-Type", "application/json; charset=utf-8")
    if idem_key:
        req.add_header("Idempotency-Key", idem_key)
    warning = ""
    try:
        with _opener().open(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", "replace")
            status = resp.status
            warning = resp.headers.get("X-Skill-Metadata-Warning", "")
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")
        status = exc.code
        warning = exc.headers.get("X-Skill-Metadata-Warning", "") if exc.headers else ""
    if warning:
        print(f"# AI 来源参数告警（{warning}）：本次已放行；下次起缺参将拒绝", file=sys.stderr)
    try:
        return status, json.loads(text), text
    except ValueError:
        return status, None, text


class PlatformError(RuntimeError):
    """平台返回了业务错误（带 code）。"""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def call(path: str, payload: dict | None = None, idem_key: str | None = None,
         timeout: int = DEFAULT_TIMEOUT, retry: int = DEFAULT_RETRY) -> dict:
    """调用平台接口；网络类失败按 retry 自动重试（始终复用同一幂等键）。"""
    attempt, last_err = 0, ""
    while True:
        attempt += 1
        try:
            status, body, text = _request(path, payload, idem_key, timeout)
        except OSError as exc:
            last_err = f"网络错误: {exc}"
            if attempt <= retry:
                time.sleep(min(2 * attempt, 5))
                continue
            raise RuntimeError(
                f"{last_err}（已重试 {retry} 次；如平台不可达请确认地址/代理，"
                f"必要时用 DY_PLATFORM_PROXY 指定代理）") from exc

        if body is None:
            raise RuntimeError(f"平台返回非 JSON 响应（HTTP {status}）：{text[:200]}")

        code = body.get("code")
        if code == 0:
            return body

        retryable, label, action = ERRORS.get(
            code, (False, "未知错误", "把 code/msg/request_id 一并告知用户，便于后台排查"))
        rid = body.get("request_id", "")
        if retryable and attempt <= retry:
            time.sleep(3 if code == 40911 else min(2 * attempt, 5))
            continue
        data = body.get("data") if isinstance(body.get("data"), dict) else {}
        money = ""
        if "refunded" in data or "balance" in data:
            money = (f"\n本次退款: {data.get('refunded', 0)} 点"
                     f"，当前余额: {data.get('balance', '-')} 点")
        raise PlatformError(
            code if isinstance(code, int) else -1,
            f"调用失败 code={code}（{label}）msg={body.get('msg')} "
            f"request_id={rid or '-'}{money}\n建议：{action}")


def _usage() -> str:
    rows = "\n".join(
        f"  {name:16s} {meta['desc']}\n"
        f"  {'':16s} 参数: {', '.join(meta['params'])}"
        f"{' | 其中 ' + '/'.join(meta['one_of']) + ' 二选一必填' if meta['one_of'] else ''}"
        f"{' | 必填: ' + ', '.join(meta['required']) if meta['required'] else ''}"
        for name, meta in ENDPOINTS.items())
    fields = "\n".join(f"  {k:16s} {v}" for k, v in FIELDS.items())
    return (f"{__doc__}\n可用命令：\n"
            f"  login            扫码/链接登录授权（无需 API Key，首次使用）\n"
            f"  login_check      校验授权并保存 API Key（需 --access-token）\n"
            f"  balance          查询余额/单价（免费）\n{rows}\n"
            f"参数说明：\n{fields}")


def _save_config(base_url: str, api_key: str, username: str, balance_points) -> str:
    """保存登录凭证到本机配置文件，供后续所有 skill 复用。"""
    folder = os.path.dirname(CONFIG_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    payload = {
        "base_url": base_url,
        "api_key": api_key,
        "username": username,
        "balance_points": balance_points,
        "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except OSError:
        pass
    return CONFIG_PATH


def cmd_login(retry: int, timeout: int) -> int:
    """创建 CLI 登录会话，输出二维码/授权链接与后续校验命令（不需要 API Key）。"""
    # 上送本 Skill 名：服务端记录 users.source_skill（仅首绑），用于统计下载来源
    body = call("/auth/cli-session", {"skill_name": SKILL_NAME}, timeout=timeout, retry=retry)
    data = body.get("data") or {}
    token = data.get("access_token", "")
    qr_url = BASE + str(data.get("qr_path", ""))
    login_url = BASE + str(data.get("login_path", ""))
    script = os.path.basename(sys.argv[0])
    print("请让用户用手机扫码，或在浏览器打开下面的链接完成登录并确认授权"
          f"（{data.get('expires_in', 600) // 60} 分钟内有效）：")
    print(f"二维码图片：{qr_url}")
    print(f"授权链接：{login_url}")
    print(f"access_token：{token}")
    print("\n用户确认授权后，执行下面的命令校验并保存 API Key：")
    print(f"python {script} login_check --access-token {token} "
          f"--skill-name {SKILL_NAME} --ai-entry <AI工具标识>")
    print("\n" + json.dumps(body, ensure_ascii=False, indent=2))
    return 0


def cmd_login_check(access_token, retry: int, timeout: int) -> int:
    """轮询授权结果；ready 时把 API Key 写入本地配置（exit 6 表示继续等待）。"""
    if not access_token:
        print("缺少 --access-token：请先执行 login 命令获取", file=sys.stderr)
        return 2
    body = call("/auth/cli-session/check", {"access_token": access_token},
                timeout=timeout, retry=retry)
    data = body.get("data") or {}
    status = data.get("status")
    if status == "pending":
        print("用户还没有完成授权：请让用户打开登录链接/扫码并确认，"
              "3~5 秒后重新执行本命令", file=sys.stderr)
        return 6
    if status != "ready":
        print("授权链接已失效或已被使用：请重新执行 login 命令生成新链接", file=sys.stderr)
        return 2
    path = _save_config(BASE, data.get("api_key", ""), data.get("username", ""),
                        data.get("balance_points", 0))
    print(json.dumps(body, ensure_ascii=False, indent=2))
    print(f"\n# 登录成功：API Key 已保存到 {path}", file=sys.stderr)
    print("# 后续可直接运行 balance 等命令；环境变量 "
          "DY_PLATFORM_API_KEY 优先级更高", file=sys.stderr)
    return 0


def _die(msg: str) -> "NoReturn":
    print(msg, file=sys.stderr)
    sys.exit(2)


def _parse_payload(meta: dict, tokens: list[str]) -> dict:
    """解析参数：支持 位置参数 / key=value / 整段 JSON 三种写法。"""
    if len(tokens) == 1 and tokens[0].lstrip().startswith("{"):
        try:
            payload = json.loads(tokens[0])
        except ValueError as exc:
            _die(f"JSON 参数解析失败：{exc}")
        if not isinstance(payload, dict):
            _die('JSON 参数必须是对象，如 {"aweme_id":"7579597758630268186"}')
    elif any("=" in t for t in tokens):
        payload = {}
        for t in tokens:
            if "=" not in t:
                _die(f"参数 {t!r} 缺少 '='，位置参数与 key=value 不要混用")
            k, v = t.split("=", 1)
            payload[k.strip()] = v
    else:
        payload = dict(zip(meta["params"], tokens))
        if len(tokens) > len(meta["params"]):
            _die(f"参数过多：{tokens[len(meta['params']):]}。该接口参数顺序为 "
                 f"{meta['params']}，建议改用 key=value 写法避免错位")

    unknown = [k for k in payload if k not in meta["params"]]
    if unknown:
        _die(f"未知参数 {unknown}；该接口只接受 {meta['params']}"
             "（平台按白名单转发，未声明字段会被静默丢弃）")
    missing = [k for k in meta["required"] if not str(payload.get(k, "")).strip()]
    if missing:
        _die(f"缺少必填参数 {missing}（{FIELDS.get(missing[0], '')}）。"
             "已阻止本次请求以避免无效扣点")
    if meta["one_of"]:
        filled = [k for k in meta["one_of"] if str(payload.get(k, "")).strip()]
        if not filled:
            names = "/".join(meta["one_of"])
            hint = "；".join(f"{k} = {FIELDS.get(k, '')}" for k in meta["one_of"])
            _die(f"必须提供 {names} 中的至少一个。\n  {hint}\n已阻止本次请求以避免无效扣点")
    return _normalize_share_link(payload)


_SHARE_URL_RE = re.compile(r"https?://v\.douyin\.com/[A-Za-z0-9]+/?")


def _normalize_share_link(payload: dict) -> dict:
    """share_link 容错：用户常把「4.87 复制打开抖音… https://v.douyin.com/xxx/ 口令」
    整段文案直接塞进来，平台会返回 50000（虽会自动退款，但白跑一次）。
    本地先抽出纯短链，让调用一次成功。其它参数原样透传。"""
    link = str(payload.get("share_link") or "")
    if "v.douyin.com" not in link:
        return payload
    m = _SHARE_URL_RE.search(link)
    if not m or m.group(0) == link.strip():
        return payload
    print(f"# 已从分享文案中提取短链: {m.group(0)}", file=sys.stderr)
    return {**payload, "share_link": m.group(0)}


def _summary(body: dict, size: int) -> str:
    data = body.get("data") or {}
    platform = data.get("_platform") or {}
    keys = [k for k in data if k != "_platform"]
    return (f"code=0 request_id={body.get('request_id')} "
            f"扣点={platform.get('points_charged', '-')} 余额={platform.get('balance', '-')} "
            f"响应 {size} 字节，顶层字段：{', '.join(keys[:8])}"
            f"{' …' if len(keys) > 8 else ''}")


def main() -> int:
    args = sys.argv[1:]
    # 帮助先行：未配置环境变量时也要能看到用法
    if not args or args[0] in ("-h", "--help", "help"):
        print(_usage())
        return 0 if args else 2

    opts = {"idem": os.environ.get("DY_IDEMPOTENCY_KEY") or None,
            "retry": DEFAULT_RETRY, "timeout": DEFAULT_TIMEOUT, "out": None,
            "access_token": None}
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--skill-name", "--ai-entry"):
            if i + 1 >= len(args):
                print(f"{a} 缺少取值", file=sys.stderr)
                return 2
            i += 2
            continue
        if a.startswith(("--skill-name=", "--ai-entry=")):
            i += 1
            continue
        if a in ("--idem", "--retry", "--timeout", "--out", "--access-token"):
            if i + 1 >= len(args):
                print(f"{a} 缺少取值", file=sys.stderr)
                return 2
            val = args[i + 1]
            if a == "--retry":
                opts["retry"] = max(0, int(val))
            elif a == "--timeout":
                opts["timeout"] = max(5, int(val))
            elif a == "--out":
                opts["out"] = val
            elif a == "--access-token":
                opts["access_token"] = val.strip()
            else:
                opts["idem"] = val[:128]
            i += 2
            continue
        rest.append(a)
        i += 1

    if not rest:
        print(_usage())
        return 2
    cmd, tokens = rest[0], rest[1:]

    try:
        if cmd == "login":
            return cmd_login(opts["retry"], opts["timeout"])
        if cmd == "login_check":
            return cmd_login_check(opts["access_token"], opts["retry"], opts["timeout"])
        if not KEY:
            print(f"尚未登录：请先执行 python {os.path.basename(sys.argv[0])} login "
                  f"--skill-name {SKILL_NAME} --ai-entry <AI工具标识>，"
                  f"或设置环境变量 DY_PLATFORM_API_KEY", file=sys.stderr)
            return 2
        if cmd == "balance":
            body = call("/api/v1/account/balance", timeout=opts["timeout"],
                        retry=opts["retry"])
            data = body.get("data") or {}
            print(json.dumps(body, ensure_ascii=False, indent=2))
            prices = {e["code"]: e["price"] for e in data.get("endpoints", [])}
            if prices:
                print("\n# 单价（点/次）: " + ", ".join(f"{k}={v}" for k, v in prices.items()),
                      file=sys.stderr)
            return 0

        if cmd not in ENDPOINTS:
            print(f"未知命令 {cmd}\n\n{_usage()}", file=sys.stderr)
            return 2
        meta = ENDPOINTS[cmd]
        payload = _parse_payload(meta, tokens)

        # 只要可能重试，就必须带幂等键：否则超时重试会重复扣点
        if not opts["idem"] and opts["retry"] > 0:
            opts["idem"] = f"task-{uuid.uuid4().hex}"
        body = call(meta["path"], payload, idem_key=opts["idem"],
                    timeout=opts["timeout"], retry=opts["retry"])

        text = json.dumps(body, ensure_ascii=False, indent=2)
        size = len(text.encode("utf-8"))
        if opts["out"]:
            with open(opts["out"], "w", encoding="utf-8") as f:
                f.write(text)
            print(_summary(body, size) + f"\n已写入 {opts['out']}")
        else:
            print(text)
            print(_summary(body, size), file=sys.stderr)
            if size > BIG_RESPONSE_BYTES:
                print(f"# 响应较大（{size // 1024} KB）：批量任务建议用 --out 落盘，"
                      "避免刷屏与上下文超限", file=sys.stderr)
        if opts["idem"]:
            print(f"# 幂等键: {opts['idem']}（重试务必复用此键）", file=sys.stderr)
        return 0
    except PlatformError as exc:
        print(str(exc), file=sys.stderr)
        # 参数类 → 2；鉴权/余额/未开放 → 3；其余业务失败 → 4
        if exc.code == 40000:
            return 2
        if exc.code in (40100, 40101, 40200, 40201):
            return 3
        return 4
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
