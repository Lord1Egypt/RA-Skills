"""CLI parser construction for the zcm entrypoint."""

import argparse


def build_parser(
    *,
    skill_version,
    api_target,
    contract_snapshot,
    funcs,
    description,
    include_skillhub_auth=False,
    allow_remote_files=False,
    include_feedback=False,
    include_version_check=False,
):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--version",
        action="version",
        version=f"biaoshu-writer-transit {skill_version}　·　适配 {api_target}　·　契约快照 {contract_snapshot}",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_common(sp, wait=False):
        sp.add_argument("--interval", type=int, default=5, help="轮询间隔秒（默认 5）")
        if wait:
            sp.add_argument("--no-wait", action="store_true", help="只提交，打印 job_id 不轮询")
            sp.add_argument("--idempotency-key", help="幂等键 UUID，重试防重复扣费")

    sp = sub.add_parser("login", help="保存凭证到 config.json" if include_skillhub_auth else "保存凭证到 skill 内 config.json")
    sp.add_argument("--app-key", help="Api Key，形如 bk_live_xxxxx（必填）")
    if include_skillhub_auth:
        sp.add_argument("--base", help="可选：Base URL")
    sp.add_argument("--output-dir", help="可选：成品标书 .docx 默认存放目录")
    sp.set_defaults(func=funcs["login"])

    sp = sub.add_parser("logout", help="删除已保存的凭证文件")
    sp.set_defaults(func=funcs["logout"])

    if include_skillhub_auth:
        sp = sub.add_parser("register", help="skill 内手机号注册/登录，换取并保存 Api Key")
        sp.add_argument("--phone", help="手机号（可选，不填则交互输入）")
        sp.add_argument("--code", help="验证码（已有验证码时传入，跳过重发短信）")
        sp.set_defaults(func=funcs["register"])

        sp = sub.add_parser("trial", help="免费试用：设备特征自动开通账号（赠 50,000 字），换取并保存 Api Key")
        sp.set_defaults(func=funcs["trial"])

    sp = sub.add_parser("me", help="查连通性与可用字数")
    sp.set_defaults(func=funcs["me"])

    if include_version_check:
        sp = sub.add_parser("version-check", help="手动检查 skill 最新版本（后台排查用）")
        sp.set_defaults(cmd="version_check", func=funcs["version_check"])

    sp = sub.add_parser("knowledge-base", help="按类别查询知识库（排除历史标书库 / 标书模板库）")
    sp.add_argument("category", nargs="?", help="可选：company_profile / qualifications / performances / financial_reports")
    sp.add_argument("--page", type=int, default=1, help="分页类页码（默认 1）")
    sp.add_argument("--page-size", type=int, default=50, help="分页类每页条数（默认 50）")
    sp.set_defaults(func=funcs["knowledge_base"])

    remote_hint = " 或 https URL" if allow_remote_files else ""
    remote_plural_hint = "，或多个 https URL" if allow_remote_files else ""
    duplicate_remote_hint = "，或 2-3 个 https URL" if allow_remote_files else ""
    tender_remote_hint = " 或 https URL" if allow_remote_files else ""

    sp = sub.add_parser("interpret", help="智能解读招标文件 → 摘要 + 解读报告")
    sp.add_argument("source", help=f"本地文件(.pdf/.doc/.docx){remote_hint}")
    sp.add_argument("--report", choices=["html", "docx", "both"], help="取结果后直接生成解读报告")
    sp.add_argument("--name", help="招标文件名（报告默认命名用；不填取上传文件名）")
    sp.add_argument("--full-json", action="store_true", help="调试用：打印完整 /result JSON（默认只打印摘要以加快 WorkBuddy 展示）")
    add_common(sp, wait=True)
    sp.set_defaults(func=funcs["interpret"])

    sp = sub.add_parser("packages", help="抽取分包供挑选")
    sp.add_argument("project_id")
    add_common(sp, wait=True)
    sp.set_defaults(func=funcs["packages"])

    sp = sub.add_parser("generate", help="生成成品标书（默认输出短时下载链接，-o 时下载 .docx）")
    sp.add_argument("project_id")
    sp.add_argument("--package-ids", help="逗号分隔的选中分包 ID，如 11,12（多包必填，需用户确认）")
    sp.add_argument("--no-package", action="store_true", help="确认该项目单包/不分包，无需传 package_ids")
    sp.add_argument("--total-pages", type=int, help="用户确认的期望总页数，不能超过抽包结果 max_total_pages")
    sp.add_argument("--use-suggested-pages", action="store_true", help="用户确认使用抽包结果中的系统建议页数")
    sp.add_argument("--suggested-pages", type=int, help="抽包结果返回的 suggested_pages；使用 --use-suggested-pages 时必填")
    sp.add_argument("--max-total-pages", type=int, help="抽包结果返回的 max_total_pages；生成时必填")
    sp.add_argument("-o", "--output", help="输出 .docx 路径（默认 招标文件名_投标文件.docx）")
    sp.add_argument("--name", help="招标文件名（成品默认命名 招标文件名_投标文件）")
    sp.add_argument("--timeout", type=int, default=3600, help="轮询超时秒（默认 3600）")
    sp.add_argument("--foreground-ok", action="store_true", help="仅本地调试使用：允许前台轮询，WorkBuddy/ClawHub 不要使用")
    add_common(sp, wait=True)
    sp.set_defaults(func=funcs["generate"])

    sp = sub.add_parser("continue-generate", help="继续生成半成品正文，并重新导出标书")
    sp.add_argument("project_id")
    sp.add_argument("--outline-id", type=int, required=True, help="半成品下载提示中的 outline_id")
    sp.add_argument("--timeout", type=int, default=3600, help="轮询超时秒（默认 3600）")
    sp.add_argument("--foreground-ok", action="store_true", help="仅本地调试使用：允许前台轮询，WorkBuddy/ClawHub 不要使用")
    add_common(sp, wait=True)
    sp.set_defaults(cmd="continue_generate", func=funcs["continue_generate"])

    sp = sub.add_parser("compliance", help="标书审查投标文件(.doc/.docx/.pdf)")
    sp.add_argument("project_id")
    sp.add_argument("files", nargs="+", help=f"一个或多个本地 .doc/.docx/.pdf{remote_plural_hint}")
    sp.add_argument("--blind", action="store_true", help="暗标")
    sp.add_argument("--electronic", action="store_true", help="电子标")
    sp.add_argument("--sibling-unit-names", help="敏感单位名称，多个用逗号或顿号分隔")
    sp.add_argument("--no-semantic-review", action="store_true", help="关闭语义审查，仅保留规则类检查")
    sp.add_argument("--report", choices=["html", "docx", "both"], help="取结果后直接生成合规报告")
    sp.add_argument("--name", help="招标文件名（合规报告默认命名 招标文件名_合规审查）")
    add_common(sp, wait=True)
    sp.set_defaults(func=funcs["compliance"])

    sp = sub.add_parser("duplicate", help="标书查重：2-3 份投标文件雷同/相似风险检查")
    sp.add_argument("files", nargs="+", help=f"必须是 2-3 份投标文件；不要把招标文件放进这里。本地 .doc/.docx/.pdf{duplicate_remote_hint}")
    sp.add_argument("--tender-file", help=f"可选：单独传招标文件（本地 .doc/.docx/.pdf{tender_remote_hint}），用于排除招标原文共同表述")
    sp.add_argument("--legal-possession-attested", action="store_true",
                    help="确认用户合法持有并有权处理本次上传的全部文件（必需）")
    sp.add_argument("--no-image", action="store_true", help="关闭图片相似检查")
    sp.add_argument("--no-metadata", action="store_true", help="关闭文档元数据检查")
    sp.add_argument("--no-semantic", action="store_true", help="关闭语义相似检查")
    sp.add_argument("--include-tender-baseline", action="store_true",
                    help="不排除招标文件原文造成的共同表述（默认排除）")
    sp.add_argument("--report", choices=["html", "docx", "both"], help="取结果后直接生成查重报告")
    add_common(sp, wait=True)
    sp.set_defaults(func=funcs["duplicate"])

    sp = sub.add_parser("report", help="把解读/合规/查重结果渲染成 HTML/Word 报告")
    group = sp.add_mutually_exclusive_group(required=True)
    group.add_argument("--job", help="任务 job_id（自动取 /result 再渲染）")
    group.add_argument("--in", dest="in_file", help="本地结果 JSON 文件（/result 响应或 result 体）")
    sp.add_argument("--service", choices=["interpretation", "compliance", "bid_duplicate"], help="不指定则自动识别")
    sp.add_argument("--format", choices=["html", "docx", "both"], default="html",
                    help="默认 html；用户明确要 Word 才用 docx 或 both")
    sp.add_argument("-o", "--out-dir", help="输出目录（默认成品目录 biaoshu-writer-transit-files/）")
    sp.add_argument("--name", help="招标文件名（报告默认命名 招标文件名_{智能解读|合规审查|标书查重}）")
    sp.add_argument("--basename", help="完整文件名（不含扩展名），优先级最高")
    sp.set_defaults(func=funcs["report"])

    sp = sub.add_parser("job", help="查任务状态（不轮询）")
    sp.add_argument("job_id")
    sp.set_defaults(func=funcs["job"])

    sp = sub.add_parser("result", help="取任务结果")
    sp.add_argument("job_id")
    sp.add_argument("-o", "--output", help="保存到本地文件（标书制作 .docx 需要本地文件时使用）")
    sp.set_defaults(func=funcs["result"])

    sp = sub.add_parser("download-url", help="获取成品标书短时下载链接（不暴露 Api Key）")
    sp.add_argument("job_id")
    sp.set_defaults(func=funcs["download_url"])

    sp = sub.add_parser("cancel", help="取消任务")
    sp.add_argument("job_id")
    sp.set_defaults(func=funcs["cancel"])

    if include_feedback:
        sp = sub.add_parser("experience", help="把本阶段经验总结回传平台沉淀（用户同意后）")
        sp.add_argument("--type", required=True,
                        choices=["material", "preference", "correction"],
                        help="material=内容素材 preference=写作偏好 correction=纠错经验")
        sp.add_argument("--stage", required=True,
                        choices=["interpret", "write", "compliance"],
                        help="interpret=解读调整 write=改稿 compliance=合规整改")
        sp.add_argument("--title", required=True, help="条目标题")
        sp.add_argument("--content", help="总结文本（短文本直接传）")
        sp.add_argument("--content-file", help="总结文本文件路径（长文本用，避开命令行长度限制）")
        sp.add_argument("--project-id", help="可选：关联项目 ID（溯源用）")
        sp.set_defaults(func=funcs["experience"])

        sp = sub.add_parser("feedback", help="上报使用问题（用户同意后；不含文件内容与个人信息）")
        sp.add_argument("--category", required=True,
                        choices=["misguide", "correction", "error", "suggestion"],
                        help="misguide=流程跑偏 correction=用户纠正 error=报错 suggestion=建议")
        sp.add_argument("--scene", required=True, help="场景，如 智能解读/生成标书/合规审查")
        sp.add_argument("--phenomenon", required=True, help="现象描述（勿含文件内容/个人信息）")
        sp.add_argument("--expectation", help="期望行为（可选）")
        sp.set_defaults(func=funcs["feedback"])

    sp = sub.add_parser("progress-stream",
                        help="流式进度到 stdout，供 Monitor 实时订阅（配合 --no-wait 两阶段用）")
    sp.add_argument("job_id")
    sp.add_argument("--interval", type=float, default=5.0, help="轮询间隔秒（默认 5）")
    sp.add_argument("--step", type=int, default=5, help="百分比变化步进阈值，达到才输出（默认 5）")
    sp.add_argument("--heartbeat", type=float, default=5, help="无新阶段时的心跳输出间隔秒（默认 5）")
    sp.add_argument("--timeout", type=int, default=3600, help="超时秒（默认 3600）")
    sp.set_defaults(func=funcs["progress_stream"])

    return parser
