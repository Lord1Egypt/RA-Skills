#!/usr/bin/env python3
"""automation_update — 跨平台定时任务管理"""
import sys, os, json, re, time
from datetime import datetime
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def get_automation_dir(params):
    """获取自动化任务存储目录"""
    base = get_param(params, "automation_dir")
    if base:
        return resolve_path(base, must_exist=False)
    return home_dir() / ".builtin-tools" / "automations"


def generate_id(name):
    """从名称生成安全 ID"""
    safe = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return safe[:50] or "unnamed"


def parse_rrule(rrule_str):
    """解析简易 RRULE 为人类可读描述"""
    if not rrule_str:
        return None
    parts = {}
    for part in rrule_str.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            parts[k] = v

    freq = parts.get("FREQ", "")
    interval = parts.get("INTERVAL", "1")
    byday = parts.get("BYDAY", "")
    byhour = parts.get("BYHOUR", "")
    byminute = parts.get("BYMINUTE", "")

    freq_map = {"HOURLY": "每小时", "DAILY": "每天", "WEEKLY": "每周", "MONTHLY": "每月"}
    freq_text = freq_map.get(freq, freq)

    if interval != "1":
        freq_text = f"每{interval}{freq_text[1:]}" if len(freq_text) > 1 else f"每{interval}{freq_text}"

    day_map = {"MO": "周一", "TU": "周二", "WE": "周三", "TH": "周四", "FR": "周五", "SA": "周六", "SU": "周日"}
    if byday:
        days = [day_map.get(d, d) for d in byday.split(",")]
        freq_text += f"（{','.join(days)}）"

    if byhour and byminute:
        freq_text += f" {byhour}:{byminute.zfill(2)}"

    return freq_text


def save_automation(auto_dir, auto_id, config):
    """保存自动化配置为 JSON"""
    auto_dir.mkdir(parents=True, exist_ok=True)
    config_path = auto_dir / auto_id / "automation.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config["updated_at"] = datetime.now().isoformat()
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    return config_path


def load_automation(auto_dir, auto_id):
    """加载自动化配置"""
    config_path = auto_dir / auto_id / "automation.json"
    if not config_path.exists():
        return None
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def list_automations(auto_dir):
    """列出所有自动化任务"""
    if not auto_dir.exists():
        return []
    automations = []
    for auto_path in sorted(auto_dir.iterdir()):
        if auto_path.is_dir():
            config = load_automation(auto_dir, auto_path.name)
            if config:
                automations.append(config)
    return automations


def get_system_cron_command(config):
    """生成系统级 cron/schtasks 命令"""
    prompt = config.get("prompt", "")
    schedule = config.get("rrule", "")
    name = config.get("name", "task")
    auto_id = config.get("id", name)

    if sys.platform == "win32":
        # Windows: schtasks
        rrule = parse_rrule(schedule)
        if "DAILY" in schedule:
            trigger = "/sc daily"
            hour = config.get("rrule", "").split("BYHOUR=")[-1].split(";")[0] if "BYHOUR" in schedule else "9"
            trigger += f" /st {hour}:00"
        elif "HOURLY" in schedule:
            interval = "1"
            for part in schedule.split(";"):
                if part.startswith("INTERVAL="):
                    interval = part.split("=")[1]
            trigger = f"/sc hourly /mo {interval}"
        elif "WEEKLY" in schedule:
            trigger = "/sc weekly"
        else:
            trigger = "/sc daily /st 09:00"

        python_path = sys.executable
        script_dir = Path(__file__).parent
        cmd = (
            f'schtasks /create /tn "builtin-tools/{auto_id}" '
            f'/tr "{python_path} {script_dir}/execute_command.py --mode command '
            f'--command \\"echo {prompt}\\"" '
            f'{trigger} /f'
        )
        return cmd
    else:
        # Unix: cron
        return f'# 添加到 crontab: crontab -e\n# {parse_rrule(schedule)}\n# {prompt}'


def main():
    params = parse_input()
    mode = get_param(params, "mode", required=True)

    auto_dir = get_automation_dir(params)

    if mode == "view":
        auto_id = get_param(params, "id", required=True)
        config = load_automation(auto_dir, auto_id)
        if not config:
            output_error(f"未找到自动化任务: {auto_id}", EXIT_EXEC_ERROR)
        config["rrule_description"] = parse_rrule(config.get("rrule"))
        output_ok(config)

    elif mode == "list":
        automations = list_automations(auto_dir)
        for a in automations:
            a["rrule_description"] = parse_rrule(a.get("rrule"))
        output_ok({"automations": automations, "total": len(automations), "dir": str(auto_dir)})

    elif mode in ("create", "suggested create"):
        name = get_param(params, "name", required=True)
        prompt = get_param(params, "prompt", required=True)
        schedule_type = get_param(params, "schedule_type", "recurring")
        rrule = get_param(params, "rrule", "FREQ=DAILY;BYHOUR=9;BYMINUTE=0")
        scheduled_at = get_param(params, "scheduled_at")
        status = get_param(params, "status", "active")
        valid_from = get_param(params, "valid_from")
        valid_until = get_param(params, "valid_until")

        auto_id = generate_id(name)

        config = {
            "id": auto_id,
            "name": name,
            "prompt": prompt,
            "schedule_type": schedule_type,
            "status": status,
            "created_at": datetime.now().isoformat(),
        }

        if schedule_type == "recurring" and rrule:
            config["rrule"] = rrule
        elif schedule_type == "once" and scheduled_at:
            config["scheduled_at"] = scheduled_at

        if valid_from:
            config["valid_from"] = valid_from
        if valid_until:
            config["valid_until"] = valid_until

        config_path = save_automation(auto_dir, auto_id, config)
        config["rrule_description"] = parse_rrule(config.get("rrule"))
        output_ok(config)

    elif mode in ("update", "suggested update"):
        auto_id = get_param(params, "id", required=True)
        existing = load_automation(auto_dir, auto_id)
        if not existing:
            output_error(f"未找到自动化任务: {auto_id}", EXIT_EXEC_ERROR)

        # 合并更新字段
        for key in ["name", "prompt", "rrule", "scheduled_at", "status", "valid_from", "valid_until"]:
            value = get_param(params, key)
            if value is not None:
                existing[key] = value

        config_path = save_automation(auto_dir, auto_id, existing)
        existing["rrule_description"] = parse_rrule(existing.get("rrule"))
        output_ok(existing)

    elif mode == "cron":
        # 生成系统级 cron/schtasks 命令
        auto_id = get_param(params, "id", required=True)
        config = load_automation(auto_dir, auto_id)
        if not config:
            output_error(f"未找到自动化任务: {auto_id}", EXIT_EXEC_ERROR)
        cmd = get_system_cron_command(config)
        output_ok({"id": auto_id, "command": cmd})

    else:
        output_error(
            f"未知模式: {mode}（支持: view, list, create, update, cron）",
            EXIT_PARAM_ERROR,
        )


if __name__ == "__main__":
    main()
