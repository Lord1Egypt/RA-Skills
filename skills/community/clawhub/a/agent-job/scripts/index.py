"""
入口脚本：解析 /lobster claim|earnings|withdraw|start|stop 命令
"""
import sys
import os
import json
import subprocess
import yaml
import requests
from datetime import datetime

# 确保 scripts 目录可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import api as lobster_api

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")
STATE_FILE = os.path.join(SKILL_DIR, "state.json")
CRON_JOB_ID_FILE = os.path.join(SKILL_DIR, "cron_job_id.json")
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")


# ===================== 工具函数 =====================

def openclaw(args: list) -> str:
    """执行 openclaw CLI 命令"""
    result = subprocess.run(
        ["openclaw"] + args,
        capture_output=True, text=True
    )
    return result.stdout + result.stderr


def save_cron_job_id(job_id):
    with open(CRON_JOB_ID_FILE, "w") as f:
        json.dump({"job_id": job_id}, f)


def load_cron_job_id():
    if not os.path.exists(CRON_JOB_ID_FILE):
        return None
    with open(CRON_JOB_ID_FILE, "r") as f:
        return json.load(f).get("job_id")


def get_installed_skills():
    """扫描已安装的 skills，返回 [{name, desc}, ...]"""
    skills = []
    if not os.path.isdir(SKILLS_DIR):
        return skills

    for item in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(skill_path):
            continue
        if item == "lobster-agent":
            continue
        skill_md = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    meta = yaml.safe_load(parts[1])
                    name = meta.get("name", item)
                    desc = meta.get("description", "")
                    skills.append({"name": name, "desc": desc[:200]})
        except Exception:
            continue
    return skills


def register_skills_to_platform():
    """将已安装的 skills 登记到平台"""
    skills = get_installed_skills()
    if not skills:
        print("[INFO] 未扫描到已安装的 skills，跳过登记")
        return

    try:
        token = lobster_api.get_token()
        url = f"{lobster_api.BASE_URL}/api/lobster/me/skills"
        resp = requests.put(
            url,
            headers={"X-Lobster-Token": token},
            json={"skills": skills},
            timeout=30
        )
        resp.raise_for_status()
        print(f"[INFO] 已将 {len(skills)} 个 skills 登记到平台")
        for s in skills:
            print(f"  - {s['name']}: {s['desc'][:50]}")
    except Exception as e:
        print(f"[WARN] 登记 skills 失败：{e}", file=sys.stderr)


# ===================== 命令实现 =====================

def cmd_start():
    """启动托管：创建 cron job + 登记 skills"""
    # 检查是否已创建过，先删旧
    existing_id = load_cron_job_id()
    if existing_id:
        try:
            openclaw(["cron", "rm", existing_id])
            print(f"[INFO] 已删除旧 cron job: {existing_id}")
        except Exception:
            pass

    # 创建新的 cron job（每分钟轮询，隔离会话，结果宣布到聊天）
    output = openclaw([
        "cron", "add",
        "--name", "lobster-agent poll",
        "--cron", "* * * * *",
        "--message", "/lobster poll",
        "--session", "isolated",
        "--announce"
    ])

    # 尝试从 JSON 输出中解析 job id
    job_id = None
    try:
        import re
        m = re.search(r'"id"\s*:\s*"([^"]+)"', output)
        if m:
            job_id = m.group(1)
    except Exception:
        pass

    if job_id:
        save_cron_job_id(job_id)
        print(f"✅ 定时任务已创建 (id={job_id})")
    else:
        print(f"⚠️ 定时任务创建未解析到 id，请手动确认：openclaw cron list")
        print(f"   原始输出: {output[:200]}")

    # 登记 skills
    register_skills_to_platform()

    # 更新状态
    state = lobster_api.load_state()
    state["poll_enabled"] = True
    lobster_api.save_state(state)

    return "✅ 龙虾托管已启动，每分钟自动轮询，有新任务时推送"


def cmd_stop():
    """停止托管：删除 cron job"""
    job_id = load_cron_job_id()
    if job_id:
        try:
            openclaw(["cron", "rm", job_id])
            print(f"[INFO] 已删除 cron job: {job_id}")
        except Exception as e:
            print(f"[WARN] 删除 cron job 失败：{e}")
        try:
            os.remove(CRON_JOB_ID_FILE)
        except Exception:
            pass

    state = lobster_api.load_state()
    state["poll_enabled"] = False
    lobster_api.save_state(state)

    return "✅ 龙虾托管已停止"


def format_task(task):
    """格式化任务信息"""
    task_id = task.get("task_id", "?")
    title = task.get("title", "无标题")
    deadline = task.get("submission_deadline", "无截止时间")
    status_map = {0: "待领取", 1: "进行中"}
    status = status_map.get(task.get("status", 0), "未知")
    attachment = task.get("attachment_signed_url") or task.get("attachment_url") or "无附件"
    return (
        f"任务 #{task_id}\n"
        f"  标题：{title}\n"
        f"  状态：{status}\n"
        f"  截止：{deadline}\n"
        f"  附件：{attachment}"
    )


def cmd_claim():
    """主动触发抢任务"""
    try:
        result = lobster_api.claim()
        claimed = result.get("claimed")
        in_progress = result.get("in_progress") or []

        if claimed and claimed.get("success"):
            task = claimed
            state = lobster_api.load_state()
            current_ids = [item.get("task_id") for item in in_progress]
            state["in_progress_task_ids"] = current_ids
            state["last_poll_at"] = task.get("claimed_at")
            lobster_api.save_state(state)

            lines = [
                "✅ 抢到新任务！",
                format_task(task),
                "",
                f"--- 进行中的任务 ({len(in_progress)}) ---",
            ]
            for item in in_progress:
                lines.append(f"#{item.get('task_id')} {item.get('title')}")
            return "\n".join(lines)
        else:
            msg = claimed.get("message", "暂无新任务或已超过领取截止时间") if claimed else "暂无新任务"
            in_progress_lines = [f"--- 进行中 ({len(in_progress)}) ---"]
            for item in in_progress:
                in_progress_lines.append(f"#{item.get('task_id')} {item.get('title')}")
            return "\n".join([msg] + (in_progress_lines if in_progress else [""]))
    except Exception as e:
        return f"❌ 抢任务失败：{e}"


def cmd_earnings():
    """查看累计收益"""
    try:
        result = lobster_api.get_earnings()
        total = result.get("total_earned", 0)
        return f"💰 累计收益：¥{total}"
    except Exception as e:
        return f"❌ 查询失败：{e}"


def cmd_withdraw(amount_str: str):
    """申请提现"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return "❌ 提现金额必须大于 0"
    except ValueError:
        return f"❌ 无效金额：{amount_str}，请填写数字"

    try:
        result = lobster_api.withdraw(amount)
        if result.get("success"):
            total = result.get("total_earned", 0)
            withdrawable = result.get("withdrawable", 0)
            return (
                f"✅ 提现申请已提交\n"
                f"   申请金额：¥{amount}\n"
                f"   累计收益：¥{total}\n"
                f"   剩余可提：¥{withdrawable}"
            )
        else:
            return f"❌ 提现失败：{result.get('message', '未知错误')}"
    except Exception as e:
        return f"❌ 提现失败：{e}"


# ===================== 入口 =====================

def main():
    args = sys.argv[1:]

    if not args:
        print("用法：/lobster claim | earnings | withdraw <金额> | start | stop | poll")
        return

    subcommand = args[0].lower()

    if subcommand == "claim":
        print(cmd_claim())
    elif subcommand == "earnings":
        print(cmd_earnings())
    elif subcommand == "withdraw":
        if len(args) < 2:
            print("❌ 请指定提现金额，如：/lobster withdraw 100")
        else:
            print(cmd_withdraw(args[1]))
    elif subcommand == "start":
        print(cmd_start())
    elif subcommand == "stop":
        print(cmd_stop())
    elif subcommand == "poll":
        # 轮询：供 cron job 调用
        state = lobster_api.load_state()
        if not state.get("poll_enabled"):
            print("[POLL] 轮询已停止，跳过")
            return
        known_ids = set(state.get("in_progress_task_ids", []))
        result = lobster_api.claim()
        in_progress = result.get("in_progress") or []
        current_ids = set(item.get("task_id") for item in in_progress)
        new_tasks = [item for item in in_progress if item.get("task_id") not in known_ids]
        state["in_progress_task_ids"] = list(current_ids)
        state["last_poll_at"] = datetime.utcnow().isoformat()
        lobster_api.save_state(state)
        if new_tasks:
            for task in new_tasks:
                print(f"[NEW_TASK] 任务 #{task.get('task_id')} - {task.get('title')}", flush=True)
        else:
            print(f"[POLL] 无新任务，进行中: {len(current_ids)}", flush=True)
    else:
        print(f"未知命令：{subcommand}")
        print("用法：/lobster claim | earnings | withdraw <金额> | start | stop | poll")


if __name__ == "__main__":
    main()
