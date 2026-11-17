"""Progress and display formatting helpers."""


def format_seconds(value):
    try:
        seconds = int(value)
    except (TypeError, ValueError):
        return None
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    remain = seconds % 60
    if minutes < 60:
        return f"{minutes}分{remain}秒" if remain else f"{minutes}分钟"
    hours = minutes // 60
    minutes = minutes % 60
    if hours >= 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}天{hours}小时" if hours else f"{days}天"
    return f"{hours}小时{minutes}分钟" if minutes else f"{hours}小时"


def format_bytes(value):
    try:
        size = int(value)
    except (TypeError, ValueError):
        return "未知大小"
    units = ["B", "KB", "MB", "GB"]
    n = float(size)
    for unit in units:
        if n < 1024 or unit == units[-1]:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}B"
        n /= 1024
    return f"{size}B"


def format_progress_line(prog, status=None, *, include_job_id=None):
    """Convert an Open API progress snapshot into one WorkBuddy-friendly line."""
    prog = prog or {}
    pct = prog.get("percent")
    raw_stage = str(prog.get("stage") or "")
    raw_label = str(prog.get("stage_label") or raw_stage or "处理中")

    def _normalize_template_text(text):
        if not text:
            return text
        return (
            str(text)
            .replace("填充制式模板", "抽取制式模板")
            .replace("正在填充模板", "正在抽取制式模板")
            .replace("填充模板", "抽取制式模板")
        )

    label = _normalize_template_text(raw_label)
    if raw_stage in {"template", "templates"} or raw_label in {"template", "templates"}:
        label = "抽取制式模板"
    message = _normalize_template_text(prog.get("message") or "")
    current = prog.get("current_step")
    total = prog.get("total_steps")
    unit = prog.get("unit_label") or "项"
    current_label = prog.get("current_step_label") or ""

    stage_meta = []
    if pct is not None:
        stage_meta.append(f"{pct}%")
    if current is not None and total is not None:
        stage_meta.append(f"{current}/{total} {unit}")

    stage = f"已进入「{label}」阶段"
    if stage_meta:
        stage += f"（{'，'.join(stage_meta)}）"

    is_bid_generation = "生成" in str(label) or str(prog.get("stage") or "") in {
        "outline", "content", "export", "template", "templates", "requirements",
    }
    if status == "queued":
        head = "任务已提交，正在排队"
    elif status == "succeeded":
        head = "任务已完成"
    elif status == "failed":
        head = "任务已失败"
    elif status == "canceled":
        head = "任务已取消"
    elif is_bid_generation:
        head = "标书正在生成中"
    else:
        head = "任务正在处理"

    parts = [head, stage]
    if message and message != label:
        parts.append(str(message))
    if current_label:
        action = "写" if unit == "节" or "正文" in str(label) else "处理"
        parts.append(f"当前正在{action}「{current_label}」")
    elapsed = format_seconds(prog.get("elapsed_seconds"))
    remaining = format_seconds(prog.get("estimated_remaining_seconds"))
    if elapsed:
        parts.append(f"已用 {elapsed}")
    if remaining:
        parts.append(f"预计还需约 {remaining}")
    if status in ("queued", "running", None):
        parts.append("我会继续后台监听，完成后交付成品链接")
    elif status == "succeeded":
        parts.append("正在准备交付成品链接")

    line = "进度更新：" + "。".join(parts) + "。"
    if include_job_id:
        return f"任务 {include_job_id}：{line}"
    return line
