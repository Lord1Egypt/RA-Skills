"""
日常小助手 MCP Server — 核心逻辑模块

从 5 个源脚本中提取的纯函数，零外部依赖（仅标准库）。
所有函数接受 daily_dir: Path 参数，不硬编码任何路径。
支持中英文双语输出（lang="zh" / "en"）。

来源映射：
  - next_action.py   → parse_task, rank_tasks, generate_steps, format_*
  - overdue_check.py  → scan_overdue_files
  - daily_inherit.py  → find_latest_daily, extract_uncompleted_tasks, create_today_file
  - daily_review.py   → parse_all_tasks, generate_review
  - action_notify.py  → scan_split_needed
"""

import re
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# 国际化（i18n）
# ============================================================

I18N = {
    # ── 优先级标签 ──
    "priority_highest":     {"zh": "最高 ⏫",   "en": "Highest ⏫"},
    "priority_high":        {"zh": "高 🔼",     "en": "High 🔼"},
    "priority_medium":      {"zh": "普通",       "en": "Normal"},
    "priority_low":         {"zh": "低 🔽",     "en": "Low 🔽"},

    # ── 星期 ──
    "weekday_0": {"zh": "周一", "en": "Mon"},
    "weekday_1": {"zh": "周二", "en": "Tue"},
    "weekday_2": {"zh": "周三", "en": "Wed"},
    "weekday_3": {"zh": "周四", "en": "Thu"},
    "weekday_4": {"zh": "周五", "en": "Fri"},
    "weekday_5": {"zh": "周六", "en": "Sat"},
    "weekday_6": {"zh": "周日", "en": "Sun"},

    # ── deadline 标签 ──
    "no_deadline":          {"zh": "无 deadline",               "en": "No deadline"},
    "overdue_days":         {"zh": "已超期 {n} 天！",           "en": "Overdue by {n} days!"},
    "deadline_today":       {"zh": "今天！",                     "en": "Today!"},
    "deadline_tomorrow":    {"zh": "明天",                       "en": "Tomorrow"},
    "deadline_in_days":     {"zh": "{n} 天后",                   "en": "in {n} days"},

    # ── recommend_next ──
    "all_done":             {"zh": "🎉 今日任务清零！\n所有任务都已完成，干得漂亮！",
                             "en": "🎉 All tasks done!\nGreat job today!"},
    "do_this_now":          {"zh": "🎯 现在做这个（{time}）：",
                             "en": "🎯 Do this now ({time}):"},
    "est_time":             {"zh": "预计 {n}min",                "en": "est. {n}min"},
    "no_time_est":          {"zh": "未设定时间",                  "en": "no time estimate"},
    "deadline_label":       {"zh": "📅 Deadline: {label}",      "en": "📅 Deadline: {label}"},
    "priority_label":       {"zh": "🔥 优先级: {label}",        "en": "🔥 Priority: {label}"},
    "suggested_steps":      {"zh": "💡 建议步骤：",              "en": "💡 Suggested steps:"},
    "next_up":              {"zh": "⏭️ 做完之后：",              "en": "⏭️ Next up:"},
    "remaining_tasks":      {"zh": "📊 剩余 {n} 个任务",        "en": "📊 {n} tasks remaining"},
    "total_minutes":        {"zh": "，共约 {n}min",              "en": ", ~{n}min total"},

    # ── generate_steps ──
    "steps_write":          {"zh": ["打开相关文档/笔记", "花 5 分钟回顾之前的进展和大纲", "开始写作，先不追求完美"],
                             "en": ["Open related docs/notes", "Spend 5 min reviewing progress and outline", "Start writing — don't aim for perfection"]},
    "steps_search":         {"zh": ["明确搜索关键词和范围", "在目标平台上系统搜索", "整理结果到笔记中"],
                             "en": ["Define search keywords and scope", "Systematically search on target platforms", "Organize results into notes"]},
    "steps_organize":       {"zh": ["打开所有相关材料", "定义分类维度", "逐项归类并记录"],
                             "en": ["Open all related materials", "Define classification dimensions", "Categorize items and record"]},
    "steps_communicate":    {"zh": ["打开相关沟通工具", "组织要表达的要点", "发送并记录"],
                             "en": ["Open communication tool", "Organize key points", "Send and log"]},
    "steps_read":           {"zh": ["找到要阅读的材料", "带着问题阅读，标注重点", "写下 3 个关键要点"],
                             "en": ["Locate the reading material", "Read with questions in mind, highlight key parts", "Write down 3 key takeaways"]},
    "steps_default":        {"zh": ["明确完成标准", "执行第一个小步骤", "完成后检查是否达标"],
                             "en": ["Clarify the definition of done", "Execute the first small step", "Check if it meets the standard"]},

    # ── generate_review ──
    "review_title":         {"zh": "## 📊 日终回顾（自动生成 {date}）",
                             "en": "## 📊 Daily Review (auto-generated {date})"},
    "completion_rate":      {"zh": "**📈 完成率：** {done}/{total}（{pct}%）",
                             "en": "**📈 Completion rate:** {done}/{total} ({pct}%)"},
    "completed_header":     {"zh": "**✅ 已完成：**",            "en": "**✅ Completed:**"},
    "uncompleted_header":   {"zh": "**⬜ 未完成：**",            "en": "**⬜ Incomplete:**"},
    "time_stats":           {"zh": "**⏱️ 时间统计：**",          "en": "**⏱️ Time stats:**"},
    "completed_time":       {"zh": "- 已完成预估总时间：{n}min",  "en": "- Completed estimated time: {n}min"},
    "uncompleted_time":     {"zh": "- 未完成预估总时间：{n}min",  "en": "- Incomplete estimated time: {n}min"},
    "tomorrow_suggestion":  {"zh": "**💡 明日建议：**",           "en": "**💡 Tomorrow's suggestion:**"},
    "inherit_count":        {"zh": "- {n} 个未完成任务将被继承到明天",
                             "en": "- {n} incomplete tasks will carry over to tomorrow"},
    "inherit_time":         {"zh": "- 预计需要 {n}min 完成剩余任务",
                             "en": "- Estimated {n}min to finish remaining tasks"},
    "all_done_tomorrow":    {"zh": "- 今天全部完成！明天可以开始新的任务 🎉",
                             "en": "- All done today! Start fresh tomorrow 🎉"},

    # ── create_today_file ──
    "daily_title":          {"zh": "每日待办 - {date}",          "en": "Daily Tasks - {date}"},
    "daily_heading":        {"zh": "📅 {date} {weekday} 每日待办",
                             "en": "📅 {date} {weekday} Daily Tasks"},
    "section_tasks":        {"zh": "📥 今日任务",                "en": "📥 Today's Tasks"},
    "section_notes":        {"zh": "📝 备注",                    "en": "📝 Notes"},
    "section_review":       {"zh": "📊 日终回顾",                "en": "📊 End of Day Review"},
    "review_prompt":        {"zh": ["> *下班前填写*",
                                    "> - 完成了什么？",
                                    "> - 没完成什么？为什么？",
                                    "> - 明天最重要的事是？"],
                             "en": ["> *Fill before end of day*",
                                    "> - What was completed?",
                                    "> - What wasn't completed? Why?",
                                    "> - What's most important tomorrow?"]},

    # ── server.py 输出文本 ──
    "srv_no_daily_file":    {"zh": "⚠️ 今日待办文件不存在: {file}\n先运行 inherit_tasks 或手动创建今日文件。",
                             "en": "⚠️ Daily file not found: {file}\nRun inherit_tasks or create the file manually."},
    "srv_no_tasks_yet":     {"zh": "📝 今日还没有添加任务。打开 Daily/{file} 添加今天的任务吧。",
                             "en": "📝 No tasks added yet. Open Daily/{file} to add today's tasks."},
    "srv_file_not_exist":   {"zh": "⚠️ 文件不存在: Daily/{file}",
                             "en": "⚠️ File not found: Daily/{file}"},
    "srv_file_header":      {"zh": "📄 Daily/{file}",
                             "en": "📄 Daily/{file}"},
    "srv_already_exists":   {"zh": "⚠️ 今日文件已存在: {file}，不会覆盖。",
                             "en": "⚠️ Today's file already exists: {file}, will not overwrite."},
    "srv_no_previous":      {"zh": "📭 未找到之前的待办文件。已创建空白的 {file}。",
                             "en": "📭 No previous daily file found. Created blank {file}."},
    "srv_all_completed":    {"zh": "🎉 {src} 中所有任务已完成！已创建空白的 {file}。",
                             "en": "🎉 All tasks in {src} completed! Created blank {file}."},
    "srv_inherit_done":     {"zh": "✅ 已创建 {file}\n继承自: {src}（{marked} 个任务已标记为已继承）\n继承任务数: {count}",
                             "en": "✅ Created {file}\nInherited from: {src} ({marked} tasks marked as inherited)\nInherited tasks: {count}"},
    "srv_no_overdue":       {"zh": "✅ 没有超期任务（截至 {date}），所有待办都已完成！",
                             "en": "✅ No overdue tasks (as of {date}). All tasks completed!"},
    "srv_overdue_found":    {"zh": "⚠️ 发现 {files} 个超期文件，共 {tasks} 个未完成任务：",
                             "en": "⚠️ Found {files} overdue files with {tasks} incomplete tasks:"},
    "srv_overdue_file":     {"zh": "📄 {date}.md（{days}天前）",
                             "en": "📄 {date}.md ({days} days ago)"},
    "srv_overdue_tip":      {"zh": "💡 建议：运行 inherit_tasks 将未完成项带到今天。",
                             "en": "💡 Tip: Run inherit_tasks to bring incomplete tasks to today."},
    "srv_no_task_record":   {"zh": "📝 今日没有任何任务记录。",
                             "en": "📝 No task records for today."},
    "srv_review_written":   {"zh": "✅ 回顾已写入 Daily/{file}",
                             "en": "✅ Review written to Daily/{file}"},
    "srv_split_ok":         {"zh": "✅ {date} 的所有任务预估时间合理，无需拆分。",
                             "en": "✅ All tasks for {date} have reasonable time estimates."},
    "srv_split_too_long":   {"zh": "✂️ 以下 {n} 个任务超过 80min，建议拆分：",
                             "en": "✂️ {n} tasks exceed 80min, consider splitting:"},
    "srv_split_no_est":     {"zh": "📝 以下 {n} 个任务缺少预估时间：",
                             "en": "📝 {n} tasks missing time estimates:"},
    "srv_split_tip":        {"zh": "💡 建议让 AI 帮你拆分大任务为多个 ≤ 45min 的子任务。",
                             "en": "💡 Tip: Ask AI to split large tasks into ≤ 45min sub-tasks."},
    "srv_history_title":    {"zh": "📊 最近 7 天任务完成统计",
                             "en": "📊 Task completion stats — last 7 days"},
    "srv_history_hdr":      {"zh": ["日期", "完成", "未完成", "完成率"],
                             "en": ["Date", "Done", "Incomplete", "Rate"]},
    "srv_no_file":          {"zh": "无文件", "en": "No file"},
    "srv_no_tasks":         {"zh": "无任务", "en": "No tasks"},
}


def t(key: str, lang: str = "zh", **kwargs) -> str | list:
    """从 I18N 字典取翻译文本。支持 {var} 占位符。"""
    entry = I18N.get(key, {})
    text = entry.get(lang, entry.get("zh", key))
    if isinstance(text, str) and kwargs:
        text = text.format(**kwargs)
    return text


# ============================================================
# 常量（纯逻辑，不涉及语言）
# ============================================================

PRIORITY_WEIGHT = {
    "highest": 40,  # ⏫
    "high": 30,     # 🔼
    "medium": 20,   # （无标记）
    "low": 10,      # 🔽
}

PRIORITY_MAP = {
    "⏫": "highest",
    "🔼": "high",
    "🔽": "low",
}


def get_priority_label(priority: str, lang: str = "zh") -> str:
    """获取优先级的本地化标签。"""
    key = f"priority_{priority}"
    return t(key, lang)


def get_weekday(weekday_num: int, lang: str = "zh") -> str:
    """获取星期的本地化名称。"""
    return t(f"weekday_{weekday_num}", lang)


# ============================================================
# 任务解析与排序（来源: next_action.py）
# ============================================================

def parse_task(line: str, today: datetime = None) -> dict | None:
    """
    解析一行任务文本，提取描述、预估时间、deadline、优先级。
    只处理未完成任务（- [ ] 开头）。
    """
    today = today or datetime.now()
    stripped = line.strip()

    if not stripped.startswith("- [ ] "):
        return None

    raw_text = stripped[6:]

    # 提取预估时间 ⏱️XXmin
    time_match = re.search(r"⏱️\s*(\d+)\s*min", raw_text)
    est_minutes = int(time_match.group(1)) if time_match else None

    # 提取 deadline 📅 YYYY-MM-DD
    deadline_match = re.search(r"📅\s*(\d{4}-\d{2}-\d{2})", raw_text)
    deadline = None
    days_until = None
    if deadline_match:
        deadline = deadline_match.group(1)
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        today_date = today.date() if hasattr(today, "date") else today
        days_until = (deadline_date - today_date).days

    # 提取优先级 ⏫ 🔼 🔽
    priority = "medium"
    for emoji, level in PRIORITY_MAP.items():
        if emoji in raw_text:
            priority = level
            break

    # 清理描述文本
    desc = raw_text
    desc = re.sub(r"\s*⏱️\s*\d+\s*min", "", desc)
    desc = re.sub(r"\s*📅\s*\d{4}-\d{2}-\d{2}", "", desc)
    for emoji in PRIORITY_MAP:
        desc = desc.replace(emoji, "")
    desc = desc.replace("🔄", "").strip()

    return {
        "raw": stripped,
        "description": desc,
        "est_minutes": est_minutes,
        "deadline": deadline,
        "days_until": days_until,
        "priority": priority,
    }


def rank_tasks(tasks: list[dict]) -> list[dict]:
    """按优先级和 deadline 紧迫度排序。第一个 = 最应该做的。"""

    def sort_key(task):
        priority_score = PRIORITY_WEIGHT.get(task["priority"], 20)
        deadline_score = 0
        if task["days_until"] is not None:
            if task["days_until"] < 0:
                deadline_score = 100 + abs(task["days_until"])
            elif task["days_until"] == 0:
                deadline_score = 80
            elif task["days_until"] <= 1:
                deadline_score = 60
            elif task["days_until"] <= 3:
                deadline_score = 40
            elif task["days_until"] <= 7:
                deadline_score = 20
            else:
                deadline_score = 10
        return -(priority_score + deadline_score)

    return sorted(tasks, key=sort_key)


def generate_steps(task: dict, lang: str = "zh") -> list[str]:
    """基于任务描述生成建议步骤（简单关键词匹配）。"""
    desc = task["description"]

    if any(kw in desc for kw in ["写", "撰写", "完成", "write", "draft"]):
        return t("steps_write", lang)
    elif any(kw in desc for kw in ["收集", "找", "搜索", "查", "search", "find", "research"]):
        return t("steps_search", lang)
    elif any(kw in desc for kw in ["整理", "归类", "分类", "梳理", "organize", "sort", "categorize"]):
        return t("steps_organize", lang)
    elif any(kw in desc for kw in ["回复", "发送", "邮件", "联系", "reply", "send", "email", "contact"]):
        return t("steps_communicate", lang)
    elif any(kw in desc for kw in ["读", "阅读", "看", "学习", "read", "study", "learn"]):
        return t("steps_read", lang)
    else:
        return t("steps_default", lang)


def format_deadline_label(days_until: int | None, deadline: str | None, lang: str = "zh") -> str:
    """格式化 deadline 显示。"""
    if days_until is None or deadline is None:
        return t("no_deadline", lang)
    if days_until < 0:
        return f"{deadline}（{t('overdue_days', lang, n=abs(days_until))}）"
    elif days_until == 0:
        return f"{deadline}（{t('deadline_today', lang)}）"
    elif days_until == 1:
        return f"{deadline}（{t('deadline_tomorrow', lang)}）"
    else:
        return f"{deadline}（{t('deadline_in_days', lang, n=days_until)}）"


def format_recommendation(tasks: list[dict], today: datetime = None, lang: str = "zh") -> str:
    """格式化推荐输出。"""
    today = today or datetime.now()

    if not tasks:
        return t("all_done", lang)

    top = tasks[0]
    time_label = t("est_time", lang, n=top["est_minutes"]) if top["est_minutes"] else t("no_time_est", lang)
    deadline_label = format_deadline_label(top["days_until"], top["deadline"], lang)
    priority_label = get_priority_label(top["priority"], lang)
    steps = generate_steps(top, lang)

    lines = [
        "",
        t("do_this_now", lang, time=time_label),
        f"{top['description']}",
        "",
        t("deadline_label", lang, label=deadline_label),
        t("priority_label", lang, label=priority_label),
        "",
        t("suggested_steps", lang),
    ]
    for i, step in enumerate(steps, 1):
        lines.append(f"  {i}. {step}")

    if len(tasks) > 1:
        nxt = tasks[1]
        nxt_time = f"（{nxt['est_minutes']}min）" if nxt["est_minutes"] else ""
        lines.extend(["", t("next_up", lang), f"  → {nxt['description']}{nxt_time}"])

    remaining = len(tasks)
    total_minutes = sum(t_item["est_minutes"] for t_item in tasks if t_item["est_minutes"])
    lines.append("")
    line = t("remaining_tasks", lang, n=remaining)
    if total_minutes:
        line += t("total_minutes", lang, n=total_minutes)
    lines.append(line)

    return "\n".join(lines)


# ============================================================
# 超期检测（来源: overdue_check.py）
# ============================================================

def scan_overdue_files(daily_dir: Path, today: datetime = None) -> list[dict]:
    """
    扫描 Daily 文件夹，找出所有超期文件。
    超期 = 文件日期 < 今天 且 包含未完成任务。
    """
    today = today or datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

    overdue = []
    for f in sorted(daily_dir.iterdir()):
        if not f.is_file() or not date_pattern.match(f.name):
            continue
        file_date = f.stem
        if file_date >= today_str:
            continue

        content = f.read_text(encoding="utf-8")
        uncompleted = [
            line.strip()
            for line in content.split("\n")
            if line.strip().startswith("- [ ] ")
        ]

        if uncompleted:
            file_dt = datetime.strptime(file_date, "%Y-%m-%d")
            days_ago = (today - file_dt).days
            overdue.append({
                "file": f,
                "date": file_date,
                "days_ago": days_ago,
                "uncompleted": uncompleted,
            })

    overdue.sort(key=lambda x: x["date"], reverse=True)
    return overdue


# ============================================================
# 待办继承（来源: daily_inherit.py）
# ============================================================

def find_latest_daily(daily_dir: Path, before_date: datetime = None) -> Path | None:
    """在 Daily 文件夹中找到日期最新的待办文件（before_date 之前）。"""
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
    today_str = (before_date or datetime.now()).strftime("%Y-%m-%d")

    candidates = [
        f for f in daily_dir.iterdir()
        if f.is_file() and date_pattern.match(f.name) and f.stem < today_str
    ]

    if not candidates:
        return None

    candidates.sort(key=lambda f: f.name, reverse=True)
    return candidates[0]


def extract_uncompleted_tasks(file_path: Path) -> list[str]:
    """从待办文件中提取所有未完成的任务行。"""
    content = file_path.read_text(encoding="utf-8")
    return [
        line.strip()
        for line in content.split("\n")
        if line.strip().startswith("- [ ] ")
    ]


def create_today_file(
    daily_dir: Path,
    today: datetime,
    inherited_tasks: list[str],
    source_date: str = None,
    lang: str = "zh",
) -> Path:
    """创建今天的待办文件。"""
    date_str = today.strftime("%Y-%m-%d")
    weekday = get_weekday(today.weekday(), lang)
    file_path = daily_dir / f"{date_str}.md"

    yaml_lines = [
        "---",
        f"title: {t('daily_title', lang, date=date_str)}",
        f"date: {date_str}",
    ]
    if source_date:
        yaml_lines.append(f"inherited_from: {source_date}")
    yaml_lines.append("---")

    heading = t("daily_heading", lang, date=date_str, weekday=weekday)
    body_lines = ["", f"# {heading}", "", f"## {t('section_tasks', lang)}", ""]

    if inherited_tasks:
        for task in inherited_tasks:
            task_text = task[6:]  # 去掉 "- [ ] "
            task_text = task_text.replace(" 🔄", "").replace("🔄", "").rstrip()
            body_lines.append(f"- [ ] {task_text} 🔄")
        body_lines.append("")

    body_lines.extend([
        "", f"## {t('section_notes', lang)}", "", "", "",
        f"## {t('section_review', lang)}", "",
    ])
    body_lines.extend(t("review_prompt", lang))

    content = "\n".join(yaml_lines) + "\n" + "\n".join(body_lines) + "\n"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def mark_tasks_inherited(file_path: Path, target_date: str) -> int:
    """将源文件中的未完成任务标记为已继承。

    - [ ] 任务  →  - [>] 任务 ➡️ YYYY-MM-DD

    已标记 [>] 的任务不会被 check_overdue / recommend_next 等函数匹配，
    从而避免继承后的重复计数。

    返回标记的任务数量。
    """
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("- [ ] "):
            indent = line[: len(line) - len(line.lstrip())]
            task_text = stripped[6:]
            lines[i] = f"{indent}- [>] {task_text} ➡️ {target_date}"
            count += 1

    if count > 0:
        file_path.write_text("\n".join(lines), encoding="utf-8")

    return count


# ============================================================
# 日终回顾（来源: daily_review.py）
# ============================================================

def parse_all_tasks(content: str) -> tuple[list[dict], list[dict]]:
    """解析 Daily 文件中的所有任务（已完成 + 未完成）。"""
    completed = []
    uncompleted = []

    for line in content.split("\n"):
        stripped = line.strip()
        is_done = stripped.startswith("- [x] ")
        is_todo = stripped.startswith("- [ ] ")

        if not is_done and not is_todo:
            continue

        raw_text = stripped[6:]

        time_match = re.search(r"⏱️\s*(\d+)\s*min", raw_text)
        est_minutes = int(time_match.group(1)) if time_match else None

        desc = raw_text
        desc = re.sub(r"\s*⏱️\s*\d+\s*min", "", desc)
        desc = re.sub(r"\s*📅\s*\d{4}-\d{2}-\d{2}", "", desc)
        desc = re.sub(r"\s*✅\s*\d{4}-\d{2}-\d{2}", "", desc)
        for emoji in ["⏫", "🔼", "🔽", "🔄"]:
            desc = desc.replace(emoji, "")
        desc = desc.strip()

        task = {"description": desc, "est_minutes": est_minutes}
        if is_done:
            completed.append(task)
        else:
            uncompleted.append(task)

    return completed, uncompleted


def generate_review(
    completed: list[dict], uncompleted: list[dict], today_str: str, lang: str = "zh"
) -> str:
    """生成日终回顾 markdown 内容。"""
    total = len(completed) + len(uncompleted)
    pct = round(len(completed) / total * 100) if total > 0 else 0

    completed_min = sum(t_item["est_minutes"] for t_item in completed if t_item["est_minutes"])
    uncompleted_min = sum(t_item["est_minutes"] for t_item in uncompleted if t_item["est_minutes"])

    lines = [
        t("review_title", lang, date=today_str),
        "",
        t("completion_rate", lang, done=len(completed), total=total, pct=pct),
        "",
    ]

    if completed:
        lines.append(t("completed_header", lang))
        for item in completed:
            time_str = f"（{item['est_minutes']}min）" if item["est_minutes"] else ""
            lines.append(f"- {item['description']}{time_str}")
        lines.append("")

    if uncompleted:
        lines.append(t("uncompleted_header", lang))
        for item in uncompleted:
            time_str = f"（{item['est_minutes']}min）" if item["est_minutes"] else ""
            lines.append(f"- {item['description']}{time_str}")
        lines.append("")

    lines.extend([
        t("time_stats", lang),
        t("completed_time", lang, n=completed_min),
        t("uncompleted_time", lang, n=uncompleted_min),
        "",
    ])

    lines.append(t("tomorrow_suggestion", lang))
    if uncompleted:
        lines.append(t("inherit_count", lang, n=len(uncompleted)))
        if uncompleted_min > 0:
            lines.append(t("inherit_time", lang, n=uncompleted_min))
    else:
        lines.append(t("all_done_tomorrow", lang))

    return "\n".join(lines)


# ============================================================
# 拆分检测（来源: action_notify.py）
# ============================================================

def scan_split_needed(daily_dir: Path, today: datetime) -> list[dict]:
    """
    检测今日 Daily 文件中需要拆分的任务。
    规则：⏱️ > 80min → 建议拆分；无 ⏱️ → 建议补上。
    """
    today_str = today.strftime("%Y-%m-%d")
    today_file = daily_dir / f"{today_str}.md"

    if not today_file.exists():
        return []

    content = today_file.read_text(encoding="utf-8")
    issues = []

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("- [ ] "):
            continue

        raw_text = stripped[6:]
        time_match = re.search(r"⏱️\s*(\d+)\s*min", raw_text)

        desc = raw_text
        desc = re.sub(r"\s*⏱️\s*\d+\s*min", "", desc)
        desc = re.sub(r"\s*📅\s*\d{4}-\d{2}-\d{2}", "", desc)
        for emoji in ["⏫", "🔼", "🔽", "🔄"]:
            desc = desc.replace(emoji, "")
        desc = desc.strip()

        if time_match:
            minutes = int(time_match.group(1))
            if minutes > 80:
                issues.append({"description": desc, "minutes": minutes, "type": "too_long"})
        else:
            issues.append({"description": desc, "minutes": None, "type": "no_estimate"})

    return issues
