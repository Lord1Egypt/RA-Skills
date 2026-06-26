#!/usr/bin/env python3
"""
feishu-agent-provision: 克隆现有 Agent — 简洁版

流程：
    Step 1: 检查源 Agent（自动）
    Step 2: 展示源 Agent 摘要
    Step 3: 用户填写清单（每行一项）
    Step 4: 生成预览报告
    Step 5: 确认克隆 [1] / 取消 [2]
    Step 6: 执行 + 重启

用法：
    python3 clone_agent.py <SOURCE_AGENT_ID>
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
AGENTS_BASE = HOME / ".openclaw" / "agents"
OPENCLAW_CONFIG = HOME / ".openclaw" / "openclaw.json"


# ── Config ────────────────────────────────────────────────

def load_config() -> dict:
    return json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8")) if OPENCLAW_CONFIG.exists() else {}


def save_config(config: dict):
    OPENCLAW_CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_existing_agents() -> list[dict]:
    return load_config().get("agents", {}).get("list", [])


def get_bindings() -> list[dict]:
    return load_config().get("bindings", [])


# ── Source Info ────────────────────────────────────────────

def get_binding_group_id(agent_id: str) -> str | None:
    binding = next((b for b in get_bindings() if b.get("agentId") == agent_id), None)
    return binding.get("match", {}).get("peer", {}).get("id") if binding else None


def get_source_crons(source_id: str) -> list[dict]:
    try:
        result = subprocess.run(["openclaw", "cron", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return []
    except Exception:
        return []

    crons, current = [], {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("Name:"):
            if current:
                crons.append(current)
            current = {"name": line.split("Name:", 1)[1].strip()}
        elif line.startswith("Schedule:"):
            current["schedule"] = line.split("Schedule:", 1)[1].strip()
    if current:
        crons.append(current)

    return [c for c in crons if c.get("name", "").startswith(f"{source_id}-")]


def read_workspace_files(source_id: str) -> dict[str, str]:
    ws = AGENTS_BASE / source_id / "workspace"
    files = {}
    for fname in ["SOUL.md", "USER.md", "AGENTS.md", "HEARTBEAT.md"]:
        fpath = ws / fname
        if fpath.exists():
            files[fname] = fpath.read_text(encoding="utf-8")
    return files


# ── SOUL.md / USER.md auto-generation ──────────────────────

def generate_soul_minimal(new_id: str, new_name: str) -> str:
    date_str = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    return f"""# {new_name}

## 基本信息
- **Agent ID**: {new_id}
- **创建时间**: {date_str}
- **角色**: （待填写）

## Session 模式
- sessionTarget: session:{new_id}
- 备份策略：启动时读 backup.md，结束时写 backup.md
"""


def generate_user_minimal() -> str:
    return """# USER.md - Service Target

## 服务对象
- （待填写）

## 科目
- （待填写）
"""


def parse_soul_input(raw: str, new_id: str) -> str:
    """根据用户单行格式生成 SOUL.md"""
    fields = {}
    for part in raw.split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            fields[k.strip()] = v.strip()

    new_name = fields.get("中文名", "新Agent")
    subject = fields.get("科目", "（待填写）")
    duty = fields.get("职责", "（待填写）")
    role = fields.get("角色", "（待填写）")

    date_str = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    return f"""# {new_name}

## 基本信息
- **Agent ID**: {new_id}
- **创建时间**: {date_str}
- **中文名**: {new_name}
- **科目**: {subject}
- **角色**: {role}

## 职责
{duty}

## Session 模式
- sessionTarget: session:{new_id}
- 备份策略：启动时读 backup.md，结束时写 backup.md
"""


def parse_user_input(raw: str) -> str:
    """根据用户单行格式生成 USER.md"""
    fields = {}
    for part in raw.split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            fields[k.strip()] = v.strip()

    target = fields.get("服务对象", "（待填写）")
    subject = fields.get("科目", "（待填写）")

    return f"""# USER.md - Service Target

## 服务对象
- {target}

## 科目
- {subject}
"""


# ── Clone logic ─────────────────────────────────────────────

def apply_replacements(content: str, replacements: dict) -> str:
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def create_new_workspace(new_id: str, files: dict[str, str]) -> Path:
    new_ws = AGENTS_BASE / new_id / "workspace"
    new_ws.mkdir(parents=True, exist_ok=True)
    (new_ws / "memory").mkdir(exist_ok=True)

    for fname in ["SOUL.md", "USER.md", "AGENTS.md", "HEARTBEAT.md"]:
        if fname in files:
            (new_ws / fname).write_text(files[fname], encoding="utf-8")

    date_str = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    backup = f"""# {new_id} 备份状态

## 基本信息
- 创建时间：{date_str}
- Session 长效性：长期

## 当前状态
- 最后更新时间：（初始化）
- 当前进度：（新 Agent）
- 待处理事项：（待定）

## Session 模式
- sessionTarget: session:{new_id}
- 备份策略：启动时读 backup.md，结束时写 backup.md
"""
    (new_ws / "memory" / "backup.md").write_text(backup, encoding="utf-8")
    return new_ws


def register_new_agent(new_id: str, new_ws: Path, new_name: str,
                      new_group_id: str | None) -> tuple[bool, str]:
    config = load_config()
    if "agents" not in config:
        config["agents"] = {"list": []}
    if "list" not in config["agents"]:
        config["agents"]["list"] = []

    if any(a.get("id") == new_id for a in config["agents"]["list"]):
        return False, f"Agent {new_id} 已存在"

    config["agents"]["list"].append({
        "id": new_id,
        "workspace": str(new_ws),
        "identity": {"name": new_name}
    })

    if new_group_id:
        if "bindings" not in config:
            config["bindings"] = []
        config["bindings"].append({
            "type": "route",
            "agentId": new_id,
            "match": {
                "channel": "feishu",
                "accountId": "main",
                "peer": {"kind": "group", "id": new_group_id}
            }
        })

    save_config(config)
    return True, "注册成功"


def clone_crons(source_id: str, new_id: str,
                new_hour: int | None = None,
                new_min: int | None = None) -> tuple[bool, list[str]]:
    source_crons = get_source_crons(source_id)
    if not source_crons:
        return True, ["无 Cron 任务"]

    results = []
    for cron in source_crons:
        old_name = cron.get("name", "")
        new_name = old_name.replace(source_id, new_id)
        schedule_str = cron.get("schedule", "")

        # 如需修改时间
        if new_hour is not None:
            # 替换 schedule 中的小时和分钟
            schedule_str = re.sub(r"^\d+\s+\d+\s+\*", f"{new_hour} {new_min or 0} *", schedule_str, count=1)

        cmd = [
            "openclaw", "cron", "add",
            "--name", new_name,
            "--schedule", schedule_str,
            "--tz", "Asia/Shanghai",
            "--session", f"session:{new_id}",
            "--message", f"📋 {new_id} 定时任务时间到！请执行对应任务。"
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            results.append(f"✅ {new_name}  ({schedule_str})" if r.returncode == 0 else f"⚠️ {new_name}: {r.stderr}")
        except Exception as e:
            results.append(f"⚠️ {new_name}: {e}")

    return all(r.startswith("✅") for r in results), results


def restart_gateway() -> tuple[bool, str]:
    try:
        r = subprocess.run(["openclaw", "gateway", "restart"], capture_output=True, text=True, timeout=30)
        return (True, "重启成功") if r.returncode == 0 else (False, f"重启失败: {r.stderr}")
    except Exception as e:
        return False, f"异常: {e}"


def send_test_message(group_id: str, new_id: str) -> tuple[bool, str]:
    try:
        r = subprocess.run(
            ["openclaw", "message", "send",
             "--channel", "feishu", "--to", group_id,
             "--message", f"✅ Agent「{new_id}」已上线！请确认收到此消息。"],
            capture_output=True, text=True, timeout=15
        )
        return (True, "已发送测试消息") if r.returncode == 0 else (False, f"发送失败: {r.stderr}")
    except Exception as e:
        return False, f"异常: {e}"


# ── Parse checklist reply ──────────────────────────────────

def parse_checklist_reply(source_id: str, lines: list[str]) -> dict:
    """解析用户清单回复，返回配置字典"""
    result = {
        "new_id": None,
        "new_group": None,
        "cron_mode": "1",       # 1=克隆 2=不克隆 3=修改时间
        "cron_time": None,       # "HH:MM"
        "soul_mode": "1",        # 1=克隆 2=minimal 3=自定义
        "soul_custom": None,     # 用户填写的单行格式字符串
        "user_mode": "1",
        "user_custom": None,
        "agents_mode": "1",      # 1=克隆 2=跳过
        "heartbeat_mode": "1",   # 1=克隆 2=跳过
    }

    # 按顺序映射（忽略空行）
    items = [l.strip() for l in lines if l.strip()]

    if len(items) >= 1:
        result["new_id"] = items[0]
    if len(items) >= 2:
        result["new_group"] = items[1] if items[1] else None
    if len(items) >= 3:
        val = items[2].strip()
        if val.startswith("3"):
            # 提取时间，如 "3 21:30" 或 "3"
            parts = val.split()
            result["cron_mode"] = "3"
            if len(parts) >= 2:
                result["cron_time"] = parts[1]
        else:
            result["cron_mode"] = val if val in ("1", "2") else "1"
    if len(items) >= 4:
        result["soul_mode"] = items[3] if items[3] in ("1", "2", "3") else "1"
    if len(items) >= 5:
        result["user_mode"] = items[4] if items[4] in ("1", "2", "3") else "1"
    if len(items) >= 6:
        result["agents_mode"] = items[5] if items[5] in ("1", "2") else "1"
    if len(items) >= 7:
        result["heartbeat_mode"] = items[6] if items[6] in ("1", "2") else "1"

    return result


# ── Main ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="克隆飞书群 Agent")
    parser.add_argument("source_id", help="原 Agent ID")
    args = parser.parse_args()
    source_id = args.source_id

    # ── Step 1: 检查源 Agent ──
    agents = get_existing_agents()
    if not any(a.get("id") == source_id for a in agents):
        print(f"❌ 原 Agent「{source_id}」不存在。可用：{[a.get('id') for a in agents]}")
        sys.exit(1)

    # ── 读取源信息 ──
    files = read_workspace_files(source_id)
    if not files:
        print("❌ 无法读取 workspace 文件")
        sys.exit(1)

    soul = files.get("SOUL.md", "")
    user = files.get("USER.md", "")
    agents_file = files.get("AGENTS.md", "")
    heartbeat = files.get("HEARTBEAT.md", "")

    src_group = get_binding_group_id(source_id)
    src_crons = get_source_crons(source_id)
    src_name = next(
        (a.get("identity", {}).get("name", "") for a in agents if a.get("id") == source_id), ""
    )

    # ── Step 2: 展示源 Agent 摘要 ──
    print()
    print("=" * 56)
    print(f"📋 克隆来源：{source_id}")
    print("=" * 56)

    print(f"\n【基本信息】")
    print(f"  • 中文名：{src_name}")
    print(f"  • 原飞书群：{src_group or '（无）'}")

    print(f"\n【Cron 定时任务】")
    if src_crons:
        for c in src_crons:
            print(f"  • {c.get('name')}  |  {c.get('schedule')}")
    else:
        print(f"  （无）")

    print(f"\n【SOUL.md 核心内容】")
    soul_lines = [l for l in soul.splitlines() if l.strip()][:12]
    for l in soul_lines:
        print(f"  {l}")
    if len(soul.splitlines()) > 12:
        print(f"  ... （共 {len(soul.splitlines())} 行）")

    print(f"\n【USER.md 核心内容】")
    user_lines = [l for l in user.splitlines() if l.strip()][:10]
    for l in user_lines:
        print(f"  {l}")
    if len(user.splitlines()) > 10:
        print(f"  ... （共 {len(user.splitlines())} 行）")

    print(f"\n【AGENTS.md】")
    print(f"  标准工作区引导（通用内容，直接克隆）")
    print(f"\n【HEARTBEAT.md】")
    print(f"  通常为空或注释（直接克隆）")

    # ── Step 3: 填写清单 ──
    print()
    print("=" * 56)
    print("📌 请按顺序回复，每行一项，空行使用默认值")
    print("=" * 56)

    print("""
【清单格式】

1. 新 Agent ID：chemistry-tutor
2. 新飞书群：oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
3. Cron策略：1
   （1=克隆原 Cron；2=不克隆；3=克隆并改为 HH:MM）
4. SOUL.md：1
   （1=克隆仅替换ID；2=留空自动生成minimal；3=修改内容）
5. USER.md：1
   （1=克隆仅替换ID；2=留空自动生成minimal；3=修改内容）
6. AGENTS.md：1
   （1=克隆；2=跳过）
7. HEARTBEAT.md：1
   （1=克隆；2=跳过）
""")

    print("请填写（直接回车逐项使用默认值）：")

    # 收集清单（逐行询问，空行给默认值）
    defaults = {
        "1": source_id + "-v2",
        "2": src_group or "",
        "3": "1",
        "4": "1",
        "5": "1",
        "6": "1",
        "7": "1",
    }

    items = {}
    prompts = [
        ("1. 新 Agent ID：", "new_id"),
        ("2. 新飞书群（回车跳过/不绑定）：", "new_group"),
        ("3. Cron策略（1/2/3）：", "cron_mode"),
        ("4. SOUL.md（1/2/3）：", "soul_mode"),
        ("5. USER.md（1/2/3）：", "user_mode"),
        ("6. AGENTS.md（1/2）：", "agents_mode"),
        ("7. HEARTBEAT.md（1/2）：", "heartbeat_mode"),
    ]

    for prompt, key in prompts:
        default_val = defaults.get(key, "")
        line = input(prompt).strip()
        items[key] = line if line else default_val

    # 处理 Cron 策略 3（修改时间）
    cron_time = None
    if items.get("cron_mode", "1") == "3":
        print("  如选 3，请输入新时间（格式 HH:MM，回车使用默认）：")
        # 尝试从源 cron 提取默认时间
        default_t = "21:00"
        if src_crons:
            m = re.search(r"(\d+)\s+(\d+)\s+\*", src_crons[0].get("schedule", ""))
            if m:
                default_t = f"{int(m.group(1))}:{int(m.group(2)):02d}"
        t = input(f"  新 Cron 时间（HH:MM，默认 {default_t}）：").strip()
        cron_time = t if t else default_t
        items["cron_time"] = cron_time

    # 处理修改内容（选项 3）
    soul_custom = None
    user_custom = None

    if items.get("soul_mode") == "3":
        print("""
【SOUL.md 修改内容】请按以下格式填写：

  格式：中文名=xxx | 科目=xxx | 职责=xxx | 角色=xxx
  示例：中文名=中考化学辅导 | 科目=化学 | 职责=中考化学苏格拉底式辅导 | 角色=AI化学辅导老师
（直接回车使用默认值：中文名=<新ID> | 科目=待填写 | 职责=待填写 | 角色=待填写）
""")
        default_soul = f"中文名={items.get('new_id')} | 科目=待填写 | 职责=待填写 | 角色=待填写"
        line = input("SOUL修改内容：").strip()
        soul_custom = line if line else default_soul

    if items.get("user_mode") == "3":
        print("""
【USER.md 修改内容】请按以下格式填写：

  格式：服务对象=xxx | 科目=xxx
  示例：服务对象=中考学生 | 科目=化学
（直接回车使用默认值：服务对象=待填写 | 科目=待填写）
""")
        default_user = "服务对象=待填写 | 科目=待填写"
        line = input("USER修改内容：").strip()
        user_custom = line if line else default_user

    # ── Step 3.5: 验证清单 ──
    new_id = items.get("new_id", "")
    new_group = items.get("new_group") or None

    if not new_id:
        print("❌ 新 Agent ID 不能为空")
        sys.exit(1)

    if any(a.get("id") == new_id for a in agents):
        print(f"❌ ID「{new_id}」已被占用")
        sys.exit(1)

    if new_group and new_group == src_group:
        print("❌ 禁止同群绑定")
        sys.exit(1)

    if new_group:
        for b in get_bindings():
            if b.get("match", {}).get("peer", {}).get("id") == new_group:
                print(f"❌ 飞书群已绑定到 Agent「{b.get('agentId')}」")
                sys.exit(1)

    # ── Step 4: 构建文件内容 ──
    replacements = {source_id: new_id}
    new_files = {}

    # SOUL.md
    soul_mode = items.get("soul_mode", "1")
    if soul_mode == "1":
        new_files["SOUL.md"] = apply_replacements(soul, replacements)
    elif soul_mode == "2":
        new_files["SOUL.md"] = generate_soul_minimal(new_id, new_id)
    else:  # "3"
        new_files["SOUL.md"] = parse_soul_input(soul_custom or "", new_id)

    # USER.md
    user_mode = items.get("user_mode", "1")
    if user_mode == "1":
        new_files["USER.md"] = apply_replacements(user, replacements)
    elif user_mode == "2":
        new_files["USER.md"] = generate_user_minimal()
    else:  # "3"
        new_files["USER.md"] = parse_user_input(user_custom or "")

    # AGENTS.md / HEARTBEAT.md
    new_files["AGENTS.md"] = agents_file if items.get("agents_mode") == "1" else ""
    new_files["HEARTBEAT.md"] = heartbeat if items.get("heartbeat_mode") == "1" else ""

    # Cron 时间处理
    cron_hour, cron_min = None, None
    if items.get("cron_mode") == "3" and cron_time:
        parts = cron_time.split(":")
        cron_hour = int(parts[0])
        cron_min = int(parts[1]) if len(parts) > 1 else 0

    clone_cron = items.get("cron_mode") != "2"

    # ── 生成预览报告 ──
    print()
    print("=" * 56)
    print("📋 克隆预览报告")
    print("=" * 56)

    print(f"\n【基本信息】")
    print(f"  • 来源 Agent：{source_id}")
    print(f"  • 新 Agent ID：{new_id}")
    print(f"  • 新飞书群：{new_group or '（不绑定）'}")

    print(f"\n【文件处理】")
    soul_status = {
        "1": "🔄 克隆（仅替换ID）",
        "2": "📝 留空自动生成 minimal",
        "3": "✏️  用户自定义内容"
    }.get(soul_mode, "?")
    user_status = {
        "1": "🔄 克隆（仅替换ID）",
        "2": "📝 留空自动生成 minimal",
        "3": "✏️  用户自定义内容"
    }.get(user_mode, "?")
    print(f"  • SOUL.md：{soul_status}")
    print(f"  • USER.md：{user_status}")
    print(f"  • AGENTS.md：{'🔄 克隆' if items.get('agents_mode')=='1' else '⏭ 跳过'}")
    print(f"  • HEARTBEAT.md：{'🔄 克隆' if items.get('heartbeat_mode')=='1' else '⏭ 跳过'}")

    print(f"\n【Cron 定时任务】")
    if clone_cron and src_crons:
        for c in src_crons:
            new_name = c["name"].replace(source_id, new_id)
            sched = c.get("schedule", "")
            if cron_hour is not None:
                sched = re.sub(r"^\d+\s+\d+\s+\*", f"{cron_hour} {cron_min} *", sched, count=1)
            print(f"  • {new_name}  |  {sched}")
    elif clone_cron:
        print(f"  （无 Cron 任务）")
    else:
        print(f"  • 不克隆（跳过）")

    print(f"\n【SOUL.md 预览】")
    soul_preview = new_files["SOUL.md"].splitlines()[:8]
    for l in soul_preview:
        print(f"  {l}")
    if len(new_files["SOUL.md"].splitlines()) > 8:
        print(f"  ...")

    print(f"\n【USER.md 预览】")
    user_preview = new_files["USER.md"].splitlines()[:6]
    for l in user_preview:
        print(f"  {l}")

    # ── Step 5: 确认 ──
    print()
    reply = input("确认开始克隆？[1] 是 / [2] 否：").strip()
    if reply != "1":
        print("❌ 已取消")
        sys.exit(0)

    # ── Step 6: 执行 ──
    print(f"\n⏱️  开始创建 Agent「{new_id}」...")

    print("\n📌 创建 Workspace...")
    new_ws = create_new_workspace(new_id, new_files)
    print(f"   ✅ {new_ws}")

    print("\n📌 注册 Agent...")
    ok, msg = register_new_agent(new_id, new_ws, new_id, new_group)
    if not ok:
        print(f"   ❌ {msg}")
        sys.exit(1)
    print(f"   ✅ {msg}")

    if clone_cron:
        print("\n📌 克隆 Cron...")
        ok, results = clone_crons(source_id, new_id, cron_hour, cron_min)
        for r in results:
            print(f"   {r}")
    else:
        print("\n📌 Cron：跳过")

    # 重启
    print()
    restart_reply = input("Gateway 重启：[1] 立即 / [2] 稍后手动：").strip()
    if restart_reply == "1":
        print("\n📌 重启 Gateway...")
        ok, msg = restart_gateway()
        print(f"   {'✅' if ok else '⚠️'} {msg}")

    if new_group:
        print("\n📌 发送测试消息...")
        ok, msg = send_test_message(new_group, new_id)
        print(f"   {'✅' if ok else '⚠️'} {msg}")

    print()
    print("=" * 56)
    print(f"✅ 克隆完成！Agent「{new_id}」已创建。")
    print("   config 已修改，重启后生效。")
    print("=" * 56)


if __name__ == "__main__":
    main()
