"""百炼®标书开放 API 轻客户端（thin client）。

封装「提交 → 轮询 → 取结果」异步模型，零第三方依赖（仅标准库）。
凭证固定通过 skill 根目录 config.json 传入；可选环境变量仅用于首次落盘或输出路径：
  ZCM_APP_KEY  Api Key（形如 bk_live_xxxxx，首次使用时会写入 skill 根目录 config.json）
  ZCM_BASE     Base URL，默认生产 https://biaoshu.zhiliaobiaoxun.com/api/open/v1
  ZCM_OUTPUT_DIR  成品标书 .docx 存放目录；未设时默认 skill 同级的 biaoshu-writer-build-files/

凭证读取优先级：环境变量 > skill 内 config.json；不读旧 ~/.zcm/ 目录，不允许 ZCM_CONFIG 重定向。
config.json 权限 600，含真实 Key，**勿上传发布包**（发布包不含配置文件；模板结构见 references/usage.md）。
经环境变量首次提供凭证时自动落盘到 config.json；也可用 login 显式保存、logout 清除。
成品存放目录优先级：generate -o 显式路径 > ZCM_OUTPUT_DIR > config.json 的 output_dir > 默认 biaoshu-writer-build-files。

子命令：
  login      --app-key ..  保存凭证到 skill 内 config.json（输一次，下次免输）
  register   [--phone ..]  skill 内手机号注册/登录，换取并保存 Api Key
  logout                   删除 config.json 里的凭证
  me                                查连通性与可用字数
  version-check                     手动检查 skill 最新版本（后台排查用）
  interpret  <file|https-url>       智能解读招标文件 → 打印摘要并生成解读报告（--full-json 可看完整结果）
  packages   <project_id>           抽取分包 → 打印 packages JSON（供用户挑选）
  generate   <project_id> [opts]    用户确认包和页数后生成成品标书，WorkBuddy/SkillHub 必须配合 --no-wait + progress-stream
  compliance <project_id> <f...>    合规审查投标文件 → 打印完整合规结果
  duplicate  <f...>                 标书查重：2-3 份投标文件雷同/相似风险检查
  report     --job <id> | --in f    把解读/合规/查重结果渲染成 HTML/Word 报告
  experience --type .. --stage ..   把本阶段经验总结回传平台沉淀（用户同意后）
  feedback   --category .. ...      上报使用问题（用户同意后；不含文件与个人信息）
  knowledge-base [category]         按类别查询知识库（排除历史标书库 / 标书模板库）

interpret / compliance / duplicate 可加 --report html|docx|both 在取结果后直接出报告。
  job        <job_id>               查单个任务状态（不轮询）
  download-url <job_id>             获取成品标书短时下载链接
  result     <job_id> [-o file]     取任务结果 / -o 下载成品
  cancel     <job_id>               取消任务

generate 必须显式确认包处理方式和页数，并默认要求 --no-wait 后接 progress-stream。
其他提交类子命令（interpret/packages/compliance/duplicate）默认自动轮询到终态，加 --no-wait 只提交并打印 job_id。
"""
import hashlib
import json
import os
import sys

from zcm_lib.parser import build_parser as build_cli_parser
from zcm_lib.http_client import (
    handle_http_error as _handle_http_error_impl,
    request_json as _request_json_impl,
)
from zcm_lib.jobs import (
    cmd_cancel as _cmd_cancel_impl,
    cmd_download_url as _cmd_download_url_impl,
    cmd_job as _cmd_job_impl,
    cmd_result as _cmd_result_impl,
    download_result as _download_result_impl,
    get_download_url as _get_download_url_impl,
    poll_job as _poll_job_impl,
    print_download_link as _print_download_link_impl,
    progress_stream as _progress_stream_impl,
)
from zcm_lib.reporting import (
    cmd_report as _cmd_report_impl,
    maybe_report as _maybe_report_impl,
    platform_reminder as _platform_reminder_impl,
    report_balance as _report_balance_impl,
    zh_risk,
)
from zcm_lib.progress import (
    format_bytes as _format_bytes,
    format_progress_line,
    format_seconds as _format_seconds,
)
from zcm_lib.files import (
    MAX_BID_MB,
    MAX_DUP_TOTAL_MB,
    MAX_TENDER_MB,
    check_size as _check_size,
    check_total_size as _check_total_size,
    download_to_local,
    encode_multipart,
    is_url,
)
from zcm_lib.billing import (
    estimate_generation_words as _estimate_generation_words,
    generation_max_pages as _generation_max_pages,
    generation_pages as _generation_pages,
    shortage_detail as _shortage_detail,
)
from zcm_lib.storage import (
    creds_path,
    load_creds_file,
    output_dir,
    recall_tender,
    remember_tender,
    save_creds_file,
)
from zcm_lib.versioning import maybe_check_update

DEFAULT_BASE = "https://biaoshu.zhiliaobiaoxun.com/api/open/v1"

# skill 版本（单一事实来源）。适配的后端 API 版本与契约快照见 references/api.md 顶部。
SKILL_VERSION = "3.1.2"
API_TARGET = "/api/open/v1"
CONTRACT_SNAPSHOT = "2026-09-07"

# 渠道码：主线留空（不带渠道）；发布各渠道副本时按平台 excel 注入（如 SkillHub 主基线注入 "s111"）。
# 非空时：免费试用/注册请求体带 channel（后端落库标记来源），官网链接追加 ?ch=。
CHANNEL = ""
SIGNUP_URL = "https://biaoshu.zhiliaobiaoxun.com/" + (f"?ch={CHANNEL}" if CHANNEL else "")

# 文档第 6 节错误码 → 友好提示
ERROR_HINTS = {
    "missing_credentials": "缺少鉴权头：请设置环境变量 ZCM_APP_KEY。",
    "invalid_credentials": f"Api Key 不正确：核对凭证，或到官网 {SIGNUP_URL} 左侧菜单『Skill 接入 → 获取 Api Key』重置 Key（重置后旧 Key 立即失效）。",
    "account_disabled": "凭证或用户已被停用，请联系百炼®标书管理员。",
    "insufficient_points": "可用字数不足：请到官网购买会员或字数包后重试。",
    "insufficient_balance": "可用字数不足：请先购买会员或字数包，或绑定手机号领取赠送字数后重试。",
    "not_found": "404：多为开放 API 总开关未开（整层 404），请联系超级管理员在『系统设置』开启；或句柄不存在。",
    "job_not_found": "任务句柄不存在或非本人，请核对 job_id。",
    "project_not_found": "project 不存在或非本人，请核对 project_id（由智能解读产出）。",
    "result_expired": "结果已过期（默认约 7 天 TTL），需重新生成。",
    "invalid_job_state": "任务状态不允许此操作：任务未成功就取结果 / 未解读就生成 / 未抽包就 generate。",
    "validation_error": "入参校验失败：文件缺失或类型不支持 / file_url 非 https 或指向内网 / 缺 package_ids 等。",
    "rate_limited": "触发限流（60 req/min）：稍后退避重试（参考 Retry-After）。",
    "too_many_concurrent_jobs": "并发任务超限（≤3）：等已有任务结束再提交。",
    "daily_quota_exceeded": "今日沉淀已达上限（每天最多 20 条），明天可以继续。",
    "internal_error": "服务端异常：稍后重试或反馈百炼®标书。",
    "fingerprint_required": "设备特征采集失败，无法自动试用：请改用官网获取 Api Key（官网注册登录后，在『Skill 接入 → 获取 Api Key』查看，把 Key 粘贴给我保存即可）。",
    "trial_limit_exceeded": "当前网络已开通过试用账号（每个网络/设备限 1 个）：请改用官网获取 Api Key（官网注册登录后，在『Skill 接入 → 获取 Api Key』查看，把 Key 粘贴给我保存即可）。",
    "skill_trial_registration_disabled": f"需要先配置百炼标书 Api Key 才能继续使用。你可以登录官网 {SIGNUP_URL} 注册并获取 Api Key；也可以直接把手机号发给我，由我帮你完成注册和配置。",
}

REGISTER_GUIDE = f"""\
还没配置 Api Key —— 这是用百炼®标书写作助手出解读/标书/合规的唯一开关。
好消息：新用户零输入就能免费试用（赠 50,000 字），开通后这份文件马上就能出解读。
拿 Key 有两种方式，**均由助手代跑，用户无需敲任何命令**（拿到后自动保存，下次免输）：

  A) 免费试用（零输入，最省事，赠 50,000 字）：
       征得用户同意后，助手直接开通（自动采集设备特征，Api Key 自动保存）；绑定手机号可升级为注册账号并继续补发 50,000 字，Key 不变。

  B) 官网获取 Api Key（可用字数不足、或无法自动试用时）：
       打开官网 {SIGNUP_URL} 用手机号 + 短信验证码注册并登录（手机号注册赠 5 万字），
       点左侧菜单『Skill 接入 → 获取 Api Key』，在弹出面板中查看/复制 Api Key
       （首次打开自动生成，形如 bk_live_xxxxx，重置后旧 Key 立即失效）。
       用户把 Key 直接粘贴到对话里即可，例如：
       「我的 Api Key 是 bk_live_xxxxx，帮我保存一下」（助手代为保存，下次免输）。
"""

BALANCE_GUIDE = """\
可用字数不足，请选择：
  1) 绑定手机号升级为注册账号并领取赠送字数（skill 内，手机号+验证码，Api Key 不变）
  2) 前往官网购买会员或字数包，或粘贴新 Api Key 到此处
  q) 退出
"""


def die(msg, code=1):
    print(msg, file=sys.stderr, flush=True)
    sys.exit(code)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def get_creds():
    """返回 Api Key。未配置时引导『自动试用 / 官网拿 Key 粘贴』。"""
    stored = load_creds_file()
    env_key = os.environ.get("ZCM_APP_KEY", "").strip()
    app_key = env_key or str(stored.get("app_key", "")).strip()
    if not app_key:
        return _guide_missing_credentials()
    if env_key and env_key != stored.get("app_key"):
        save_creds_file(dict(stored, app_key=env_key))
        log(f"凭证已保存到 {creds_path()}（权限 600），下次无需再输。")
    return app_key


def _guide_missing_credentials():
    """无 Api Key：交互环境二选一（试用 / 粘贴 Key）并返回 Key；
    非交互环境打印获取指引后退出（由 Claude 转达用户，再走 trial / login）。"""
    if not sys.stdin.isatty():
        die(REGISTER_GUIDE, code=2)
    log(REGISTER_GUIDE)
    choice = input("请选择 [1] 免费试用（自动开通）  [2] 已有 Api Key 直接粘贴  [q] 退出：").strip().lower()
    if choice == "1":
        _trial_flow()
        return str(load_creds_file().get("app_key", "")).strip()
    if choice == "2":
        new_key = input("请粘贴 Api Key（形如 bk_live_xxxxx）：").strip()
        if not new_key:
            die("未输入 Api Key，已退出。", code=2)
        save_creds_file(dict(load_creds_file(), app_key=new_key))
        log(f"Api Key 已保存到 {creds_path()}（权限 600）。")
        return new_key
    sys.exit(0)


def _collect_device():
    """采集 6 项设备特征；任一失败置空串，绝不中断。"""
    import getpass
    import platform as _platform
    import socket
    import uuid as _uuid

    def _try(fn):
        try:
            v = fn()
            return str(v).strip() if v else ""
        except Exception:
            return ""

    def _mac():
        node = _uuid.getnode()
        if (node >> 40) & 0x01:   # 组播位=1：随机 MAC，视为采集失败
            return ""
        return hashlib.sha256(str(node).encode("utf-8")).hexdigest()

    return {
        "hostname": _try(socket.gethostname),
        "platform": _try(_platform.system),
        "arch": _try(_platform.machine),
        "username": _try(getpass.getuser),
        "home_path": _try(lambda: os.path.expanduser("~")),
        "mac_hash": _try(_mac),
    }


def _trial_flow():
    """免费试用：设备指纹自动注册 → 拿 Api Key 写入 config.json。幂等：同设备返回原 Key。"""
    body = {"device": _collect_device()}
    if CHANNEL:
        body["channel"] = CHANNEL
    resp = _anon_json("POST", "/trial-accounts", json_body=body)
    key = str(resp.get("app_key", "")).strip()
    if not key:
        die("试用开通失败：接口未返回 Api Key。")
    save_creds_file(dict(load_creds_file(), app_key=key))
    balance = resp.get("available_words", resp.get("wallet_balance", 0))
    if resp.get("is_new"):
        log(f"试用开通成功！当前可用字数：{balance}，Api Key 已保存到 {creds_path()}（权限 600）。")
        log("绑定手机号可升级为注册账号并领取赠送字数（把手机号给我即可在 skill 内绑定，Api Key 不变）。")
    else:
        log(f"本设备已有试用账号，已恢复原 Api Key，当前可用字数：{balance}。")


def _register_flow(phone=None, code=None):
    """skill 内手机号注册/登录：发验证码 → 校验 → 拿 Api Key 写入 config.json。
    phone/code 可从外部传入（如 --phone/--code 参数），避免重复发短信。
    """
    if not phone:
        if not sys.stdin.isatty():
            die("非交互环境请传参：python3 scripts/zcm.py register --phone 手机号 [--code 验证码]", code=2)
        phone = input("手机号：").strip()
    if not phone:
        die("手机号不能为空。")
    if not code:
        _anon_json("POST", "/auth/send-sms", json_body={"phone": phone})
        log("验证码已发送，5 分钟内有效。")
        if not sys.stdin.isatty():
            die("非交互环境获取验证码后请带 --code 重试：python3 scripts/zcm.py register --phone 手机号 --code 验证码", code=2)
        code = input("验证码：").strip()
    if not code:
        die("验证码不能为空。")
    body = {"phone": phone, "code": code}
    if CHANNEL:
        body["channel"] = CHANNEL
    stored_key = str(load_creds_file().get("app_key", "")).strip()
    if stored_key:
        body["trial_app_key"] = stored_key   # 已有试用 Key：请求绑定（平台校验，非试用 Key 自动忽略）
    resp = _anon_json("POST", "/auth/register", json_body=body)
    new_key = str(resp.get("app_key", "")).strip()
    balance = resp.get("available_words", resp.get("wallet_balance", 0))
    is_new = resp.get("is_new_user", True)
    if not new_key:
        die("注册失败：接口未返回 Api Key。")
    save_creds_file(dict(load_creds_file(), app_key=new_key))
    if resp.get("bound"):
        log(f"绑定成功！手机号已关联当前试用账号（Api Key 不变），当前可用字数：{balance}。")
    elif is_new:
        log(f"注册成功！当前可用字数：{balance}，Api Key 已保存。")
    else:
        log(f"该手机号已注册，已切换到对应账号，当前可用字数：{balance}。")


def _site_base():
    """站点根地址（剥掉 /api/... 段），用于给用户展示官网入口。"""
    b = base_url()
    return b.split("/api/", 1)[0].rstrip("/") if "/api/" in b else "https://biaoshu.zhiliaobiaoxun.com"


def _with_ch(url):
    """CHANNEL 非空时给网页链接追加渠道码 ch；为空原样返回。"""
    if not CHANNEL:
        return url
    return f"{url}{'&' if '?' in url else '?'}ch={CHANNEL}"


def _guide_insufficient_balance(err=None):
    """可用字数不足引导：未绑手机号 → 先提示绑定领取赠送字数；已绑 → 购买会员或字数包。
    绑定只走 skill 内手机号验证码流程；对外只展示不含 Api Key 的官网链接。
    ⚠️ 切勿把 `python3 scripts/zcm.py register` 这类命令或 exit 码抛给用户——只告诉用户下一步需要提供什么。"""
    err = err or {}
    site_url = _with_ch(_site_base())
    phone_bound = bool(err.get("phone_bound"))
    detail = _shortage_detail(err)
    failed_note = ""
    if err.get("task_failed"):
        failed_note = "本次任务已停止；平台不会自动续跑。若平台已导出半成品，可用 download-url 获取；充值或购买字数包后，可用 continue-generate 继续生成正文。\n"
    if not sys.stdin.isatty():
        if phone_bound:
            die(
                f"可用字数不足，{detail}{failed_note}请登录百炼®标书官网购买会员或字数包后重试：{site_url}",
                code=1,
            )
        die(
            f"可用字数不足，{detail}{failed_note}可二选一继续（Api Key 保持不变）：\n"
            "  1) 绑定手机号升级为注册账号并领取赠送字数：把手机号给我，我来发验证码完成绑定。\n"
            f"  2) 登录百炼®标书官网购买会员或字数包后重试：{site_url}",
            code=1,
        )
    if detail:
        log(detail)
    if failed_note:
        log(failed_note.strip())
    log(BALANCE_GUIDE)
    log(f"  （官网地址：{site_url}）")
    choice = input("请输入选项：").strip().lower()
    if choice == "1":
        _register_flow()
        log("请重新提交任务（赠送字数已到账）。")
        sys.exit(0)
    elif choice == "2":
        new_key = input("请粘贴新的 Api Key（直接回车则去官网充值）：").strip()
        if new_key:
            save_creds_file(dict(load_creds_file(), app_key=new_key))
            log("新 Api Key 已保存，请重新提交任务。")
        sys.exit(0)
    else:
        sys.exit(0)


def base_url():
    env_base = os.environ.get("ZCM_BASE", "").strip()
    if env_base:
        return env_base.rstrip("/")
    stored = load_creds_file()
    return str(stored.get("base") or DEFAULT_BASE).rstrip("/")


def _headers(extra=None):
    h = {"X-App-Key": get_creds()}
    if extra:
        h.update(extra)
    return h


def _handle_http_error(e):
    return _handle_http_error_impl(
        e,
        error_hints=ERROR_HINTS,
        guide_insufficient_balance=_guide_insufficient_balance,
        die=die,
    )


def _anon_json(method, path, *, json_body=None, headers=None):
    """无鉴权请求，用于 /auth/send-sms、/auth/register 等注册类接口。"""
    return _request_json_impl(
        method,
        base_url() + path,
        headers=headers,
        json_body=json_body,
        handle_http_error_fn=_handle_http_error,
        die=die,
        network_error_message=lambda e: f"网络错误：{e.reason}",
    )


def request_json(method, path, *, headers=None, data=None, json_body=None):
    """发起请求并解析 JSON 响应。data 为已编码 bytes（如 multipart）。"""
    return _request_json_impl(
        method,
        base_url() + path,
        headers=_headers(headers),
        data=data,
        json_body=json_body,
        handle_http_error_fn=_handle_http_error,
        die=die,
        network_error_message=lambda e: f"网络错误：{e.reason}\n  → 检查 ZCM_BASE（当前 {base_url()}）与网络连通性。",
    )


def poll(job_id, interval=5, timeout=3600):
    return _poll_job_impl(
        job_id,
        interval=interval,
        timeout=timeout,
        request_json_fn=request_json,
        format_progress_line_fn=format_progress_line,
        log_fn=log,
        die_fn=die,
        error_hints=ERROR_HINTS,
        guide_insufficient_balance_fn=_guide_insufficient_balance,
    )


def idempotency_header(args):
    if getattr(args, "idempotency_key", None):
        return {"Idempotency-Key": args.idempotency_key}
    return {}


# ---------------- 子命令 ----------------


def _platform_reminder():
    return _platform_reminder_impl(log)


def _report_balance():
    return _report_balance_impl(request_json, log)


def _maybe_report(result_response, fmt, label, tender_name=None):
    return _maybe_report_impl(
        result_response,
        fmt,
        label,
        tender_name=tender_name,
        output_dir_fn=output_dir,
        log_fn=log,
        platform_reminder_fn=_platform_reminder,
    )


def cmd_report(args):
    return _cmd_report_impl(
        args,
        request_json_fn=request_json,
        recall_tender_fn=recall_tender,
        output_dir_fn=output_dir,
        log_fn=log,
        platform_reminder_fn=_platform_reminder,
    )


def cmd_login(args):
    stored = load_creds_file()
    if args.app_key:
        stored["app_key"] = args.app_key.strip()
    if args.base:
        stored["base"] = args.base.strip().rstrip("/")
    if args.output_dir:
        stored["output_dir"] = os.path.expanduser(args.output_dir.strip())
    if not stored.get("app_key"):
        die("login 需要 --app-key（Api Key 形如 bk_live_xxxxx）。")
    save_creds_file(stored)
    log(f"凭证已保存到 {creds_path()}（权限 600），下次免输。")
    if stored.get("output_dir"):
        log(f"成品标书默认存放目录：{stored['output_dir']}")


def cmd_logout(args):
    try:
        os.remove(creds_path())
        log(f"已删除凭证文件 {creds_path()}。")
    except FileNotFoundError:
        log("没有已保存的凭证文件。")


def cmd_me(args):
    data = request_json("GET", "/me")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    bal = data.get("available_words", data.get("wallet_balance"))
    if bal is not None:
        log(f"可用字数：{bal}")


def cmd_version_check(args):
    result = maybe_check_update(
        skill_version=SKILL_VERSION,
        channel=CHANNEL,
        base_url_fn=base_url,
        creds_path_fn=creds_path,
        load_creds_file_fn=load_creds_file,
        save_creds_file_fn=save_creds_file,
        log_fn=log,
        force=True,
        verbose=True,
    )
    print(json.dumps(result or {}, ensure_ascii=False, indent=2))


def cmd_knowledge_base(args):
    path = "/knowledge-base"
    if getattr(args, "category", None):
        path += f"/{args.category}"
    query = []
    if getattr(args, "category", None):
        query.append(f"page={args.page}")
        query.append(f"page_size={args.page_size}")
    if query:
        path += "?" + "&".join(query)
    data = request_json("GET", path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _precheck_balance():
    """付费任务提交前门槛：低于 1 直接走购买/绑定引导，不发起任务。

    平台侧同样有 402 闸门兜底；此处提前拦截，避免白传大文件。
    """
    resp = request_json("GET", "/me")
    balance = int(resp.get("available_words", resp.get("wallet_balance", 0)) or 0)
    if balance < 1:
        log(f"当前可用字数：{balance}，不足以发起操作（需 ≥ 1）。")
        _guide_insufficient_balance({"wallet_balance": balance})


def _precheck_generation_balance(args):
    """生成前只按确认页数估算字数；不做余额示警，继续推进制作流程。"""
    pages = _generation_pages(args)
    required = _estimate_generation_words(pages)
    log(
        f"本次标书制作预计约需 {required:,} 字；预计消耗仅供参考，"
        "实际消耗以平台最终结算为准；继续提交生成任务。"
    )


def _submit_interpret(args):
    extra = idempotency_header(args)
    if is_url(args.source):
        args.source = download_to_local(args.source, max_mb=MAX_TENDER_MB)   # 云端先下载到本地
    _check_size(args.source, MAX_TENDER_MB, "招标文件")
    body, ctype = encode_multipart(None, [("file", args.source)])
    return request_json("POST", "/interpretations",
                        headers={**extra, "Content-Type": ctype}, data=body)


def _project_info_value(project_info, *names):
    if not isinstance(project_info, list):
        return ""
    wanted = {str(name).strip() for name in names}
    for item in project_info:
        if not isinstance(item, dict):
            continue
        field = str(item.get("field_name") or item.get("name") or "").strip()
        if field in wanted:
            value = item.get("field_value", item.get("value", ""))
            return str(value).strip()
    return ""


def _list_count(result, key):
    value = result.get(key) if isinstance(result, dict) else None
    return len(value) if isinstance(value, list) else 0


def _log_interpret_summary(result_response):
    result = (result_response.get("result") or {}) if isinstance(result_response, dict) else {}
    if not isinstance(result, dict):
        log("解读摘要：平台返回结果格式异常，完整明细请查看解读报告或使用 --full-json 调试。")
        return
    project_info = result.get("project_info") or []
    project_name = _project_info_value(project_info, "项目名称", "项目名", "采购项目名称")
    purchaser = _project_info_value(project_info, "招标人", "采购人", "建设单位")
    decision = result.get("decision_analysis") or {}
    recommendation = decision.get("participation_recommendation") if isinstance(decision, dict) else ""
    risk_level = decision.get("control_risk_level") if isinstance(decision, dict) else ""
    counts = [
        ("合标项", _list_count(result, "compliance")),
        ("废标红线", _list_count(result, "disqualification")),
        ("评分项", _list_count(result, "evaluation")),
        ("关键要求", _list_count(result, "key_requirements")),
        ("商务条款", _list_count(result, "business_terms")),
        ("报价要求", _list_count(result, "pricing")),
    ]
    log("解读摘要：")
    if project_name:
        log(f"项目名称：{project_name}")
    if purchaser:
        log(f"招标/采购人：{purchaser}")
    if recommendation or risk_level:
        parts = []
        if recommendation:
            parts.append(f"参与建议：{recommendation}")
        if risk_level:
            parts.append(f"控标风险：{risk_level}")
        log("；".join(parts))
    log("结构化条目：" + " · ".join(f"{label} {count}" for label, count in counts))
    log("完整明细已写入解读报告；如需调试完整 JSON，可显式使用 --full-json。")


def cmd_interpret(args):
    resp = _submit_interpret(args)
    job_id = resp["job_id"]
    log(f"已提交解读任务 job_id={job_id}")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval)
    result = request_json("GET", f"/jobs/{job_id}/result")
    if getattr(args, "full_json", False):
        print(json.dumps(zh_risk(result), ensure_ascii=False, indent=2))
    else:
        _log_interpret_summary(zh_risk(result))
    pid = (result.get("result") or {}).get("project_id")
    if pid is not None:
        log(f"project_id={pid}  （后续抽包/生成/合规都复用它）")
    # 招标文件名：优先 --name，否则取上传文件名（路径或 URL 末段）
    tender = args.name or os.path.basename(args.source.rstrip("/"))
    # 记到本地，供后续 report --job / compliance 自动命名（无需再传 --name）
    remember_tender(tender, project_id=pid, job_id=job_id)
    _maybe_report(result, args.report or "html", "解读", tender_name=tender)
    _report_balance()


def cmd_packages(args):
    extra = idempotency_header(args)
    resp = request_json("POST", f"/bid-documents/{args.project_id}/packages", headers=extra)
    job_id = resp["job_id"]
    log(f"已提交抽包任务 job_id={job_id}")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval)
    result = request_json("GET", f"/jobs/{job_id}/result")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _build_generate_body(args):
    package_ids = getattr(args, "package_ids", None)
    no_package = bool(getattr(args, "no_package", False))
    total_pages = getattr(args, "total_pages", None)
    use_suggested_pages = bool(getattr(args, "use_suggested_pages", False))
    suggested_pages = getattr(args, "suggested_pages", None)
    max_total_pages = _generation_max_pages(args)
    if not getattr(args, "no_wait", False) and not getattr(args, "foreground_ok", False):
        die("生成任务耗时较长，必须先用 --no-wait 提交 job_id，再用 progress-stream 实时播报；仅本地调试可加 --foreground-ok。", code=2)
    if package_ids and no_package:
        die("生成前只能二选一：多包传 --package-ids；单包/不分包传 --no-package。", code=2)
    if not package_ids and not no_package:
        die("生成前必须先抽包并让用户确认：多包传 --package-ids；单包/不分包传 --no-package。", code=2)
    if total_pages and use_suggested_pages:
        die("生成页数只能二选一：传 --total-pages 指定页数，或传 --use-suggested-pages 使用系统建议页数。", code=2)
    if not total_pages and not use_suggested_pages:
        die("生成前必须先让用户确认页数：传 --total-pages <页数>，或传 --use-suggested-pages 使用系统建议页数。", code=2)
    if max_total_pages is None:
        die("--max-total-pages 必须传入抽包结果 max_total_pages，避免超过当前项目允许页数。", code=2)
    if max_total_pages <= 0 or max_total_pages > 1200:
        die("--max-total-pages 必须在 1-1200 之间，并以抽包结果返回值为准。", code=2)
    if use_suggested_pages and suggested_pages is None:
        die("--use-suggested-pages 必须同时传 --suggested-pages <抽包结果 suggested_pages>，避免按固定页数误估。", code=2)
    if suggested_pages is not None and (suggested_pages <= 0 or suggested_pages > max_total_pages):
        die(f"--suggested-pages 必须在 1-{max_total_pages} 之间，不能超过当前项目最大页数 {max_total_pages}。", code=2)

    body = {}
    if package_ids:
        try:
            body["package_ids"] = [int(x) for x in package_ids.split(",") if x.strip()]
        except ValueError:
            die("--package-ids 必须是逗号分隔的数字，如 11,12。", code=2)
        if not body["package_ids"]:
            die("--package-ids 不能为空；单包/不分包请传 --no-package。", code=2)
    if total_pages:
        if total_pages <= 0 or total_pages > max_total_pages:
            die(f"--total-pages 必须在 1-{max_total_pages} 之间，不能超过当前项目最大页数 {max_total_pages}。", code=2)
        body["total_pages"] = total_pages
    elif use_suggested_pages:
        body["total_pages"] = suggested_pages
    return body


def cmd_generate(args):
    body = _build_generate_body(args)
    _precheck_generation_balance(args)
    extra = idempotency_header(args)
    resp = request_json("POST", f"/bid-documents/{args.project_id}/generate",
                        headers=extra, json_body=body)
    job_id = resp["job_id"]
    log(f"已提交生成任务 job_id={job_id}（耗时较长，请耐心轮询）")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval, timeout=args.timeout)
    if args.output:
        out = args.output
        download_result(job_id, out)
        abs_out = os.path.abspath(out)
        log(f"已下载成品标书：{abs_out}")
        log(f"标书所在目录：{os.path.dirname(abs_out)}")
        print(abs_out)
    else:
        print_download_link(job_id)
    _platform_reminder()
    _report_balance()


def cmd_continue_generate(args):
    if not getattr(args, "no_wait", False) and not getattr(args, "foreground_ok", False):
        die("继续生成任务耗时较长，必须先用 --no-wait 提交 job_id，再用 progress-stream 实时播报；仅本地调试可加 --foreground-ok。", code=2)
    _precheck_balance()
    extra = idempotency_header(args)
    resp = request_json(
        "POST",
        f"/bid-documents/{args.project_id}/continue-generate",
        headers=extra,
        json_body={"outline_id": args.outline_id},
    )
    job_id = resp["job_id"]
    log(f"已提交继续生成任务 job_id={job_id}（将补写未完成正文并重新导出）")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval, timeout=args.timeout)
    print_download_link(job_id)
    _platform_reminder()
    _report_balance()


def cmd_compliance(args):
    _precheck_balance()
    extra = idempotency_header(args)
    # 云端投标文件先逐个下载到本地，再统一按本地文件多文件上传
    paths = [download_to_local(s, max_mb=MAX_BID_MB) if is_url(s) else s for s in args.files]
    for p in paths:
        _check_size(p, MAX_BID_MB, "投标文件")
    fields = {
        "is_blind_bid": str(args.blind).lower(),
        "is_electronic_bid": str(args.electronic).lower(),
    }
    if args.sibling_unit_names:
        fields["sibling_unit_names"] = args.sibling_unit_names
    if args.no_semantic_review:
        fields["semantic_review"] = "false"
    body, ctype = encode_multipart(fields, [("bid_files", p) for p in paths])
    resp = request_json("POST", f"/projects/{args.project_id}/compliance-reviews",
                        headers={**extra, "Content-Type": ctype}, data=body)
    job_id = resp["job_id"]
    log(f"已提交合规审查任务 job_id={job_id}")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval)
    result = request_json("GET", f"/jobs/{job_id}/result")
    print(json.dumps(zh_risk(result), ensure_ascii=False, indent=2))
    # 招标文件名：--name 优先，否则按 project_id 回查本地（interpret 时记下的）
    tender = args.name or recall_tender(project_id=args.project_id)
    _maybe_report(result, args.report or "html", "合规", tender_name=tender)
    _report_balance()


def cmd_duplicate(args):
    """标书查重：2-3 份投标文件做雷同/相似风险检查，可选招标文件作为公共表述基线。"""
    if not 2 <= len(args.files) <= 3:
        die(
            "标书查重需要先提供 2-3 份投标文件；招标文件不能算作投标文件，"
            "如需作为公共表述基线请单独用 --tender-file 传入。请先向用户收齐至少 2 份投标文件后再发起查重。",
            code=2,
        )
    if not args.legal_possession_attested:
        die(
            "发起标书查重前必须确认：用户合法持有并有权处理本次上传的全部投标文件/招标文件。"
            "确认后再加 --legal-possession-attested。",
            code=2,
        )
    _precheck_balance()
    extra = idempotency_header(args)
    paths = [download_to_local(s, max_mb=MAX_BID_MB) if is_url(s) else s for s in args.files]
    tender = download_to_local(args.tender_file, max_mb=MAX_TENDER_MB) if args.tender_file and is_url(args.tender_file) else args.tender_file
    for p in paths:
        _check_size(p, MAX_BID_MB, "投标文件")
    if tender:
        _check_size(tender, MAX_TENDER_MB, "招标文件")
    _check_total_size(paths + ([tender] if tender else []), MAX_DUP_TOTAL_MB, "查重文件")
    fields = {
        "legal_possession_attested": "true",
        "enable_image": str(not args.no_image).lower(),
        "enable_metadata": str(not args.no_metadata).lower(),
        "enable_semantic": str(not args.no_semantic).lower(),
        "exclude_tender_baseline": str(not args.include_tender_baseline).lower(),
    }
    files = [("bid_files", p) for p in paths]
    if tender:
        files.append(("tender_file", tender))
    body, ctype = encode_multipart(fields, files)
    resp = request_json("POST", "/bid-duplicate/runs",
                        headers={**extra, "Content-Type": ctype}, data=body)
    job_id = resp["job_id"]
    log(f"已提交标书查重任务 job_id={job_id}")
    if args.no_wait:
        print(job_id)
        return
    poll(job_id, interval=args.interval)
    result = request_json("GET", f"/jobs/{job_id}/result")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    _maybe_report(result, args.report or "html", "查重")
    _report_balance()


def cmd_job(args):
    return _cmd_job_impl(args, request_json_fn=request_json)


def download_result(job_id, out_path):
    return _download_result_impl(
        job_id,
        out_path,
        base_url_fn=base_url,
        headers_fn=_headers,
        handle_http_error_fn=_handle_http_error,
        die_fn=die,
    )


def get_download_url(job_id):
    return _get_download_url_impl(job_id, request_json_fn=request_json)


def print_download_link(job_id):
    return _print_download_link_impl(
        job_id,
        request_json_fn=request_json,
        format_seconds_fn=_format_seconds,
        format_bytes_fn=_format_bytes,
        log_fn=log,
    )


def cmd_result(args):
    return _cmd_result_impl(
        args,
        request_json_fn=request_json,
        download_result_fn=download_result,
        platform_reminder_fn=_platform_reminder,
        zh_risk_fn=zh_risk,
        log_fn=log,
    )


def cmd_download_url(args):
    return _cmd_download_url_impl(args, print_download_link_fn=print_download_link)


def cmd_register(args):
    """skill 内手机号注册/登录，换取 Api Key 并保存到 config.json。"""
    _register_flow(phone=getattr(args, "phone", None),
                   code=getattr(args, "code", None))


def cmd_trial(args):
    """免费试用：设备特征自动开通账号（赠 50,000 字），换取并保存 Api Key。"""
    _trial_flow()


def cmd_cancel(args):
    return _cmd_cancel_impl(args, request_json_fn=request_json)


# 经验/反馈单条内容上限（与平台一致）
MAX_EXPERIENCE_CHARS = 10 * 1024


def cmd_experience(args):
    """经验沉淀：把助手总结（用户已过目并同意）回传平台，只存不用。"""
    if args.content_file:
        try:
            with open(args.content_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except OSError as e:
            die(f"读取内容文件失败：{e}")
    else:
        content = (args.content or "").strip()
    if not content:
        die("需要 --content 文本或 --content-file 文件路径。")
    if len(content) > MAX_EXPERIENCE_CHARS:
        die(f"内容过长（{len(content)} 字符 > {MAX_EXPERIENCE_CHARS}），请精简后重试。")
    body = {"type": args.type, "stage": args.stage,
            "title": args.title, "content": content}
    if args.project_id:
        body["project_id"] = args.project_id
    resp = request_json("POST", "/experience/submit", json_body=body)
    total = resp.get("total_count")
    if total is not None:
        log(f"经验已沉淀到百炼®标书平台，累计 {total} 条。")
    else:
        log("经验已沉淀到百炼®标书平台。")
    print(json.dumps(resp, ensure_ascii=False))


def cmd_feedback(args):
    """问题上报：结构化上报使用问题（用户已过目并同意），自动附带版本与渠道。"""
    body = {
        "category": args.category,
        "scene": args.scene,
        "phenomenon": args.phenomenon,
        "expectation": (args.expectation or ""),
        "skill_version": SKILL_VERSION,
        "channel": CHANNEL,
    }
    resp = request_json("POST", "/feedback/submit", json_body=body)
    log("问题已上报，感谢反馈（不含文件内容与个人信息）。")
    print(json.dumps(resp, ensure_ascii=False))


def cmd_progress_stream(args):
    return _progress_stream_impl(
        args,
        request_json_fn=request_json,
        format_progress_line_fn=format_progress_line,
        guide_insufficient_balance_fn=_guide_insufficient_balance,
        error_hints=ERROR_HINTS,
    )


def _parser_funcs():
    return {
        "login": cmd_login,
        "logout": cmd_logout,
        "register": cmd_register,
        "trial": cmd_trial,
        "me": cmd_me,
        "version_check": cmd_version_check,
        "knowledge_base": cmd_knowledge_base,
        "interpret": cmd_interpret,
        "packages": cmd_packages,
        "generate": cmd_generate,
        "continue_generate": cmd_continue_generate,
        "compliance": cmd_compliance,
        "duplicate": cmd_duplicate,
        "report": cmd_report,
        "job": cmd_job,
        "result": cmd_result,
        "download_url": cmd_download_url,
        "cancel": cmd_cancel,
        "experience": cmd_experience,
        "feedback": cmd_feedback,
        "progress_stream": cmd_progress_stream,
    }


def _build_parser():
    return build_cli_parser(
        skill_version=SKILL_VERSION,
        api_target=API_TARGET,
        contract_snapshot=CONTRACT_SNAPSHOT,
        funcs=_parser_funcs(),
        description="百炼®标书开放 API 轻客户端",
        include_skillhub_auth=True,
        allow_remote_files=True,
        include_feedback=True,
        include_version_check=True,
    )

def main():
    args = _build_parser().parse_args()
    maybe_check_update(
        skill_version=SKILL_VERSION,
        channel=CHANNEL,
        base_url_fn=base_url,
        creds_path_fn=creds_path,
        load_creds_file_fn=load_creds_file,
        save_creds_file_fn=save_creds_file,
        log_fn=log,
    )
    args.func(args)
