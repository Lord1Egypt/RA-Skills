#!/usr/bin/env python3
"""bigtimer.py — 定时任务 + 消息推送管家 (v0.1.0)

双端兼容：OpenClaw（openclaw cron / message send）与 DSH（crontab / 飞书 webhook）
数据目录：$DSH_WORKSPACE/memory 或 $OPENCLAW_WORKSPACE/memory 或 ~/.openclaw/workspace/memory

用法:
  bigtimer.py add --name <n> --schedule "<cron>" --action "<cmd>" [--push auto|openclaw|webhook|stdout] [--webhook <url>] [--channel <c>] [--target <t>]
  bigtimer.py list
  bigtimer.py remove <name>
  bigtimer.py status <name>
  bigtimer.py run <name> [--quiet]
  bigtimer.py cron-gen [name]      # 打印可用的调度条目（不写入系统）
  bigtimer.py install <name>       # 把任务写入系统调度（OpenClaw cron / crontab）
"""
import sys, os, json, shutil, subprocess, argparse, time
from datetime import datetime

def ws_root():
    for v in ("DSH_WORKSPACE", "OPENCLAW_WORKSPACE"):
        if os.environ.get(v):
            return os.environ[v]
    # OpenClaw agent 执行环境（gateway 子进程）
    if os.environ.get("OPENCLAW_GATEWAY_PORT") or os.environ.get("OPENCLAW_SERVICE_KIND"):
        return os.path.expanduser("~/.openclaw/workspace")
    # DSH 机器兜底
    if os.path.isdir(os.path.expanduser("~/.dsh")):
        return os.path.expanduser("~/.dsh/workspace")
    return os.path.expanduser("~/.openclaw/workspace")

MEMORY_DIR = os.path.join(ws_root(), "memory")
TASKS_FILE = os.path.join(MEMORY_DIR, "bigtimer-tasks.json")
LOG_FILE = os.path.join(MEMORY_DIR, "bigtimer.log")

os.makedirs(MEMORY_DIR, exist_ok=True)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    line = f"[{now()}] {msg}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    return line

def has_openclaw():
    return shutil.which("openclaw") is not None

def detect_env():
    """环境判定：BIGTIMER_ENV 显式 > DSH_WORKSPACE（DSH 环境特征）> OpenClaw 标记 > ~/.dsh 存在性 > openclaw CLI"""
    forced = os.environ.get("BIGTIMER_ENV", "").lower()
    if forced in ("openclaw", "dsh"):
        return forced
    if os.environ.get("DSH_WORKSPACE"):
        return "dsh"
    if (os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("OPENCLAW_GATEWAY_PORT")
            or os.environ.get("OPENCLAW_SERVICE_KIND")):
        return "openclaw"
    if os.path.isdir(os.path.expanduser("~/.dsh")):
        return "dsh"
    return "openclaw" if has_openclaw() else "dsh"

def load_tasks():
    if not os.path.isfile(TASKS_FILE):
        return {}
    try:
        with open(TASKS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# ── 推送引擎 ──────────────────────────────────────────
def push_openclaw(content, channel, target):
    """OpenClaw 环境：openclaw message send"""
    if not channel or not target:
        # 尝试从 biga-send-config.json 读默认投递目标
        cfg_path = os.path.join(MEMORY_DIR, "biga-send-config.json")
        if os.path.isfile(cfg_path):
            try:
                with open(cfg_path, encoding="utf-8") as f:
                    cfg = json.load(f)
                channel = channel or cfg.get("channel")
                target = target or cfg.get("target")
            except Exception:
                pass
    if not channel or not target:
        return {"ok": False, "error": "缺少 channel/target（可用 --channel/--target 或配置 biga-send-config.json）"}
    # 分段发送：超长内容按 ---SEGMENT--- 或空行切段
    parts = content.split("---SEGMENT---") if "---SEGMENT---" in content else [content]
    segs = [p.strip() for p in parts if p.strip()]
    if len(segs) <= 1 and len(content) > 500:
        import re
        segs = [p.strip() for p in re.split(r"\n{2,}", content) if p.strip()]
    results = []
    for i, seg in enumerate(segs):
        p = subprocess.Popen(
            ["openclaw", "message", "send", "--channel", channel, "--target", target,
             "--message", seg, "--json"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(timeout=30)
        ok = False
        try:
            ok = json.loads(out.decode()).get("payload", {}).get("ok", False)
        except Exception:
            ok = False
        results.append({"segment": i + 1, "ok": ok})
        time.sleep(0.8)
    return {"ok": all(r["ok"] for r in results) if results else False,
            "results": results, "mode": "openclaw"}

def push_webhook(content, webhook_url):
    """飞书自定义机器人 webhook 推送"""
    if not webhook_url:
        return {"ok": False, "error": "缺少 webhook URL"}
    payload = {"msg_type": "text", "content": {"text": content[:4000]}}
    p = subprocess.Popen(
        ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False), webhook_url],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(timeout=20)
    try:
        resp = json.loads(out.decode())
        ok = resp.get("code") == 0 or resp.get("StatusCode") == 0
    except Exception:
        ok = False
    return {"ok": ok, "resp": out.decode()[:200], "mode": "webhook"}

def push(task, content):
    mode = task.get("push", "auto")
    env = detect_env()
    if mode in ("auto", "openclaw") and env == "openclaw" and mode != "webhook":
        return push_openclaw(content, task.get("channel"), task.get("target"))
    if mode in ("auto", "webhook") and task.get("webhook"):
        return push_webhook(content, task.get("webhook"))
    if mode in ("auto", "stdout"):
        print(content)
        return {"ok": True, "mode": "stdout"}
    return {"ok": False, "error": f"无法推送（push={mode}）"}

# ── 调度生成 ──────────────────────────────────────────
def gen_crontab_line(task, skill_dir):
    """DSH 环境：生成 crontab 行"""
    name = task["name"]
    cmd = (f"cd {skill_dir} && python3 scripts/bigtimer.py run {name} --quiet "
           f">> {LOG_FILE} 2>&1")
    return f"{task['schedule']} {cmd}"

def gen_openclaw_cron(task):
    """OpenClaw 环境：生成 openclaw cron add 命令（提示，不自动执行）"""
    name = task["name"]
    action = task["action"]
    return (f"openclaw cron add --name bigtimer-{name} --schedule '{task['schedule']}' "
            f"--message \"【bigtimer 任务 {name}】\n执行动作: {action}\\n按 SKILL.md 输出结果并推送\" "
            f"--channel {task.get('channel', '<channel>')} --to {task.get('target', '<target>')}")

# ── 命令实现 ──────────────────────────────────────────
def cmd_add(args):
    tasks = load_tasks()
    if args.name in tasks:
        return {"ok": False, "error": f"任务已存在: {args.name}"}
    if not args.action:
        return {"ok": False, "error": "缺少 --action"}
    tasks[args.name] = {
        "name": args.name,
        "schedule": args.schedule,
        "action": args.action,
        "push": args.push,
        "webhook": args.webhook,
        "channel": args.channel,
        "target": args.target,
        "created": now(),
        "last_run": None,
        "last_status": None,
    }
    save_tasks(tasks)
    log(f"add 任务 {args.name} schedule={args.schedule} push={args.push}")
    env = detect_env()
    return {"ok": True, "task": args.name, "env": env,
            "tip": "用 install 写入系统调度"}

def cmd_list(_args):
    tasks = load_tasks()
    if not tasks:
        return {"ok": True, "tasks": [], "note": "暂无任务"}
    out = []
    for t in sorted(tasks.values(), key=lambda x: x.get("created", "")):
        out.append({
            "name": t["name"], "schedule": t["schedule"], "push": t["push"],
            "action": t["action"][:80], "last_run": t.get("last_run"),
            "last_status": t.get("last_status"),
        })
    return {"ok": True, "tasks": out}

def cmd_remove(args):
    tasks = load_tasks()
    if args.name not in tasks:
        return {"ok": False, "error": f"任务不存在: {args.name}"}
    del tasks[args.name]
    save_tasks(tasks)
    log(f"remove 任务 {args.name}")
    return {"ok": True, "removed": args.name, "tip": "需手动移除系统调度条目（crontab -e / openclaw cron remove）"}

def cmd_status(args):
    tasks = load_tasks()
    if args.name not in tasks:
        return {"ok": False, "error": f"任务不存在: {args.name}"}
    t = tasks[args.name]
    t["env"] = detect_env()
    return {"ok": True, "task": t}

def cmd_run(args):
    tasks = load_tasks()
    if args.name not in tasks:
        return {"ok": False, "error": f"任务不存在: {args.name}"}
    t = tasks[args.name]
    log(f"run 任务 {args.name}: {t['action']}")
    # 执行 action（shell 命令）
    p = subprocess.Popen(["bash", "-c", t["action"]],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         cwd=os.path.dirname(os.path.abspath(__file__)))
    out, err = p.communicate(timeout=300)
    content = out.decode("utf-8", errors="replace").strip()
    err_txt = err.decode("utf-8", errors="replace").strip()
    if not content and err_txt:
        content = f"[stderr]\n{err_txt}"
    # 推送
    result = push(t, content)
    t["last_run"] = now()
    t["last_status"] = "ok" if result.get("ok") else "fail"
    tasks[args.name] = t
    save_tasks(tasks)
    log(f"run 完成 {args.name}: {t['last_status']} ({result.get('mode', '?')})")
    if args.quiet:
        return None
    return {"ok": result.get("ok"), "task": args.name, "push": result.get("mode", "?"),
            "exit": p.returncode, "result": result}

def cmd_cron_gen(args):
    tasks = load_tasks()
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lines = []
    env = detect_env()
    for name in ([args.name] if args.name else sorted(tasks.keys())):
        if name not in tasks:
            return {"ok": False, "error": f"任务不存在: {name}"}
        t = tasks[name]
        if env == "openclaw":
            lines.append(gen_openclaw_cron(t))
        else:
            lines.append(gen_crontab_line(t, skill_dir))
    return {"ok": True, "env": env, "lines": lines}

def cmd_install(args):
    tasks = load_tasks()
    if args.name not in tasks:
        return {"ok": False, "error": f"任务不存在: {args.name}"}
    t = tasks[args.name]
    env = detect_env()
    if env == "openclaw":
        cmd = gen_openclaw_cron(t)
        return {"ok": True, "env": env,
                "tip": "OpenClaw 环境请用 gateway cron 添加（本脚本仅生成命令供参考）",
                "cmd": cmd}
    # DSH 环境：写入 crontab
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    line = gen_crontab_line(t, skill_dir)
    cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    lines = [l for l in cur.splitlines() if f"bigtimer.py run {args.name}" not in l]
    lines.append(line)
    p = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, capture_output=True)
    if p.returncode == 0:
        log(f"install 任务 {args.name} → crontab: {line}")
        return {"ok": True, "env": "dsh", "crontab": line}
    return {"ok": False, "error": p.stderr, "crontab": line}

def main():
    ap = argparse.ArgumentParser(description="bigtimer 定时任务+推送管家")
    ap.add_argument("--version", action="version", version="bigtimer 1.0.0")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--schedule", default="0 8 * * *", help="cron 表达式（5段）")
    p_add.add_argument("--action", required=True, help="要执行的 shell 命令")
    p_add.add_argument("--push", default="auto", choices=["auto", "openclaw", "webhook", "stdout"])
    p_add.add_argument("--webhook", default="", help="飞书自定义机器人 webhook URL")
    p_add.add_argument("--channel", default="", help="OpenClaw 推送渠道")
    p_add.add_argument("--target", default="", help="OpenClaw 推送目标")
    p_add.set_defaults(fn=cmd_add)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    p_rm = sub.add_parser("remove")
    p_rm.add_argument("name")
    p_rm.set_defaults(fn=cmd_remove)
    p_st = sub.add_parser("status")
    p_st.add_argument("name")
    p_st.set_defaults(fn=cmd_status)
    p_run = sub.add_parser("run")
    p_run.add_argument("name")
    p_run.add_argument("--quiet", action="store_true")
    p_run.set_defaults(fn=cmd_run)
    p_cg = sub.add_parser("cron-gen")
    p_cg.add_argument("name", nargs="?", default=None)
    p_cg.set_defaults(fn=cmd_cron_gen)
    p_in = sub.add_parser("install")
    p_in.add_argument("name")
    p_in.set_defaults(fn=cmd_install)
    args = ap.parse_args()
    result = args.fn(args)
    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
