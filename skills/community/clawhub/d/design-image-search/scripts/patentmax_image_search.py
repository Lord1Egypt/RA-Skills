#!/usr/bin/env python3
"""PatentMax 外观专利以图搜图客户端（v1.0.2）。

给 AI 用的命令行工具，走 POST /api/v1/reports 的 report_type=image_search。

**每条命令最多跑 30 秒就返回。** WorkBuddy 这类宿主前台跑命令时，要等命令结束才显示输出，
AI 中途也插不了话；一条命令阻塞几十分钟，用户就几十分钟什么都看不到，宿主还可能把命令掐掉。
所以 create 提交后只等 15 秒就先返回，之后用 wait 接着等，每次最多 30 秒：

    退出码 0   完成了（Word 报告已自动下载到提交时的目录）
    退出码 10  还在生成：把输出里的「[进度]」行告诉用户，再运行一次 wait
    退出码 2   输入有误（少必填项、文件读不了、方案太短），什么都没提交
    退出码 3   同样的任务已经在跑（这次没有重复提交、没有重复扣费），用输出里的 operation_id 接着 wait
    退出码 1   出错，message 是给用户看的中文说明，原样转述即可

输出：先打若干行「[进度] ……」，最后打一份 JSON。报告在服务端生成，命令结束、被杀、
对话关掉都不影响，任何时候 wait --operation-id 都能接着看。

Idempotency-Key 默认按请求内容算稳定指纹——同样的输入重跑 create，拿回的是同一个任务，不会重复扣费。

依赖：只用标准库，不需要 pip install。
"""

import argparse
import calendar
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

BASE_URL = os.environ.get("PATENTMAX_BASE_URL", "https://api.ip930.com").rstrip("/")
API_KEY = os.environ.get("PATENTMAX_API_KEY", "").strip()


# 试用金用完后，用户注册拿到的正式密钥由 AI 写进这个文件（只写密钥一行），所有 PatentMax 技能都会自动读取
def _saved_key_path():
    root = os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")
    return os.path.join(root, "api_key.txt")


if not API_KEY:
    try:
        API_KEY = open(_saved_key_path(), encoding="utf-8").read().strip()
    except OSError:
        pass

TRIAL_CONTINUE = "\n注册后在「API 平台」创建一个密钥（pm_live_ 开头）发给我，我存好后接着帮你做。"


def trial_end_extra():
    """试用金用完时附给 AI 的说明：原样转告、链接别省；收到密钥怎么存。"""
    return {"free_trial": True,
            "ai_hint": "把 message 原样转告用户，注册链接不要省略。用户发来密钥后，用 Write 工具把密钥本身（只写这一行）"
                       f"写进 {_saved_key_path()}，然后重跑刚才那条命令；不要把密钥写进别的文件。"}


TIMEOUT = 60

REPORT_TYPE = "image_search"
REPORT_NAME = "以图搜图结果"

EXIT_DONE, EXIT_ERROR, EXIT_INPUT, EXIT_BUSY, EXIT_RUNNING = 0, 1, 2, 3, 10
# 每条命令最多等多久就返回（秒）。刚提交那一次只等 15 秒，让「已开始」早点报出去
WAIT_SECONDS = max(15, int(os.environ.get("PATENTMAX_WAIT_SECONDS") or 30))
FIRST_WAIT_SECONDS = min(15, WAIT_SECONDS)
POLL_SECONDS = 10

ME = os.path.basename(__file__)


def cache_root():
    return os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")


# ─────────────────────── 输出 ───────────────────────

def emit(payload, code=EXIT_DONE):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def die(message, code=EXIT_ERROR, **extra):
    """出错：message 是给用户看的中文说明，AI 原样转述，不猜原因、不自己换写法重试。"""
    payload = {"error": True, "message": message}
    payload.update(extra)
    emit(payload, code)


def say(line):
    """进度行打到 stdout（不用 stderr：PowerShell 会把 stderr 当成报错显示）。"""
    print(line, flush=True)


def clock(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60}分{seconds % 60:02d}秒" if seconds >= 60 else f"{seconds}秒"


# ─────────────────────── 免费试用密钥 ───────────────────────
#
# 免密钥版（TRIAL_SOURCE 非空）：没设 PATENTMAX_API_KEY 时，第一次调用自动领一把免费试用密钥（不用注册），
# 存在 ~/.patentmax/ 下，之后接着用。规则由服务端定：每把 ¥5、30 天有效、只开通这个 Skill 用到的功能。
# 设了 PATENTMAX_API_KEY 就一律用它，不会去领试用。
# 密钥版（TRIAL_SOURCE 为空）：必须设 PATENTMAX_API_KEY，不领试用。
TRIAL_SOURCE = "design-image-search"
TRIAL_GROUP = "image-search"
TRIAL_REGISTER_URL = "https://api.ip930.com/features/api-platform"
KEY_FROM_TRIAL = False


def _trial_key_path():
    return os.path.join(cache_root(), f"trial-key-{TRIAL_GROUP}.json")


def _load_trial_key():
    try:
        with open(_trial_key_path(), encoding="utf-8") as fh:
            saved = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(saved, dict) or saved.get("base_url") != BASE_URL:
        return None
    expires = str(saved.get("expires_at") or "")
    # ISO 时间同为 UTC，可直接按字符串比
    if expires and expires <= time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()):
        return None
    return saved.get("api_key") or None


def _server_error(detail):
    """取服务端返回的 error.code / error.message。"""
    try:
        body = json.loads(detail)
    except ValueError:
        return "", ""
    error = body.get("error") if isinstance(body, dict) else None
    if not isinstance(error, dict):
        return "", ""
    return str(error.get("code") or ""), str(error.get("message") or "")


def _claim_trial_key():
    url = f"{BASE_URL}/api/v1/trial-keys"
    data = json.dumps({"source": TRIAL_SOURCE}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        _, message = _server_error(exc.read().decode("utf-8", "replace"))
        die(message or f"领取免费试用失败（HTTP {exc.code}）。可以注册 PatentMax 创建正式密钥：{TRIAL_REGISTER_URL}",
            free_trial=True)
    except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as exc:
        die(f"领取免费试用失败，网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试。",
            free_trial=True)
    data = payload.get("data") if isinstance(payload, dict) else None
    key = data.get("api_key") if isinstance(data, dict) else None
    if not key:
        die("领取免费试用失败：服务端没有返回密钥，请稍后重试。", free_trial=True)
    path = _trial_key_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({
                "api_key": key,
                "expires_at": data.get("expires_at"),
                "spending_limit_yuan": data.get("spending_limit_yuan"),
                "source": TRIAL_SOURCE,
                "base_url": BASE_URL,
            }, fh, ensure_ascii=False, indent=2)
        os.chmod(path, 0o600)
    except OSError:
        pass  # 存不下就只用这一次，下次再领
    say(f"[PatentMax] 已自动领取免费试用：{data.get('note') or ''}")
    return key


def ensure_api_key():
    """有 PATENTMAX_API_KEY 用它；没有就用本地存的试用密钥，再没有就领一把。"""
    global API_KEY, KEY_FROM_TRIAL
    if API_KEY:
        return API_KEY
    if not TRIAL_SOURCE:
        die("还没有设置 PatentMax 密钥。到 https://api.ip930.com/features/api-platform 注册（新用户送 ¥50 体验额度）"
            "并创建密钥，设成环境变量 PATENTMAX_API_KEY=pm_live_xxx 后，再运行同一条命令。", EXIT_INPUT)
    API_KEY = _load_trial_key() or _claim_trial_key()
    KEY_FROM_TRIAL = True
    return API_KEY


# ─────────────────────── 请求与报错 ───────────────────────

# 服务端个别报错只给了英文代码，这里翻成用户看得懂的话
CODE_MESSAGES = {
    "DAILY_LIMIT_EXCEEDED": "今天提交的报告数已达上限，北京时间明天 0 点恢复。这次没有提交，未扣费。",
    "CONCURRENT_LIMIT_EXCEEDED": "同时在生成的任务已达上限，等前面的任务完成后再提交。这次没有提交，未扣费。",
    "API_BALANCE_INSUFFICIENT": f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    # 防重复提交的编号冲突：同一份内容之前由同一账户下的另一把密钥提交过，或手动给的编号对应的是别的内容
    "IDEMPOTENCY_KEY_OWNED_BY_DIFFERENT_API_KEY": "这份内容之前用同一账户的另一把密钥提交过。这次没有提交、未扣费。"
                                                  "去 https://api.ip930.com 控制台的调用记录里找原来那份；要重新生成，换个说法补充一句材料再提交。",
    "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST": "这个任务编号已经用于另一份内容。这次没有提交、未扣费。不要手动指定 --idempotency-key，让脚本自动生成即可。",
    "REPORT_NOT_READY": "报告还没有生成完，用 wait 接着等。",
}
HTTP_MESSAGES = {
    400: "图片或检索条件有问题（图片要是 jpg / png、不超过 10MB；外观分类写成 12-11 这样）。这次没有提交，未扣费。",
    401: "密钥无效或已撤销。请到 https://api.ip930.com 控制台重新创建。",
    402: f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    403: "这把密钥没有开通这项功能。",
    404: "找不到这个任务或报告，请确认编号完整。",
    409: "同样的任务已经在生成，这次没有重复提交、没有重复扣费。",
    429: "提交太频繁，请稍后再试。这次没有提交，未扣费。",
}


def _has_cjk(text):
    return bool(re.search(r"[一-鿿]", text or ""))


def _open(path, method="GET", body=None, headers=None):
    ensure_api_key()
    url = path if path.startswith("http") else f"{BASE_URL}{path}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    return urllib.request.urlopen(req, timeout=TIMEOUT)


def request(path, method="GET", body=None, headers=None, raw=False):
    try:
        with _open(path, method, body, headers) as response:
            payload = response.read()
            return payload if raw else json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:600]
        code, message = _server_error(detail)
        if KEY_FROM_TRIAL and exc.code == 401:
            # 试用密钥过期或被停用：清掉本地缓存，下次运行自动领新的
            try:
                os.remove(_trial_key_path())
            except OSError:
                pass
            die("免费试用已过期或失效。重新运行同一条命令会自动领取新的试用；"
                f"也可以注册 PatentMax 换正式密钥：{TRIAL_REGISTER_URL}", free_trial=True)
        if KEY_FROM_TRIAL and "免费试用" in (message or ""):
            # 服务端对试用账户余额用完回 409 + 引导注册的话；不能当成「忙，稍后重试」
            die(message + TRIAL_CONTINUE, **trial_end_extra())
        # 优先用服务端的中文说明（里面写着下一步怎么办）；只有英文代码时用本地翻译
        text = (message if _has_cjk(message) else "") \
            or CODE_MESSAGES.get(message) or CODE_MESSAGES.get(code) \
            or HTTP_MESSAGES.get(exc.code) \
            or f"PatentMax 服务暂时不可用（HTTP {exc.code}），请稍后重试。"
        extra = {"free_trial": True} if "免费试用" in text else {}
        busy = exc.code == 409 and not code.startswith("IDEMPOTENCY_") and not message.startswith("IDEMPOTENCY_")
        die(text, EXIT_BUSY if busy else EXIT_ERROR, http_status=exc.code, **extra)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        die(f"网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试；"
            "已提交的任务不受影响，稍后用 wait 接着看。")
    except json.JSONDecodeError:
        die("PatentMax 返回的内容不完整，请稍后重试。")


def try_download(path):
    """下载文件；失败不退出，返回 None（报告受限时可能没有 Word）。"""
    try:
        with _open(path) as response:
            return response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionError):
        return None


def unwrap(payload):
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def fingerprint(body):
    """同样的内容 + 同一把密钥 → 同一个编号：重跑拿回原任务，不重复扣费。

    带上密钥本身的指纹（不是密钥原文）：同一账户换了密钥再交同样的内容时，服务端会因为「编号属于另一把密钥」拒绝，
    用户卡在那里拿不到任务（2026-10-14 实测）。按密钥区分后，换密钥就是一个新任务。
    """
    ensure_api_key()
    raw = json.dumps(body, ensure_ascii=False, sort_keys=True) + "|" + hashlib.sha256(API_KEY.encode("utf-8")).hexdigest()[:12]
    return "pm-img-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def read_docx(path, label):
    """标准库取 .docx 正文（它就是个 zip，正文在 word/document.xml）。写好的交底书、初稿可以直接拿来用。"""
    import zipfile
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8", "replace")
    except (zipfile.BadZipFile, KeyError, OSError) as exc:
        die(f"读不了这个 Word 文件：{path}（{exc}）。只支持 .docx，老的 .doc 请先另存为 .docx。", EXIT_INPUT)
    xml = re.sub(r"</w:tc>", " | ", xml)
    xml = re.sub(r"</w:p>|</w:tr>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    xml = re.sub(r"<w:br[^>]*/>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    for entity, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'"), ("&amp;", "&")):
        text = text.replace(entity, char)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        die(f"{label}文件是空的：{path}", EXIT_INPUT)
    return text


def read_text_file(path, label):
    if not os.path.isfile(path):
        die(f"找不到{label}文件：{path}", EXIT_INPUT)
    if path.lower().endswith(".docx"):
        return read_docx(path, label)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read().strip()
    except UnicodeDecodeError:
        die(f"{label}文件不是 UTF-8 文本：{path}。只支持 .md / .txt / .docx。", EXIT_INPUT)
    except OSError as exc:
        die(f"读不到{label}文件：{path}（{exc}）", EXIT_INPUT)
    if not text:
        die(f"{label}文件是空的：{path}", EXIT_INPUT)
    return text


def split_list(value):
    return [x.strip() for x in value.replace("，", ",").replace("、", ",").split(",") if x.strip()] if value else []


# ─────────────────────── 本地任务记录 ───────────────────────
#
# 记下每个任务从哪个目录提交、几点提交，wait 完成时把 Word 存回那个目录，
# 「已用时」也从提交时刻算起，命令断了再接上不会从 0 重新数。

def _task_path(operation):
    return os.path.join(cache_root(), "tasks", re.sub(r"[^\w.-]", "_", operation) + ".json")


def save_task(operation, **fields):
    record = load_task(operation)
    record.update({k: v for k, v in fields.items() if v is not None})
    try:
        os.makedirs(os.path.dirname(_task_path(operation)), exist_ok=True)
        with open(_task_path(operation), "w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return record


def load_task(operation):
    try:
        with open(_task_path(operation), encoding="utf-8") as fh:
            saved = json.load(fh)
            return saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        return {}


# ─────────────────────── 本技能的输入 ───────────────────────

import base64

QUALITY_HINT = {
    "qualified": "检索完成。",
    "qualified_degraded": "检索完成，但为了找到结果放宽过条件，排在后面的相似度一般，要保守看。",
    "review_required": "结果需要人工复核。",
}
DEMO_IMAGE_URL = "https://api.ip930.com/demo/image-search-demo.png"
DEMO_BRAND = "安克"
MAX_IMAGE_BYTES = 10 * 1024 * 1024


def _image_source(args):
    """图片三选一：本地文件 / 网址 / 识别时拿到的 photo_id；--demo 用技能自带的演示图。"""
    if getattr(args, "demo", False):
        return {"image_url": DEMO_IMAGE_URL}
    if getattr(args, "photo_id", None):
        return {"photo_id": args.photo_id}
    if getattr(args, "image", None):
        path = os.path.abspath(os.path.expanduser(args.image))
        if not os.path.isfile(path):
            die(f"找不到图片文件：{path}。请给图片的完整路径。", EXIT_INPUT)
        if os.path.getsize(path) > MAX_IMAGE_BYTES:
            die("图片不能超过 10MB，请压缩后再试。", EXIT_INPUT)
        with open(path, "rb") as handle:
            return {"image_base64": base64.b64encode(handle.read()).decode("ascii")}
    if getattr(args, "image_url", None):
        return {"image_url": args.image_url}
    die("请给一张产品图片：--image <本地图片路径> 或 --image-url <图片网址>；想先试试，用 --demo（技能自带的演示图）。", EXIT_INPUT)


def do_identify(args):
    """第一步：识别照片（免费，每天 30 次）。返回 photo_id 和识别出的产品名称、外观分类、品牌。"""
    body = _image_source(args)
    if args.hint:
        body["hint"] = args.hint
    data = unwrap(request("/api/v1/image-search/identify", method="POST", body=body)) or {}
    emit({
        "photo_id": data.get("photo_id"),
        "is_product": data.get("is_product"),
        "product_name": data.get("product_name"),
        "synonyms": data.get("synonyms"),
        "loc_suggestions": data.get("loc_suggestions"),
        "brand": data.get("brand"),
        "appearance": data.get("appearance"),
        "confidence": data.get("confidence"),
        "next": "把识别结果（产品名称、外观分类、品牌）用一条消息给用户确认或修改；确认后用 create --photo-id <photo_id> --yes 检索"
                "（成功 ¥1，没找到、失败不扣费）。识别不出产品（is_product=false）的，请用户换一张清楚的产品照片。",
    })


def do_create(args):
    if not args.yes:
        die("以图搜图检索成功一次 ¥1（没找到、失败、取消都不扣费）。取得用户同意后加 --yes 再运行；"
            "用户说「用演示图试一下」就视为同意。", EXIT_INPUT)
    data = _image_source(args)
    if args.product_name:
        data["product_name"] = args.product_name.strip()[:40]
    if args.synonyms:
        data["synonyms"] = [s[:40] for s in split_list(args.synonyms)][:12]
    if args.loc:
        codes = split_list(args.loc)[:3]
        bad = [c for c in codes if not re.match(r"^\d{2}-\d{2}$", c)]
        if bad:
            die(f"外观分类编号要写成 12-11 这样：{', '.join(bad)}", EXIT_INPUT)
        data["loc_codes"] = codes
    if args.brand:
        data["brand"] = args.brand.strip()[:40]
    elif getattr(args, "demo", False):
        data["brand"] = DEMO_BRAND  # 演示图是安克的储能电源：带上品牌，第 1 名就是它本身，同品牌、第三方一起演示
    if args.applicants:
        data["applicants"] = [a[:40] for a in split_list(args.applicants)][:8]
    if args.hint:
        data["hint"] = args.hint.strip()[:60]
    if args.us_kr or args.jp_tw:
        data["scope"] = {"us_kr": bool(args.us_kr), "jp_tw": bool(args.jp_tw)}
    submit({"report_type": REPORT_TYPE, "input": data}, args, args.product_name or "以图搜图")


def _items(items, limit):
    keys = ("rank", "publication_number", "title", "applicant", "application_date", "legal_status", "loc", "reason", "same_brand")
    return [{k: item.get(k) for k in keys} for item in (items or [])[:limit]]


def _download_figures(results, top, folder):
    """把结果里前 N 名的附图下载到 folder（只给结果里出现过的专利）；下不到的记下来，不中断。"""
    os.makedirs(folder, exist_ok=True)
    saved, missing = [], []
    for region in ("cn", "us", "kr"):
        for item in (results.get(region) or [])[:top]:
            number, path = item.get("publication_number"), item.get("figure_path")
            data = try_download(path) if path else None
            if not data:
                missing.append(number)
                continue
            target = os.path.join(folder, f"{number}.jpg")
            with open(target, "wb") as handle:
                handle.write(data)
            saved.append(target)
    return {"saved": len(saved), "folder": folder, "missing": missing}


def summarize(payload):
    """要讲的：检索条件、中国前 10 名（按外观相似度）、美韩 / 日台（勾了才有）。完整结果另存文件。
    2026-10-21：完成时顺手把前 10 名的附图下载到 附图/，AI 不用等用户开口再去取。"""
    result = payload.get("result") or {}
    results = result.get("results") or {}
    text = result.get("text_results") or {}
    conditions = result.get("conditions") or {}
    figures = _download_figures(results, 10, os.path.abspath("附图"))
    return {
        "figures": figures,
        "title": conditions.get("product_name") or "以图搜图",
        "conditions": conditions,
        "searched": result.get("summary"),
        "cn_total": len(results.get("cn") or []),
        "cn_top10": _items(results.get("cn"), 10),
        "us_top5": _items(results.get("us"), 5),
        "kr_top5": _items(results.get("kr"), 5),
        "jp_text_top5": _items(text.get("jp"), 5),
        "tw_text_top5": _items(text.get("tw"), 5),
        "next": "附图已经下载到 figures.folder：**直接**用 Read 看用户原图和每张附图，按 SKILL.md 第 4 步写对比表和图集，不要等用户开口要附图。"
                "Word 报告这一项不适用，忽略 docx_note。",
    }


def do_figures(args):
    """重新下载附图（wait 完成时已自动下载前 10 名；要更多或换目录时用）。"""
    payload = unwrap(request(f"/api/v1/reports/{urllib.parse.quote(args.report_id)}")) or {}
    results = (payload.get("result") or {}).get("results") or {}
    out = _download_figures(results, args.top, os.path.abspath(args.out_dir or "附图"))
    out["next"] = "用 Write 写 外观对比图集.html：第一格放用户的原图，后面每格放一件专利的附图、公开号、申请人、你的判断。"
    emit(out)


# ─────────────────────────── 等待 ───────────────────────────

STATUS_TEXT = {"queued": "排队中", "accepting": "排队中", "running": "生成中"}
DONE_TEXT = {"succeeded": "已完成", "failed": "没有完成，预扣的费用已全额退回", "cancelled": "已取消，预扣的费用已全额退回"}


# 给人看的进度：和工作台一样一直往上走、带一位小数（2026-10-22，与服务端 MCP 的 report-progress-display.ts 同一套算法）。
# 服务端的真值很粗：想法升级、竞争分析、技术路线、OA 按「完成了几步」折算，会一下跳到完成、十分钟停在 75%，甚至倒退；
# 查新、交底书两次真值之间也是停着的。这里只改展示：真值之间按每格实测耗时往下一格爬（差 0.4 停住），只增不减，完成才 100。
_LADDERS = {
    "novelty": [(20, 160), (32, 176), (48, 56), (62, 16), (84, 623), (94, 67), (100, 20)],
    "technical_disclosure": [(12, 40), (15, 9), (46, 105), (96, 170), (100, 13)],
}
# 真值只是「完成了几步」的报告：按已用时间走曲线，线上实测中位用时处约 80%，95% 封顶等完成
_MEDIAN_SECONDS = {"idea_upgrade": 153, "patent_intelligence": 779, "roadmap_layout": 1179, "oa_response": 466, "image_search": 15}


def shown_progress(operation, data):
    status = (data.get("status") or "").lower()
    raw = data.get("progress")
    raw = float(raw) if isinstance(raw, (int, float)) else 0.0
    now = time.time()
    record = load_task(operation)
    state = record.get("shown_progress") or {}
    if not state:
        state = {"shown": 0.0, "raw": raw, "raw_since": now, "active": max(0.0, now - started_at_of(operation, data)),
                 "last_seen": now, "last_status": status}
    else:
        if state.get("last_status") in ("running", "accepting"):
            state["active"] = state.get("active", 0) + now - state.get("last_seen", now)
        if raw != state.get("raw"):
            state["raw"], state["raw_since"] = raw, now
        state["last_seen"], state["last_status"] = now, status
    if status == "running":
        report_type = data.get("report_type") or REPORT_TYPE
        ladder = _LADDERS.get(report_type)
        if ladder:
            value = raw
            nxt = next(((th, secs) for th, secs in ladder if th > raw), None)
            if nxt:
                crept = raw + (nxt[0] - raw) * (1 - math.exp(-(now - state["raw_since"]) / (max(nxt[1], 1) / 3)))
                value = max(raw, min(crept, nxt[0] - 0.4))
        else:
            tau = _MEDIAN_SECONDS.get(report_type, 600) / math.log(95 / 15)
            value = 95 * (1 - math.exp(-state["active"] / tau))
            if report_type == "image_search":
                value = max(value, raw)
        state["shown"] = min(99.9, max(state.get("shown", 0.0), value))
    save_task(operation, shown_progress=state)
    return round(state["shown"], 1)


def progress_line(data, started_at, operation=None):
    """「[进度 X.X%] 阶段，已用时 N」。百分比是平滑后的展示值（见 shown_progress），排队中不报百分比。"""
    status = (data.get("status") or "").lower()
    if status in DONE_TEXT:
        return f"[进度] {DONE_TEXT[status]}"
    stage = str(data.get("stage") or "")
    percent = data.get("progress")
    elapsed = clock(time.time() - started_at)
    label = STATUS_TEXT.get(status, status or "处理中")
    detailed = _has_cjk(stage) and stage not in ("正在接收任务",)
    if operation and status == "running":
        return f"[进度 {shown_progress(operation, data):.1f}%] {stage if detailed else label}，已用时 {elapsed}"
    if detailed and isinstance(percent, (int, float)) and 0 < percent < 100:
        return f"[进度 {int(percent)}%] {stage}，已用时 {elapsed}"
    if status in ("queued", "accepting"):
        return f"[进度] 排队中，已等待 {elapsed}"
    return f"[进度] {stage if detailed else label}，已用时 {elapsed}"


def started_at_of(operation, data):
    record = load_task(operation)
    if record.get("started_at"):
        return float(record["started_at"])
    created = str(data.get("created_at") or "")
    try:
        return calendar.timegm(time.strptime(created[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return time.time()


def wait_for(operation, seconds, out_dir=None):
    """最多等 seconds 秒：完成就交付（退出码 0），还没完就报进度（退出码 10）。"""
    deadline = time.time() + seconds
    last_stage = None
    while True:
        data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(operation)}"))
        status = (data.get("status") or "").lower()
        if status == "succeeded":
            emit(deliver(operation, data, out_dir), EXIT_DONE)
        if status in ("failed", "cancelled"):
            error = data.get("error") or {}
            message = error.get("message") if _has_cjk(error.get("message")) else ""
            die(message or ("任务已取消。" if status == "cancelled" else f"{REPORT_NAME}没有生成成功。"),
                EXIT_ERROR, operation_id=operation, status=status,
                refund="预扣的费用已全额退回。")
        line = progress_line(data, started_at_of(operation, data), operation)
        stage = str(data.get("stage") or status)  # 百分比每次都变，按阶段名判断换没换阶段
        ending = time.time() + POLL_SECONDS > deadline
        # 一条命令只在返回前报一行最新进度；中途换了阶段再多报一行。不要每次轮询都刷一行
        if ending or (last_stage is not None and stage != last_stage):
            say(line)
        last_stage = stage
        if ending:
            emit({
                "status": "running",
                "operation_id": operation,
                "next": f"把上面的进度告诉用户，然后运行：python {ME} wait --operation-id {operation}",
            }, EXIT_RUNNING)
        time.sleep(POLL_SECONDS)


def safe_name(text):
    return re.sub(r'[\\/:*?"<>|\s]+', "", str(text))[:40] or REPORT_NAME


def deliver(operation, data, out_dir=None):
    """完成：Word 报告自动存到提交时的目录；完整结果存成文件，只返回要讲的几项。"""
    report_id = data.get("report_id")
    record = load_task(operation)
    target = out_dir or record.get("out_dir") or os.getcwd()
    payload = unwrap(request(f"/api/v1/reports/{urllib.parse.quote(report_id)}")) or {}
    quality = payload.get("quality_status") or data.get("quality_status")
    out = {
        "status": "succeeded",
        "operation_id": operation,
        "report_id": report_id,
        "elapsed": clock(time.time() - started_at_of(operation, data)),
        "amount_charged_yuan": data.get("amount_charged_yuan"),
        "quality_status": quality,
        "quality_hint": QUALITY_HINT.get(quality, ""),
    }
    summary = summarize(payload)
    stem = safe_name(summary.get("title") or record.get("title") or data.get("title") or REPORT_NAME)

    os.makedirs(target, exist_ok=True)
    files = {}
    docx = try_download(f"/api/v1/reports/{urllib.parse.quote(report_id)}/files/report.docx")
    if docx:
        path = os.path.abspath(os.path.join(target, f"{REPORT_NAME}_{stem}.docx"))
        with open(path, "wb") as handle:
            handle.write(docx)
        files[REPORT_NAME] = path
    else:
        out["docx_note"] = "这次没有生成 Word 报告，结论以下面的摘要和完整结果为准。"
    full = os.path.abspath(os.path.join(target, f"{REPORT_NAME}_{stem}_结果.json"))
    with open(full, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    files["完整结果"] = full
    out["files"] = files
    out["summary"] = summary
    return out


# ─────────────────────────── 子命令 ───────────────────────────

def submit(body, args, title=None):
    key = args.idempotency_key or fingerprint(body)
    created = unwrap(request("/api/v1/reports", method="POST", body=body,
                             headers={"Idempotency-Key": key}))
    operation = created.get("operation_id")
    if not operation:
        die("PatentMax 没有返回任务编号，请稍后重试。")
    record = load_task(operation)
    resumed = bool(record)
    save_task(operation, started_at=record.get("started_at") or time.time(),
              out_dir=os.path.abspath(args.out_dir or os.getcwd()), title=title or created.get("title"))
    if not resumed:
        say(f"[进度] 已开始生成{REPORT_NAME}（预计费用 ¥{created.get('price_yuan')}）")
    else:
        say("[进度] 同样的内容已经提交过，这次没有重复提交、没有重复扣费，接着看原来的任务")
    if args.wait:
        # 老用法：一直等到出结果。宿主前台跑命令时用户全程看不到进度，SKILL.md 里不再用
        wait_for(operation, args.timeout, args.out_dir)
    wait_for(operation, FIRST_WAIT_SECONDS, args.out_dir)


def do_wait(args):
    wait_for(args.operation_id, WAIT_SECONDS, args.out_dir)


def do_status(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}"))
    emit({
        "operation_id": args.operation_id,
        "report_id": data.get("report_id"),
        "status": (data.get("status") or "").lower(),
        "progress": progress_line(data, started_at_of(args.operation_id, data), args.operation_id),
    })


def do_download(args):
    payload = request(f"/api/v1/reports/{urllib.parse.quote(args.report_id)}/files/report.docx", raw=True)
    out = args.out or f"{REPORT_NAME}.docx"
    with open(out, "wb") as handle:
        handle.write(payload)
    emit({"saved": os.path.abspath(out), "bytes": len(payload)})


def do_cancel(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/cancel",
                          method="POST"))
    emit({"operation_id": args.operation_id, "status": data.get("status"),
          "refund": "取消后预扣的费用全额退回。"})


def main():
    parser = argparse.ArgumentParser(description="PatentMax 外观专利以图搜图")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="提交外观专利以图搜图任务（约 15 秒后返回，之后用 wait 接着等）")
    p.add_argument("--image", default=None, help="本地产品图片路径（jpg/png，≤10MB）")
    p.add_argument("--image-url", dest="image_url", default=None, help="公网图片网址")
    p.add_argument("--photo-id", dest="photo_id", default=None, help="identify 返回的 photo_id（推荐：识别确认后再检索）")
    p.add_argument("--demo", action="store_true", help="用技能自带的演示图（安克的一款便携储能电源外观图，检索时自动带品牌「安克」）")
    p.add_argument("--hint", default=None, help="可选：一句提示，例如「这是一款电动滑板车」")
    p.add_argument("--product-name", dest="product_name", default=None, help="产品名称（不填按识别结果）")
    p.add_argument("--synonyms", default=None, help="产品的其他叫法，逗号分隔")
    p.add_argument("--loc", default=None, help="外观分类编号，逗号分隔，最多 3 个，形如 12-11（不填按识别结果）")
    p.add_argument("--brand", default=None, help="品牌（可选）")
    p.add_argument("--applicants", default=None, help="品牌对应的申请人全称，逗号分隔（可选）")
    p.add_argument("--us-kr", dest="us_kr", action="store_true", help="同时查美国、韩国（按图比对）")
    p.add_argument("--jp-tw", dest="jp_tw", action="store_true", help="同时查日本、台湾（只按文字）")
    p.add_argument("--out-dir", dest="out_dir", default=None, help="完成后 Word 存到哪个目录，默认当前目录")
    p.add_argument("--idempotency-key", dest="idempotency_key", default=None, help="幂等键，默认按请求内容自动生成")
    p.add_argument("--wait", action="store_true", help="（旧用法）一直等到出结果，不推荐")
    p.add_argument("--timeout", type=int, default=5400, help="配合 --wait 的等待上限（秒）")
    p.add_argument("--quiet", action="store_true", help=argparse.SUPPRESS)  # 旧参数，保留以兼容
    p.add_argument("--yes", action="store_true", help="确认扣费")
    p.set_defaults(func=do_create)

    p = sub.add_parser("wait", help="接着等：最多 30 秒，完成就自动下载 Word")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.set_defaults(func=do_wait)

    p = sub.add_parser("identify", help="第一步：识别照片（免费，每天 30 次），返回 photo_id 和识别结果")
    p.add_argument("--image", default=None, help="本地产品图片路径（jpg/png，≤10MB）")
    p.add_argument("--image-url", dest="image_url", default=None, help="公网图片网址")
    p.add_argument("--photo-id", dest="photo_id", default=None, help="identify 返回的 photo_id（推荐：识别确认后再检索）")
    p.add_argument("--demo", action="store_true", help="用技能自带的演示图（安克的一款便携储能电源外观图，检索时自动带品牌「安克」）")
    p.add_argument("--hint", default=None, help="可选：一句提示，例如「这是一款电动滑板车」")
    p.set_defaults(func=do_identify)

    p = sub.add_parser("figures", help="下载结果里前 N 名的附图到 附图/ 文件夹")
    p.add_argument("--report-id", dest="report_id", required=True)
    p.add_argument("--top", type=int, default=10, help="每个地区前几名，默认 10")
    p.add_argument("--out-dir", dest="out_dir", default=None, help="默认 附图/")
    p.set_defaults(func=do_figures)

    p = sub.add_parser("status", help="只查一次任务状态")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_status)

    p = sub.add_parser("download", help="重新下载 Word 报告（wait 完成时已自动下载过）")
    p.add_argument("--report-id", dest="report_id", required=True)
    p.add_argument("--out", default=None)
    p.set_defaults(func=do_download)

    p = sub.add_parser("cancel", help="取消任务，预扣费用全额退回")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
