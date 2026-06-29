from __future__ import annotations

from typing import Any


CARD_VERSION = "paper-kb-card-v1"


def option(label: str, value: str, description: str = "", style: str = "default") -> dict[str, Any]:
    return {
        "label": label,
        "value": value,
        "description": description,
        "style": style,
    }


def field(name: str, label: str, placeholder: str = "", required: bool = True, multiline: bool = False) -> dict[str, Any]:
    return {
        "name": name,
        "label": label,
        "placeholder": placeholder,
        "required": required,
        "multiline": multiline,
    }


def card(
    card_id: str,
    title: str,
    summary: str,
    actions: list[dict[str, Any]] | None = None,
    fields: list[dict[str, Any]] | None = None,
    hidden: dict[str, Any] | None = None,
    submit_action: str = "",
) -> dict[str, Any]:
    return {
        "type": "feishu_interactive_card",
        "version": CARD_VERSION,
        "card_id": card_id,
        "title": title,
        "summary": summary,
        "fallback_text": summary,
        "fields": fields or [],
        "actions": actions or [],
        "hidden": hidden or {},
        "submit_action": submit_action,
        "callback_contract": {
            "action_value_field": "CardActionValue",
            "form_values_field": "CardFormValues",
            "hidden_fields_included": True,
        },
    }


def target_choice(team_name: str = "") -> dict[str, Any]:
    actions = [option("个人知识库", "target:personal", "导入到我的个人知识库", "primary")]
    if team_name:
        actions.append(option(f"团队知识库：{team_name}", "target:team", "导入到团队知识库", "primary"))
    return card(
        "batch.target.choice",
        "选择导入目标",
        "请选择这批资料要导入到哪里。",
        actions=actions,
    )


def project_choice(projects: list[dict[str, str]], can_create_project: bool) -> dict[str, Any]:
    actions = [option("general", "project:general", "团队公共资料", "primary")]
    for project in projects[:8]:
        project_id = project.get("project_id", "")
        name = project.get("name", project_id)
        if project_id and project_id != "general":
            actions.append(option(name, f"project:{project_id}", project.get("brief", "")))
    if can_create_project:
        actions.append(option("创建新项目", "project:create", "需要填写项目名称和说明"))
    return card(
        "batch.project.choice",
        "选择团队项目",
        "请选择这批资料所属的项目空间。",
        actions=actions,
    )


def preview_confirm(
    task_id: str,
    source_label: str,
    stats: dict[str, Any],
    target_owner: str,
    target_repo: str,
    auto_update: bool,
) -> dict[str, Any]:
    document_count = sum(int(stats.get(key, 0) or 0) for key in ["markdown", "text", "pdf", "docx", "xlsx", "xls"])
    code_count = int(stats.get("code", 0) or 0) + int(stats.get("dependency", 0) or 0)
    skipped_count = int(stats.get("skipped", stats.get("skip", 0)) or 0)
    summary = (
        f"资料源：{source_label}。目标知识库：{target_owner}/{target_repo}。"
        f"文档 {document_count} 个，代码相关 {code_count} 个，跳过 {skipped_count} 个。"
        f"自动更新：{'开启' if auto_update else '关闭'}。"
    )
    return card(
        "batch.preview.confirm",
        "确认开始批量编译",
        summary,
        actions=[
            option("开始编译", f"start_batch:{task_id}", "确认后会派后台 worker 执行", "primary"),
            option("取消导入", f"cancel_batch:{task_id}", "删除待确认任务", "danger"),
        ],
        hidden={"task_id": task_id},
    )


def worker_started(job_id: str, total_documents: int, code_files: int) -> dict[str, Any]:
    return card(
        "batch.worker.started",
        "批量编译已开始",
        f"Job：{job_id}。待编译文档 {total_documents} 个，代码相关文件 {code_files} 个。完成后会自动通知。",
        actions=[
            option("查看状态", f"job_status:{job_id}", "查询当前 job 进度"),
        ],
        hidden={"job_id": job_id},
    )
