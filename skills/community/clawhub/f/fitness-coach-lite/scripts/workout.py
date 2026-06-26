#!/usr/bin/env python3
"""
workout-tracker 主脚本
用法:
  python3 workout.py plan set '<json>'
  python3 workout.py plan import <path>
  python3 workout.py plan view
  python3 workout.py start
  python3 workout.py history [days]
  python3 workout.py reset-today
  python3 workout.py status        # 查看当前训练进度（供agent调用）
  python3 workout.py complete-set <reps>   # 记录一组完成
  python3 workout.py skip-action             # 跳过当前动作
"""

import json
import os
import sys
from datetime import datetime, date, timezone, timedelta

# 严格从环境变量 HERMES_SESSION_START 解析真实日期（UTC+8）
# 格式示例: "2026-04-21T05:15:00+08:00"
def _get_session_dt():
    raw = os.environ.get("HERMES_SESSION_START", "")
    if raw:
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except Exception:
            pass
    # Fallback：用 UTC+8（Asia/Shanghai）的当前时间
    utc8 = timezone(timedelta(hours=8))
    return datetime.now(utc8)

def _get_session_dt_local():
    """当前时刻的UTC+8 datetime（用于timestamp记录）"""
    dt = _get_session_dt()
    utc8 = timezone(timedelta(hours=8))
    return dt.astimezone(utc8)

def _get_session_date():
    """从session时间戳获取真实日期（UTC+8），fallback到系统时间"""
    return _get_session_dt_local().date()

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PLAN_FILE = os.path.join(DATA_DIR, "plan.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
BODY_FILE = os.path.join(DATA_DIR, "body_status.json")
CURRENT_FILE = os.path.join(DATA_DIR, ".current_workout.json")

# ─── 基础工具 ───────────────────────────────────────────────

def load_json(path, default=None):
    if not os.path.exists(path):
        return default or {}
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_today_name():
    return _get_session_date().strftime("%A").lower()

# ─── 计划管理 ───────────────────────────────────────────────

def plan_parse(text: str):
    """将文字描述转为plan JSON（实际转换由agent完成）"""
    return {
        "status": "parse_needed",
        "text": text
    }

def plan_set(json_str: str):
    """从JSON字符串设置计划"""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return f"JSON解析失败: {e}"
    if "schedule" not in data and "sequence" not in data:
        return "计划必须包含 'schedule' 或 'sequence' 字段"
    save_json(PLAN_FILE, data)
    return f"运动计划已保存 (共 {len(data.get('schedule', {}))} 天 / {len(data.get('sequence', []))} 组)"

def plan_import(file_path: str):
    """从本地文件导入计划"""
    if not os.path.exists(file_path):
        return f"文件不存在: {file_path}"
    try:
        with open(file_path) as f:
            data = json.load(f)
    except Exception as e:
        return f"读取失败: {e}"
    if "schedule" not in data and "sequence" not in data:
        return "计划必须包含 'schedule' 或 'sequence' 字段"
    save_json(PLAN_FILE, data)
    return f"计划已从 {file_path} 导入"

def plan_view():
    """查看当前计划"""
    plan = load_json(PLAN_FILE)
    if not plan:
        return "当前没有运动计划，请用「运动计划 <文字>」导入"
    name = plan.get("name", "未命名计划")
    mode = plan.get("mode", "weekly")
    note = plan.get("note", "")
    lines = [f"📋 **{name}** ({mode}模式)"]
    if note:
        lines.append(f"  {note}")
    lines.append("")
    if mode == "sequence":
        for i, day_plan in enumerate(plan.get("sequence", [])):
            lines.append(f"  第{i+1}天: {', '.join(a['name'] for a in day_plan)}")
    else:
        today_day = get_today_name().capitalize()
        day_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        schedule = plan.get("schedule", {})
        # 按固定顺序输出
        for day in day_order:
            if day not in schedule:
                continue
            day_data = schedule[day]
            marker = "👉 " if day == today_day.lower() else "   "
            if isinstance(day_data, dict):
                # 双版本格式
                goal = day_data.get("goal", "")
                versions = []
                for key in day_data:
                    if key not in ("goal", "duration", "note"):
                        items = day_data[key]
                        if isinstance(items, list) and items:
                            versions.append(f"{key}: {', '.join(a['name'] for a in items)}")
                lines.append(f"{marker}{day.capitalize()} 🎯{goal}")
                for v in versions:
                    lines.append(f"    {v}")
            elif isinstance(day_data, list):
                # 普通格式
                if day_data:
                    lines.append(f"{marker}{day.capitalize()}: {', '.join(a['name'] for a in day_data)}")
                else:
                    lines.append(f"{marker}{day.capitalize()}: 休息")
            else:
                lines.append(f"{marker}{day.capitalize()}: {day_data}")
    return "\n".join(lines)

# ─── 获取今日训练 ───────────────────────────────────────────

def get_today_workout(version_hint=None):
    """根据今天日期获取今日训练内容，支持新版每组级格式
    version_hint: 'long' / 'short' / None（None时返回含版本信息的结构）
    """
    plan = load_json(PLAN_FILE)
    if not plan:
        return None
    mode = plan.get("mode", "weekly")
    if mode == "sequence":
        seq = plan.get("sequence", [])
        if not seq:
            return None
        day_of_year = _get_session_date().timetuple().tm_yday
        idx = (day_of_year - 1) % len(seq)
        return seq[idx]
    else:
        day_name = get_today_name()
        schedule = plan.get("schedule", {})
        day_plan = schedule.get(day_name, [])
        if not day_plan:
            return None
        # 检查是否是 dict（双版本格式）
        if isinstance(day_plan, dict):
            if version_hint == "long":
                for key in ["30min", "30-40min"]:
                    if key in day_plan:
                        return day_plan[key]
                return day_plan.get(list(day_plan.keys())[0]) if day_plan else []
            elif version_hint == "short":
                for key in ["15min", "15-20min"]:
                    if key in day_plan:
                        return day_plan[key]
                return day_plan.get(list(day_plan.keys())[0]) if day_plan else []
            else:
                return {"_dual_version": True, "day_plan": day_plan, "goal": day_plan.get("goal", "")}
        # 检查是否是新版每组级格式（每个动作含sets数组）
        first = day_plan[0] if day_plan else None
        if isinstance(first, dict) and "sets" in first:
            return day_plan
        return day_plan

# ─── 训练状态 ───────────────────────────────────────────────

def start_workout(version_hint=None):
    """初始化训练状态
    version_hint: 'long' / 'short' / None
    """
    # 如果已有hint，先尝试直接获取（避免双版字典干扰）
    if version_hint:
        workout = get_today_workout(version_hint)
        if isinstance(workout, list) and workout:
            return _start_workout_common(workout)
    raw = get_today_workout()
    if raw is None:
        return "今天没有训练计划！"
    if isinstance(raw, str):
        day_name = get_today_name().capitalize()
        return f"今天（{day_name}）是休息日～"
    if isinstance(raw, dict) and raw.get("_dual_version"):
        # 双版本计划，需要用户选择
        dv = raw["day_plan"]
        goal = dv.get("goal", "")
        lines = [f"🏋️ 今日训练：{goal}\n"]
        long_key = next((k for k in dv if k in ("30min", "30-40min")), None)
        short_key = next((k for k in dv if k in ("15min", "15-20min")), None)
        if version_hint == "long" and long_key:
            workout = dv[long_key]
            return _start_workout_common(workout)
        elif version_hint == "short" and short_key:
            workout = dv[short_key]
            return _start_workout_common(workout)
        # 询问用户选择
        lines.append("今天有两个版本可选：")
        if long_key:
            lines.append(f"  🕐 **{long_key}**：{', '.join(a['name'] for a in dv[long_key])}")
        if short_key:
            lines.append(f"  ⚡ **{short_key}**：{', '.join(a['name'] for a in dv[short_key])}")
        lines.append(f"\n请回复：「30分钟」或「15分钟」（或直接说「长」「短」）")
        return "\n".join(lines)
    if isinstance(raw, list):
        return _start_workout_common(raw)
    return f"无法解析训练计划: {raw}"

def _action_to_steps(workout):
    """将动作列表展开为单个步骤列表，每步=[动作名, set_index, weight_kg, reps]"""
    steps = []
    for action in workout:
        name = action["name"]
        sets = action.get("sets", [])
        for i, s in enumerate(sets):
            if isinstance(s, dict):
                weight = s.get("weight_kg")
                reps = s.get("reps")
                hold = s.get("hold_secs")
            else:
                weight = action.get("weight_kg")
                reps = s if isinstance(s, int) else s.get("reps")
                hold = s.get("hold_secs") if isinstance(s, dict) else None
            steps.append({"name": name, "set_idx": i, "weight_kg": weight, "reps": reps, "hold_secs": hold,
                           "dropset": action.get("last_set_dropset") and i == len(sets)-1})
    return steps

def _steps_summary(workout):
    """生成动作摘要（每动作一行）"""
    lines = []
    for action in workout:
        name = action["name"]
        sets = action.get("sets", [])
        weights = []
        reps_list = []
        for s in sets:
            if isinstance(s, dict):
                w = str(s.get("weight_kg", "")) if s.get("weight_kg") else "自重"
                r = s.get("reps", "")
            else:
                w = str(action.get("weight_kg", "")) if action.get("weight_kg") else "自重"
                r = s if isinstance(s, int) else s.get("reps", "")
            if w not in weights:
                weights.append(w)
            if str(r) not in reps_list:
                reps_list.append(str(r))
        w_str = weights[0] if len(weights) == 1 else f"{min(weights)}-{max(weights)}"
        r_str = reps_list[0] if len(reps_list) == 1 else f"{min(map(int,reps_list))}-{max(map(int,reps_list))}"
        dropset = " 🔥" if action.get("last_set_dropset") else ""
        lines.append(f"  **{name}** {w_str}kg × {r_str} × {len(sets)}组{dropset}")
    return lines

def _start_workout_common(workout):
    """通用的开始训练逻辑（新版每组级）"""
    if not workout:
        return "今天没有训练动作！"
    steps = _action_to_steps(workout)
    state = {
        "started_at": _get_session_dt_local().isoformat(),
        "date": str(_get_session_date()),
        "workout": workout,
        "steps": steps,
        "current_step": 0,
        "completed": [],  # [{"name", "weight_kg", "reps", "hold_secs", "actual_reps", "skipped"}]
    }
    save_json(CURRENT_FILE, state)
    lines = ["🏋️ 训练开始！\n"]
    lines.append("动作列表：")
    lines.extend(_steps_summary(workout))
    lines.append(f"\n共 {len(steps)} 个步骤，确认开始？")
    return "\n".join(lines)

def workout_status():
    """返回当前训练进度（供agent展示）"""
    state = load_json(CURRENT_FILE)
    if not state:
        return None
    steps = state.get("steps", [])
    current = state.get("current_step", 0)
    if current >= len(steps):
        return None  # 已完成
    step = steps[current]
    return {
        "current_step": current,
        "total_steps": len(steps),
        "name": step["name"],
        "weight_kg": step.get("weight_kg"),
        "reps": step.get("reps"),
        "hold_secs": step.get("hold_secs"),
        "set_idx": step.get("set_idx"),
        "dropset": step.get("dropset"),
        "completed": state.get("completed", [])
    }

def complete_set(actual_reps: int):
    """记录当前步骤完成"""
    state = load_json(CURRENT_FILE)
    if not state:
        return "没有正在进行的训练"
    steps = state.get("steps", [])
    current = state.get("current_step", 0)
    if current >= len(steps):
        return "所有步骤已完成"
    step = steps[current]
    record = {
        "name": step["name"],
        "weight_kg": step.get("weight_kg"),
        "reps": step.get("reps"),
        "hold_secs": step.get("hold_secs"),
        "actual_reps": actual_reps,
        "skipped": False
    }
    state["completed"].append(record)
    state["current_step"] = current + 1
    save_json(CURRENT_FILE, state)
    if state["current_step"] >= len(steps):
        return finish_workout()
    next_step = steps[state["current_step"]]
    w = f"{next_step['weight_kg']}kg" if next_step.get("weight_kg") else "自重"
    r = next_step.get("reps", "?")
    dropset = " 🔥" if next_step.get("dropset") else ""
    return f"✅ 完成！\n⏭️ 下一步：**{next_step['name']}** {w} × {r}{dropset}"

def skip_action():
    """跳过当前步骤"""
    state = load_json(CURRENT_FILE)
    if not state:
        return "没有正在进行的训练"
    steps = state.get("steps", [])
    current = state.get("current_step", 0)
    if current >= len(steps):
        return "所有步骤已完成"
    step = steps[current]
    record = {
        "name": step["name"],
        "weight_kg": step.get("weight_kg"),
        "reps": step.get("reps"),
        "hold_secs": step.get("hold_secs"),
        "actual_reps": 0,
        "skipped": True
    }
    state["completed"].append(record)
    state["current_step"] = current + 1
    save_json(CURRENT_FILE, state)
    if state["current_step"] >= len(steps):
        return finish_workout()
    next_step = steps[state["current_step"]]
    w = f"{next_step['weight_kg']}kg" if next_step.get("weight_kg") else "自重"
    r = next_step.get("reps", "?")
    dropset = " 🔥" if next_step.get("dropset") else ""
    return f"⏭️ 已跳过 **{step['name']}**\n下一个：**{next_step['name']}** {w} × {r}{dropset}"

def finish_workout():
    """完成训练，保存到历史"""
    state = load_json(CURRENT_FILE)
    if not state:
        return "没有正在进行的训练"
    history = load_json(HISTORY_FILE, [])
    record = {
        "date": state["date"],
        "started_at": state["started_at"],
        "finished_at": _get_session_dt_local().isoformat(),
        "completed": state.get("completed", [])
    }
    history = [h for h in history if h.get("date") != state["date"]]
    history.insert(0, record)
    save_json(HISTORY_FILE, history)
    os.remove(CURRENT_FILE)
    lines = ["🏁 **训练完成！**\n"]
    # 按动作分组显示
    by_action = {}
    for c in record["completed"]:
        name = c["name"]
        if name not in by_action:
            by_action[name] = {"name": name, "sets": []}
        by_action[name]["sets"].append(c)
    for name, data in by_action.items():
        sets = data["sets"]
        done = [s for s in sets if not s.get("skipped")]
        skip = [s for s in sets if s.get("skipped")]
        total_reps = sum(s.get("actual_reps", 0) for s in done)
        w = sets[0].get("weight_kg") if sets[0].get("weight_kg") else 0
        if skip:
            lines.append(f"  ✅ {name} {w}kg: {len(done)}/{len(sets)}组 ({total_reps}次) 【跳过{len(skip)}组】")
        elif len(done) == len(sets):
            lines.append(f"  ✅ {name} {w}kg: {len(done)}组 ({total_reps}次)")
        else:
            lines.append(f"  ⚠️ {name} {w}kg: {len(done)}/{len(sets)}组 ({total_reps}次)")
    lines.append(f"\n⏱️ 用时: {get_duration(state.get('started_at',''), record['finished_at'])}")
    return "\n".join(lines)

def get_duration(start: str, end: str):
    try:
        s = datetime.fromisoformat(start)
        e = datetime.fromisoformat(end)
        mins = int((e - s).total_seconds() / 60)
        return f"{mins}分钟"
    except:
        return "—"

def reset_today():
    """重置今日训练（兼容新旧history格式）"""
    if os.path.exists(CURRENT_FILE):
        os.remove(CURRENT_FILE)
    today = str(_get_session_date())
    hist_data = load_json(HISTORY_FILE, {})
    if isinstance(hist_data, dict) and "records" in hist_data:
        hist_data["records"] = [r for r in hist_data["records"] if r.get("date") != today]
        save_json(HISTORY_FILE, hist_data)
    elif isinstance(hist_data, list):
        hist_data = [h for h in hist_data if h.get("date") != today]
        save_json(HISTORY_FILE, hist_data)
    return "今日记录已清除"

def reset_date(target_date: str):
    """重置指定日期的训练记录（兼容新旧history格式）"""
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return f"日期格式错误，请使用 YYYY-MM-DD，如 2026-04-20"
    hist_data = load_json(HISTORY_FILE, {})
    removed = 0
    if isinstance(hist_data, dict) and "records" in hist_data:
        before = len(hist_data["records"])
        hist_data["records"] = [r for r in hist_data["records"] if r.get("date") != target_date]
        removed = before - len(hist_data["records"])
        save_json(HISTORY_FILE, hist_data)
    elif isinstance(hist_data, list):
        before = len(hist_data)
        hist_data = [h for h in hist_data if h.get("date") != target_date]
        removed = before - len(hist_data)
        save_json(HISTORY_FILE, hist_data)
    if removed == 0:
        return f"{target_date} 没有训练记录"
    return f"{target_date} 的记录已清除（{removed}条）"

def add_record(date_str: str, completed_list: list, skipped_list: list = None):
    """手动添加某日期的训练记录（兼容新旧格式）
    completed_list: [{"name": "俯卧撑", "weight_kg": null, "sets": [{"reps": 15}, {"reps": 12}]}]
    skipped_list: ["动作名", ...]
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return f"日期格式错误，请使用 YYYY-MM-DD"
    # 构建 workout_data（新格式）
    exercises = []
    for item in completed_list:
        name = item.get("name", "?")
        weight = item.get("weight_kg")
        sets_raw = item.get("sets", [])
        new_sets = []
        for s in sets_raw:
            if isinstance(s, int):
                new_sets.append({"reps": s})
            elif isinstance(s, dict):
                new_sets.append({"reps": s.get("reps", 0), "actual_reps": s.get("reps")})
            else:
                new_sets.append({"reps": s})
        exercises.append({"name": name, "weight_kg": weight, "sets": new_sets})
    workout_data = {"exercises": exercises, "summary": "", "note": ""}
    _history_add(date_str, "workout", workout_data=workout_data)
    return f"{date_str} 记录已保存：{', '.join(item['name'] for item in completed_list)}"
# ─── 历史记录 ───────────────────────────────────────────────

def show_history(days: int = 30):
    """显示训练历史表格（兼容新旧格式）"""
    hist_data = load_json(HISTORY_FILE, [])
    if isinstance(hist_data, dict):
        records = hist_data.get("records", [])
    else:
        records = hist_data  # 旧格式是数组
    cutoff_date = (_get_session_dt_local() - __import__('datetime').timedelta(days=days-1)).strftime("%Y-%m-%d")
    # 过滤 workout 类型
    workouts = [r for r in records if r.get("date", "") >= cutoff_date and r.get("type") == "workout"]
    if not workouts:
        return f"近{days}天没有训练记录"
    lines = [f"📊 **训练历史（近{days}天）**\n"]
    lines.append("| 日期 | 完成动作 |")
    lines.append("|------|---------|")
    for h in workouts:
        d = h.get("date", "—")
        wd = h.get("workout", {})
        exercises = wd.get("exercises", [])
        if exercises:
            parts = []
            for e in exercises:
                w_str = f"{e.get('weight_kg','')}kg" if e.get("weight_kg") else "自重"
                parts.append(f"{e['name']}({w_str})✅{len(e.get('sets',[]))}")
            action_str = "; ".join(parts)
        else:
            action_str = wd.get("summary", "—")
        lines.append(f"| {d} | {action_str} |")
    return "\n".join(lines)

def history_table(days: int = 30):
    """返回结构化历史数据供agent渲染"""
    hist_data = load_json(HISTORY_FILE, [])
    if isinstance(hist_data, dict):
        records = hist_data.get("records", [])
    else:
        records = hist_data
    cutoff_date = (_get_session_dt_local() - __import__('datetime').timedelta(days=days-1)).strftime("%Y-%m-%d")
    recent = [h for h in records if h.get("date", "") >= cutoff_date]
    if not recent:
        return None
    return recent

def _history_add(date_str: str, record_type: str, workout_data=None, status=None, detail=None, reason=None):
    """向history.json追加记录（新版统一格式，自动迁移旧数据）"""
    raw = load_json(HISTORY_FILE, None)
    now = _get_session_dt_local().isoformat()

    # 首次写入：如果是 None（旧文件不存在）或 list（旧格式），迁移为新格式
    if raw is None:
        hist_data = {"records": [], "plan_versions": [], "snapshots": []}
    elif isinstance(raw, list):
        # 旧格式是数组，每项是 workout 记录，转为新 records
        hist_data = {
            "records": [{"date": r.get("date"), "type": "workout", "logged_at": r.get("started_at", now), "workout": _normalize_workout_legacy(r)} for r in raw],
            "plan_versions": [],
            "snapshots": []
        }
    elif isinstance(raw, dict):
        hist_data = raw
        if "records" not in hist_data:
            hist_data["records"] = []
        if "plan_versions" not in hist_data:
            hist_data["plan_versions"] = []
        if "snapshots" not in hist_data:
            hist_data["snapshots"] = []
    else:
        hist_data = {"records": [], "plan_versions": [], "snapshots": []}

    if record_type == "workout":
        record = {
            "date": date_str,
            "type": "workout",
            "logged_at": now,
            "workout": workout_data or {}
        }
        # 兼容旧格式：如果传入的是旧格式的 completed 列表
        if isinstance(workout_data, dict) and "completed" in workout_data:
            record["workout"] = _normalize_workout_legacy(workout_data)
        hist_data["records"] = [r for r in hist_data["records"] if not (r.get("date") == date_str and r.get("type") == "workout")]
        hist_data["records"].insert(0, record)
    elif record_type == "status":
        record = {
            "date": date_str,
            "type": "status",
            "logged_at": now,
            "status": status or "normal",
            "detail": detail or ""
        }
        hist_data["records"] = [r for r in hist_data["records"] if not (r.get("date") == date_str and r.get("type") == "status")]
        hist_data["records"].insert(0, record)
    elif record_type == "plan_change":
        version_entry = {
            "date": date_str,
            "type": "plan_change",
            "logged_at": now,
            "reason": reason or ""
        }
        hist_data["plan_versions"].insert(0, version_entry)
    elif record_type == "snapshot":
        hist_data["snapshots"].insert(0, record)

    save_json(HISTORY_FILE, hist_data)

def _normalize_workout_legacy(data: dict) -> dict:
    """将旧格式 workout 数据转换为新格式"""
    completed = data.get("completed", [])
    exercises = {}
    for c in completed:
        name = c.get("name", "?")
        if name not in exercises:
            exercises[name] = {"name": name, "weight_kg": c.get("weight_kg"), "sets": []}
        exercises[name]["sets"].append({"reps": c.get("reps"), "actual_reps": c.get("actual_reps")})
    return {
        "summary": "",
        "exercises": list(exercises.values()),
        "duration_min": data.get("duration_min"),
        "note": data.get("note", "")
    }

# ─── 报告生成 ───────────────────────────────────────────────

def _get_week_range(ref_date_str: str):
    """返回给定日期所在周的起止日期（周一~周日）"""
    d = datetime.strptime(ref_date_str, "%Y-%m-%d")
    monday = d - __import__('datetime').timedelta(days=d.weekday())
    sunday = monday + __import__('datetime').timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

def _get_month_range(ref_date_str: str):
    """返回给定日期所在月的起止日期"""
    d = datetime.strptime(ref_date_str, "%Y-%m-%d")
    first = d.replace(day=1)
    if d.month == 12:
        last = d.replace(year=d.year+1, month=1, day=1) - __import__('datetime').timedelta(days=1)
    else:
        last = d.replace(month=d.month+1, day=1) - __import__('datetime').timedelta(days=1)
    return first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")

def _filter_records(hist_data, start_date: str, end_date: str, rec_type=None):
    records = hist_data.get("records", []) if isinstance(hist_data, dict) else hist_data
    result = [r for r in records if start_date <= r.get("date", "") <= end_date]
    if rec_type:
        result = [r for r in result if r.get("type") == rec_type]
    return result

def report_today(ref_date: str = None):
    ref = ref_date or str(_get_session_date())
    hist_data = load_json(HISTORY_FILE, {"records": []})
    workouts = _filter_records(hist_data, ref, ref, "workout")
    statuses = _filter_records(hist_data, ref, ref, "status")
    lines = [f"📅 **{ref} 日报**", "━━━━━━━━━━━━━━━"]
    if workouts:
        for w in workouts:
            wd = w.get("workout", {})
            summary = wd.get("summary", "")
            exercises = wd.get("exercises", [])
            dur = wd.get("duration_min")
            ex_lines = []
            for e in exercises:
                sets_str = "×".join(str(s.get("reps", s.get("actual_reps", "?"))) for s in e.get("sets", []))
                w_str = f"{e.get('weight_kg','')}kg" if e.get("weight_kg") else "自重"
                ex_lines.append(f"{e['name']} {w_str}×{len(e.get('sets',[]))}组")
            if summary:
                lines.append(f"🏋️ 训练：{'；'.join(ex_lines) if ex_lines else summary}")
            else:
                lines.append(f"🏋️ 训练：{'；'.join(ex_lines)}")
            if dur:
                lines.append(f"⏱️ 约 {dur} 分钟")
    else:
        lines.append("🏋️ 训练：无记录")
    if statuses:
        for s in statuses:
            st = s.get("status", "normal")
            det = s.get("detail", "")
            lines.append(f"😫 状态：{st}{'（' + det + ')' if det else ''}")
    else:
        lines.append("😫 状态：无记录")
    note = (workouts[0].get("workout", {}).get("note") if workouts else "") or ""
    lines.append(f"📝 备注：{note or '—'}")
    lines.append("━━━━━━━━━━━━━━━")
    return "\n".join(lines)

def report_week(ref_date: str = None):
    ref = ref_date or str(_get_session_date())
    mon, sun = _get_week_range(ref)
    hist_data = load_json(HISTORY_FILE, {"records": []})
    workouts = _filter_records(hist_data, mon, sun, "workout")
    statuses = _filter_records(hist_data, mon, sun, "status")
    lines = [f"📅 **周报（{mon} - {sun}）**", "━━━━━━━━━━━━━━━"]
    lines.append(f"🏋️ 训练次数：{len(workouts)}次")
    # 状态统计
    status_counts = {}
    for s in statuses:
        st = s.get("status", "normal")
        status_counts[st] = status_counts.get(st, 0) + 1
    if status_counts:
        status_str = " / ".join(f"{k}×{v}" for k, v in status_counts.items())
        lines.append(f"😫 状态：{status_str}")
    # 执行率
    plan = load_json(PLAN_FILE, {})
    if plan.get("mode") == "weekly":
        scheduled = len([d for d in plan.get("schedule", {}).values() if d])
        exe_rate = f"{len(workouts)}/{scheduled}" if scheduled else "?"
    else:
        exe_rate = f"{len(workouts)}次"
    lines.append(f"📉 执行率：{exe_rate}")
    # 问题
    if statuses:
        problems = [s.get("detail", "") for s in statuses if s.get("status") in ("tired", "poor_sleep", "travel", "injury") and s.get("detail")]
        if problems:
            lines.append(f"⚠️ 问题：{problems[0]}")
    # 方案变更
    pv = hist_data.get("plan_versions", []) if isinstance(hist_data, dict) else []
    recent_pv = [v for v in pv if v.get("date", "") >= mon]
    if recent_pv:
        lines.append(f"📋 方案变更：v{len(hist_data.get('plan_versions',[]))}（{recent_pv[0].get('reason','')[:20]}）")
    lines.append("━━━━━━━━━━━━━━━")
    return "\n".join(lines)

def report_month(ref_date: str = None):
    ref = ref_date or str(_get_session_date())
    first, last = _get_month_range(ref)
    hist_data = load_json(HISTORY_FILE, {"records": []})
    workouts = _filter_records(hist_data, first, last, "workout")
    statuses = _filter_records(hist_data, first, last, "status")
    total_dur = sum((w.get("workout") or {}).get("duration_min") or 0 for w in workouts)
    lines = [f"📅 **月报（{first[:7]}）**", "━━━━━━━━━━━━━━━"]
    lines.append(f"🏋️ 训练次数：{len(workouts)}次")
    if total_dur:
        lines.append(f"⏱️ 总时长：约 {total_dur} 分钟（{total_dur//60} 小时）")
    # 状态趋势
    status_counts = {}
    for s in statuses:
        st = s.get("status", "normal")
        status_counts[st] = status_counts.get(st, 0) + 1
    if status_counts:
        status_str = " / ".join(f"{k}×{v}" for k, v in sorted(status_counts.items()))
        lines.append(f"😫 状态：{status_str}")
    lines.append("━━━━━━━━━━━━━━━")
    return "\n".join(lines)

def report_summary(ref_date: str = None):
    ref = ref_date or str(_get_session_date())
    hist_data = load_json(HISTORY_FILE, {"records": []})
    today_dt = datetime.strptime(ref, "%Y-%m-%d")
    # 最近4周
    four_weeks_ago = (today_dt - __import__('datetime').timedelta(weeks=4)).strftime("%Y-%m-%d")
    workouts_4w = _filter_records(hist_data, four_weeks_ago, ref, "workout")
    pv = hist_data.get("plan_versions", []) if isinstance(hist_data, dict) else []
    lines = [f"📅 **阶段总结（近4周）**", "━━━━━━━━━━━━━━━"]
    lines.append(f"🏋️ 训练次数：{len(workouts_4w)}次")
    # 方案变更次数
    recent_pv = [v for v in pv if v.get("date", "") >= four_weeks_ago]
    if recent_pv:
        lines.append(f"📋 方案变更：{len(recent_pv)}次")
        lines.append(f"  最近：{recent_pv[0].get('reason', '')}")
    # 总训练时长
    total_dur = sum((w.get("workout") or {}).get("duration_min") or 0 for w in workouts_4w)
    if total_dur:
        lines.append(f"⏱️ 总时长：约 {total_dur//60} 小时")
    lines.append("━━━━━━━━━━━━━━━")
    return "\n".join(lines)

# ─── 身体状态 ────────────────────────────────────────────────

def body_get():
    """获取当前身体状态"""
    return load_json(BODY_FILE, None)

def body_update(height_cm=None, weight_kg=None, body_fat_pct=None,
                goal=None, notes=None, exercise_freq=None,
                experience=None, limitations=None):
    """更新身体状态字段（只更新提供的字段）"""
    data = load_json(BODY_FILE, {})
    now = _get_session_dt_local().strftime("%Y-%m-%d")
    if "created_at" not in data:
        data["created_at"] = now
    data["updated_at"] = now
    if height_cm is not None:
        data["height_cm"] = height_cm
    if weight_kg is not None:
        data["weight_kg"] = weight_kg
    if body_fat_pct is not None:
        data["body_fat_pct"] = body_fat_pct
    if goal is not None:
        data["goal"] = goal
    if notes is not None:
        data["notes"] = notes
    if exercise_freq is not None:
        data["exercise_freq"] = exercise_freq
    if experience is not None:
        data["experience"] = experience
    if limitations is not None:
        data["limitations"] = limitations
    save_json(BODY_FILE, data)
    return data

def body_log(height_cm=None, weight_kg=None, body_fat_pct=None, notes=None):
    """记录一条身体状态历史（用于定期追踪变化）"""
    data = load_json(BODY_FILE, {})
    history = data.get("history", [])
    entry = {
        "date": _get_session_dt_local().strftime("%Y-%m-%d"),
        "height_cm": height_cm if height_cm is not None else data.get("height_cm"),
        "weight_kg": weight_kg if weight_kg is not None else data.get("weight_kg"),
        "body_fat_pct": body_fat_pct if body_fat_pct is not None else data.get("body_fat_pct"),
        "notes": notes or "",
    }
    history = [h for h in history if h.get("date") != entry["date"]]
    history.insert(0, entry)
    data["history"] = history
    save_json(BODY_FILE, data)
    return entry

def body_history(days=90):
    """显示身体状态历史"""
    data = load_json(BODY_FILE, {})
    history = data.get("history", [])
    cutoff = (_get_session_dt_local() - __import__('datetime').timedelta(days=days-1)).strftime("%Y-%m-%d")
    recent = [h for h in history if h.get("date", "") >= cutoff]
    if not recent:
        return None
    return recent

def body_display():
    """返回身体状态摘要字符串"""
    data = load_json(BODY_FILE, None)
    if not data:
        return "还没有身体数据，请用「更新身体数据」告诉我你的基本信息～"
    lines = ["🏋️ **当前身体状态**"]
    if data.get("height_cm"):
        lines.append(f"  身高：{data['height_cm']} cm")
    if data.get("weight_kg"):
        lines.append(f"  体重：{data['weight_kg']} kg")
    if data.get("body_fat_pct"):
        lines.append(f"  体脂：{data['body_fat_pct']} %")
    if data.get("goal"):
        lines.append(f"  目标：{data['goal']}")
    if data.get("exercise_freq"):
        lines.append(f"  训练频率：{data['exercise_freq']}")
    if data.get("experience"):
        lines.append(f"  经验：{data['experience']}")
    if data.get("limitations"):
        lines.append(f"  限制：{data['limitations']}")
    if data.get("notes"):
        lines.append(f"  备注：{data['notes']}")
    history = data.get("history", [])
    if history:
        latest = history[0]
        lines.append(f"\n📈 最新记录（{latest.get('date','')}）")
        if latest.get("weight_kg"):
            lines.append(f"  体重 {latest['weight_kg']} kg")
        if latest.get("body_fat_pct"):
            lines.append(f"  体脂 {latest['body_fat_pct']} %")
    updated = data.get("updated_at", "")
    if updated:
        lines.append(f"\n⏱️ 更新于 {updated}")
    return "\n".join(lines)

# ─── 主入口 ───────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "plan":
        if len(sys.argv) < 3:
            print("用法: workout.py plan set/import/view")
            sys.exit(1)
        sub = sys.argv[2]
        if sub == "set":
            print(plan_set(sys.argv[3] if len(sys.argv) > 3 else sys.stdin.read()))
        elif sub == "import":
            print(plan_import(sys.argv[3] if len(sys.argv) > 3 else ""))
        elif sub == "view":
            print(plan_view())
        else:
            print(f"未知子命令: {sub}")

    elif cmd == "start":
        hint = sys.argv[2] if len(sys.argv) > 2 else None
        hint_map = {"长": "long", "短": "short", "30分钟": "long", "15分钟": "short",
                    "long": "long", "short": "short"}
        hint = hint_map.get(hint, None)
        print(start_workout(hint))

    elif cmd == "status":
        print(json.dumps(workout_status() or {}, ensure_ascii=False))

    elif cmd == "complete-set":
        reps = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        print(complete_set(reps))

    elif cmd == "skip-action":
        print(skip_action())

    elif cmd == "history":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(show_history(days))

    elif cmd == "reset-today":
        print(reset_today())

    elif cmd == "reset-date":
        if len(sys.argv) < 3:
            print("用法: workout.py reset-date <YYYY-MM-DD>")
            sys.exit(1)
        print(reset_date(sys.argv[2]))

    elif cmd == "add-record":
        # 用法: workout.py add-record <date> <json_completed_list> [json_skipped_list]
        if len(sys.argv) < 4:
            print("用法: workout.py add-record <YYYY-MM-DD> '<completed_json>' ['<skipped_json>']")
            sys.exit(1)
        date_str = sys.argv[2]
        try:
            completed = json.loads(sys.argv[3])
        except Exception as e:
            print(f"completed_list JSON解析失败: {e}")
            sys.exit(1)
        skipped = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
        print(add_record(date_str, completed, skipped))

    elif cmd == "plan-parse":
        # 用法: workout.py plan-parse "<自然语言描述>"
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        result = plan_parse(text)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "body":
        # 用法: workout.py body get/update/log/view
        sub = sys.argv[2] if len(sys.argv) > 2 else "view"
        if sub == "get":
            print(json.dumps(body_get() or {}, ensure_ascii=False, indent=2))
        elif sub == "update":
            # workout.py body update height_cm=175 weight_kg=70 body_fat_pct=18 goal="增肌"
            kwargs = {}
            for arg in sys.argv[3:]:
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    if k in ("height_cm", "weight_kg", "body_fat_pct"):
                        kwargs[k] = float(v) if "." in v else int(v)
                    else:
                        kwargs[k] = v
            body_update(**kwargs)
            print(body_display())
        elif sub == "log":
            # workout.py body log weight=69.5 body_fat=17.5
            kwargs = {}
            for arg in sys.argv[3:]:
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    if k in ("height_cm", "weight_kg", "body_fat_pct"):
                        kwargs[k] = float(v) if "." in v else int(v)
                    else:
                        kwargs[k] = v
            entry = body_log(**kwargs)
            print(f"✅ 已记录身体状态（{entry['date']}）：体重 {entry.get('weight_kg','?')} kg，体脂 {entry.get('body_fat_pct','?')} %")
        elif sub == "history":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 90
            hist = body_history(days)
            if not hist:
                print(f"近{days}天没有身体状态记录")
            else:
                lines = [f"📊 **身体状态历史（近{days}天）**\n", "| 日期 | 体重(kg) | 体脂(%) |", "|------|---------|--------|"]
                for h in hist:
                    lines.append(f"| {h.get('date','?')} | {h.get('weight_kg','—')} | {h.get('body_fat_pct','—')} |")
                print("\n".join(lines))
        elif sub == "view":
            print(body_display())
        else:
            print(f"未知子命令: {sub}，可用: get / update / log / view / history")

    elif cmd == "log":
        # workout.py log "2026-04-20" '{"summary":"练了背","exercises":[...],"duration_min":null}'
        session_file = os.path.join(DATA_DIR, ".session.json")
        has_session = os.path.exists(session_file)
        session = load_json(session_file) if has_session else None
        date_str = sys.argv[2] if len(sys.argv) > 2 else str(_get_session_date())
        try:
            data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        except:
            print("JSON格式错误")
            sys.exit(1)

        # 如果有 session，先检查计划是否已全部完成
        auto_finished = False
        if has_session and session:
            plan = session.get("plan")
            if plan and isinstance(plan, list) and isinstance(data, dict):
                logged_names = {e.get("name") for e in data.get("exercises", []) if isinstance(e, dict)}
                planned_names = {a.get("name") for a in plan if isinstance(a, dict)}
                if planned_names and planned_names <= logged_names:
                    # 所有计划动作都已记录，自动算时长
                    started_at = session.get("started_at")
                    finished_at = _get_session_dt_local().isoformat()
                    dur_mins = 0
                    try:
                        s = datetime.fromisoformat(started_at)
                        e = datetime.fromisoformat(finished_at)
                        dur_mins = int((e - s).total_seconds() / 60)
                    except:
                        pass
                    data["duration_min"] = dur_mins
                    auto_finished = True

        _history_add(date_str, "workout", workout_data=data)
        if auto_finished:
            os.remove(session_file)
            print(f"✅ 已记录训练：{data.get('summary', '训练记录')}（{date_str}）")
            print(f"🏁 计划动作全部完成，自动结束训练，用时约 {data.get('duration_min')} 分钟")
        else:
            print(f"✅ 已记录训练：{data.get('summary', '训练记录')}（{date_str}）")

    elif cmd == "status-log":
        # workout.py status-log "2026-04-20" tired "昨晚没睡好"
        date_str = sys.argv[2] if len(sys.argv) > 2 else str(_get_session_date())
        status = sys.argv[3] if len(sys.argv) > 3 else "normal"
        detail = sys.argv[4] if len(sys.argv) > 4 else ""
        _history_add(date_str, "status", status=status, detail=detail)
        print(f"✅ 已记录状态：{status}（{date_str}）{'— ' + detail if detail else ''}")

    elif cmd == "report":
        sub = sys.argv[2] if len(sys.argv) > 2 else "today"
        ref_date = sys.argv[3] if len(sys.argv) > 3 else str(_get_session_date())
        if sub == "today":
            print(report_today(ref_date))
        elif sub == "week":
            print(report_week(ref_date))
        elif sub == "month":
            print(report_month(ref_date))
        elif sub == "summary":
            print(report_summary(ref_date))
        else:
            print("可用: today / week / month / summary")

    elif cmd == "plan":
        sub = sys.argv[2] if len(sys.argv) > 2 else ""
        if sub == "version":
            reason = sys.argv[3] if len(sys.argv) > 3 else ""
            _history_add(str(_get_session_date()), "plan_change", reason=reason)
            print(f"✅ 方案版本记录已保存：{reason}")
        elif sub == "view":
            print(plan_view())
        elif sub == "set":
            print(plan_set(sys.argv[3] if len(sys.argv) > 3 else sys.stdin.read()))
        elif sub == "import":
            print(plan_import(sys.argv[3] if len(sys.argv) > 3 else ""))
        else:
            print("可用: version / view / set / import")

    elif cmd == "start-session":
        # 开启训练计时会话（不依赖 guided start workflow）
        session_file = os.path.join(DATA_DIR, ".session.json")
        # 自动读取今日计划写入 session，用于判断是否全部完成
        plan = load_json(PLAN_FILE)
        today_plan = None
        if plan:
            mode = plan.get("mode", "weekly")
            if mode == "sequence":
                day_of_year = _get_session_date().timetuple().tm_yday
                seq = plan.get("sequence", [])
                if seq:
                    today_plan = seq[(day_of_year - 1) % len(seq)]
            else:
                day_name = get_today_name()
                schedule = plan.get("schedule", {})
                raw = schedule.get(day_name)
                # 解析出简单动作列表用于完成判断
                if isinstance(raw, list):
                    today_plan = raw
                elif isinstance(raw, dict):
                    # 双版本，取第一个可用版本
                    for key in raw:
                        if key not in ("goal", "duration", "note"):
                            today_plan = raw[key]
                            break
        session = {
            "started_at": _get_session_dt_local().isoformat(),
            "date": str(_get_session_date()),
            "plan": today_plan
        }
        save_json(session_file, session)
        print(f"✅ 训练计时开始：{session['started_at']}")

    elif cmd == "finish-workout":
        # 结束训练：从 session.json 读取开始时间，计算时长，更新 history.json 最新记录
        session_file = os.path.join(DATA_DIR, ".session.json")
        if not os.path.exists(session_file):
            print("没有正在计时的训练会话，请先运行 start-session")
            sys.exit(1)
        session = load_json(session_file)
        started_at = session.get("started_at")
        finished_at = _get_session_dt_local().isoformat()
        # 计算时长
        dur_mins = 0
        try:
            s = datetime.fromisoformat(started_at)
            e = datetime.fromisoformat(finished_at)
            dur_mins = int((e - s).total_seconds() / 60)
        except:
            pass
        # 读取 history.json 最新训练记录，更新其 duration_min
        hist_data = load_json(HISTORY_FILE, {"records": []})
        records = hist_data.get("records", [])
        # 找到 date 相同的最新的 workout 记录
        date_str = session.get("date", str(_get_session_date()))
        for i, rec in enumerate(records):
            if rec.get("date") == date_str and rec.get("type") == "workout":
                if rec["workout"].get("duration_min") is None or rec["workout"].get("duration_min") == 0:
                    rec["workout"]["duration_min"] = dur_mins
                    records[i] = rec
                    break
        hist_data["records"] = records
        save_json(HISTORY_FILE, hist_data)
        os.remove(session_file)
        print(f"✅ 训练完成，用时约 {dur_mins} 分钟")

    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
