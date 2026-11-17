"""百炼®标书开放 API 轻客户端（thin client）。

封装「提交 → 轮询 → 取结果」异步模型，零第三方依赖（仅标准库）。
凭证通过本地凭证文件 config.json 传入；可选环境变量仅覆盖本地输出路径：
  ZCM_OUTPUT_DIR  成品标书 .docx 存放目录；未设时默认 skill 同级的 biaoshu-bailian-files/

Api Key 只从 skill 内 config.json 读取。
凭证文件权限 600。config.json 含真实 Key，**勿上传发布包**（发布包不含配置文件）。
Api Key 仅能在官网自助注册获取（本 skill 不代注册）。
用 login 显式保存凭证、logout 清除。
成品存放目录优先级：generate -o 显式路径 > ZCM_OUTPUT_DIR > 凭证文件的 output_dir > 默认 biaoshu-bailian-files。

子命令：
  login      --app-key ..  保存凭证到 skill 内 config.json（输一次，下次免输）
  logout                   删除已保存的凭证
  me                                查连通性与可用字数
  interpret  <file>                 智能解读招标文件 → 打印摘要并生成解读报告（--full-json 可看完整结果）
  packages   <project_id>           抽取分包 → 打印 packages JSON（供用户挑选）
  generate   <project_id> [opts]    用户确认包和页数后生成成品标书，WorkBuddy/ClawHub 必须配合 --no-wait + progress-stream
  compliance <project_id> <f...>    合规审查投标文件 → 打印完整合规结果
  duplicate  <f...>                 标书查重：2-3 份投标文件雷同/相似风险检查
  report     --job <id> | --in f    把解读/合规/查重结果渲染成 HTML/Word 报告
  knowledge-base [category]         按类别查询知识库（排除历史标书库 / 标书模板库）

interpret / compliance / duplicate 可加 --report html|docx|both 在取结果后直接出报告。
  job        <job_id>               查单个任务状态（不轮询）
  download-url <job_id>             获取成品标书短时下载链接
  result     <job_id> [-o file]     取任务结果 / -o 下载成品
  cancel     <job_id>               取消任务

generate 必须显式确认包处理方式和页数，并默认要求 --no-wait 后接 progress-stream。
其他提交类子命令（interpret/packages/compliance/duplicate）默认自动轮询到终态，加 --no-wait 只提交并打印 job_id。
Locale scope: zh-CN (Simplified Chinese) by design for mainland-China bidding workflows. User-facing help text, platform menu names, risk labels, and generated report prompts default to Chinese because they mirror procurement terminology used by the underlying platform and report artifacts. Assistants may explain those terms in the user's language when needed, but in-product labels remain zh-CN.
"""
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
    encode_multipart,
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

DEFAULT_BASE = "https://biaoshu.zhiliaobiaoxun.com/api/open/v1"

# skill 版本（单一事实来源）。适配的后端 API 版本与契约快照见 references/api.md 顶部。
SKILL_VERSION = "3.1.2"
API_TARGET = "/api/open/v1"
CONTRACT_SNAPSHOT = "2026-09-07"

# 渠道码：开发线留空（不带渠道）；发布/装配变体时按平台 excel 注入（ClawHub 基线 s113，变体 s81–s114）。
# 非空时官网链接追加 ?ch=。
CHANNEL = "c666"
SIGNUP_URL = "https://biaoshu.zhiliaobiaoxun.com/" + (f"?ch={CHANNEL}" if CHANNEL else "")

# Locale scope: zh-CN labels are intentional for mainland-China bidding workflows;
# assistants may translate explanations externally, but in-product menu names and prompts remain Chinese.
# 文档第 6 节错误码 → 友好提示
ERROR_HINTS = {
    "missing_credentials": "缺少鉴权头：请在本 skill 目录下的 config.json 写入 app_key（或用 login 保存）。",
    "invalid_credentials": f"Api Key 不正确：核对凭证，或到官网 {SIGNUP_URL} 左侧菜单『Skill 接入 → 获取 Api Key』重置 Key（重置后旧 Key 立即失效）。",
    "account_disabled": "凭证或用户已被停用，请联系百炼®标书管理员。",
    "insufficient_points": "可用字数不足：请到官网购买会员或字数包后重试。",
    "insufficient_balance": "可用字数不足：请先购买会员或字数包后重试。",
    "not_found": "404：多为开放 API 总开关未开（整层 404），请联系超级管理员在『系统设置』开启；或句柄不存在。",
    "job_not_found": "任务句柄不存在或非本人，请核对 job_id。",
    "project_not_found": "project 不存在或非本人，请核对 project_id（由智能解读产出）。",
    "result_expired": "结果已过期（默认约 7 天 TTL），需重新生成。",
    "invalid_job_state": "任务状态不允许此操作：任务未成功就取结果 / 未解读就生成 / 未抽包就 generate。",
    "validation_error": "入参校验失败：文件缺失或类型不支持 / 缺 package_ids 等。",
    "rate_limited": "触发限流（60 req/min）：稍后退避重试（参考 Retry-After）。",
    "too_many_concurrent_jobs": "并发任务超限（≤3）：等已有任务结束再提交。",
    "internal_error": "服务端异常：稍后重试或反馈百炼®标书。",
    "skill_trial_registration_disabled": f"需要先配置百炼标书 Api Key 才能继续使用。请用户本人登录官网 {SIGNUP_URL} 注册并获取 Api Key，再自行写入本 skill 目录下的 config.json；不要把手机号、短信验证码或 Api Key 发给助手。",
}

REGISTER_GUIDE = f"""\
还没配置 Api Key —— 这是用百炼®标书写作助手出解读/标书/合规的唯一开关。
用户本人按官网流程注册可领取赠送字数，配置 Api Key 后这份文件马上就能出解读。

转述给用户时按顺序完整给出，链接原样显示完整 URL：

  第 1 步 · 用户本人在官网注册并拿 Key
    1) 打开官网 {SIGNUP_URL}
    2) 用户本人按官网流程注册登录（注册可领赠送字数）
    3) 点左侧菜单『Skill 接入 → 获取 Api Key』，在面板里查看/复制 Api Key（首次打开自动生成，形如 bk_live_xxxxx）

  第 2 步 · 配置凭证（拿到 Key 后做一次，配好下次免输）
    由用户本人在本 skill 目录下创建凭证文件 config.json，写入一行：
      {{"app_key": "bk_live_xxxxx"}}
    （把 bk_live_xxxxx 换成自己的 Key。）

凭证安全：Api Key 是账户的完整凭证，全程由用户本人写入本地文件——
  不要在对话里索取手机号、短信验证码、Api Key，也不要让用户粘贴或复述 Key。Key 泄露或想作废时，随时到官网
  左侧菜单『Skill 接入 → 获取 Api Key』重置，旧 Key 立即失效。
"""


def die(msg, code=1):
    print(msg, file=sys.stderr, flush=True)
    sys.exit(code)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def get_creds():
    """返回 Api Key。只从本地 config.json 读取；未配置时打印官网获取指引并退出（码 2）。"""
    app_key = str(load_creds_file().get("app_key", "")).strip()
    if not app_key:
        die(REGISTER_GUIDE, code=2)
    return app_key


def _site_base():
    """站点根地址（剥掉 /api/... 段），用于拼注册/绑定/充值网页链接。"""
    b = base_url()
    return b.split("/api/", 1)[0].rstrip("/") if "/api/" in b else "https://biaoshu.zhiliaobiaoxun.com"


def _guide_insufficient_balance(err=None):
    """可用字数不足引导：只给不含凭证的官网链接（凭证保护：平台 402 下发的
    recharge_url/bind_url 携带明文 bind_key，一律不转发进对话）。"""
    detail = _shortage_detail(err)
    failed_note = ""
    if (err or {}).get("task_failed"):
        failed_note = "本次任务已停止；平台不会自动续跑。若平台已导出半成品，可用 download-url 获取；充值或购买字数包后，可用 continue-generate 继续生成正文。"
    die(
        f"可用字数不足，{detail}{failed_note}请用户自行登录官网购买会员或字数包后重试，"
        "Api Key 保持不变：\n"
        f"  入口：{_site_base()}/recharge （用本人账号登录后操作）\n"
        "（为保护凭证，不要向用户转发任何携带 Api Key / bind_key 参数的链接。）",
        code=1,
    )


def base_url():
    """ClawHub 净化线固定只访问生产开放 API，禁止任何本地覆盖。"""
    return DEFAULT_BASE


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
        network_error_message=lambda e: f"网络错误：{e.reason}\n  → 检查网络连通性与开放 API 地址（当前 {base_url()}）。",
    )


def _reject_remote(s, label):
    """本 skill 只接受本地文件；给了链接就友好拒绝（不做任何远程抓取）。"""
    if s.startswith("http://") or s.startswith("https://"):
        die(f"{label}只支持本地文件路径，不支持云端链接：请先自行把文件下载到本地，再把本地路径提供给助手。")


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
    stored.pop("base", None)
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
    """付费任务提交前门槛：低于 1 直接走购买引导，不发起任务。

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
    _reject_remote(args.source, "招标文件")
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
    paths = list(args.files)
    for p in paths:
        _reject_remote(p, "投标文件")
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
    paths = list(args.files)
    for p in paths:
        _reject_remote(p, "投标文件")
        _check_size(p, MAX_BID_MB, "投标文件")
    tender = args.tender_file
    if tender:
        _reject_remote(tender, "招标文件")
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


def cmd_cancel(args):
    return _cmd_cancel_impl(args, request_json_fn=request_json)


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
        "me": cmd_me,
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
        "progress_stream": cmd_progress_stream,
    }


def _build_parser():
    return build_cli_parser(
        skill_version=SKILL_VERSION,
        api_target=API_TARGET,
        contract_snapshot=CONTRACT_SNAPSHOT,
        funcs=_parser_funcs(),
        description="百炼®标书开放 API 轻客户端 / zh-CN client for mainland-China bidding workflows",
    )

def main():
    args = _build_parser().parse_args()
    args.func(args)
