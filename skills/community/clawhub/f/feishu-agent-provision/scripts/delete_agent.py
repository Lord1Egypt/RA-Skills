#!/usr/bin/env python3
"""
feishu-agent-provision: 删除指定的飞书群 Agent

用法：
    python3 delete_agent.py <AGENT_ID> [--force]

流程：
    Step 1: 检查 Agent 是否存在
    Step 2: 检查活跃 Session（有则警告）
    Step 3: 列出清理清单（预览）
    Step 4: 等待用户输入「确认删除」
    Step 5: 执行清理（cron → bindings → agents.list → workspace trash → 重启）
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
AGENTS_BASE = HOME / ".openclaw" / "agents"
OPENCLAW_CONFIG = HOME / ".openclaw" / "openclaw.json"


def load_config() -> dict:
    """加载 openclaw.json 配置"""
    if not OPENCLAW_CONFIG.exists():
        return {}
    return json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))


def save_config(config: dict):
    """保存 openclaw.json 配置"""
    OPENCLAW_CONFIG.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )


def get_existing_agents() -> list[dict]:
    """获取所有已注册的 Agent"""
    config = load_config()
    return config.get("agents", {}).get("list", [])


def get_agent_workspace(agent_id: str) -> Path:
    """获取 Agent workspace 路径"""
    return AGENTS_BASE / agent_id / "workspace"


def get_agent_crons(agent_id: str) -> list[str]:
    """获取该 Agent 相关的所有 Cron 任务名称"""
    return [f"{agent_id}-daily-report", f"{agent_id}-weekly-report"]


def get_active_sessions(agent_id: str) -> list[dict]:
    """检查是否有活跃的 Agent session"""
    # 通过 openclaw sessions list 获取
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "list", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return []
        sessions = json.loads(result.stdout)
        # 过滤出属于该 agent 的 session
        return [
            s for s in sessions
            if s.get("agentId") == agent_id or s.get("sessionKey", "").startswith(f"session:{agent_id}")
        ]
    except Exception:
        return []


def list_cleanup_preview(agent_id: str, group_id: str | None) -> str:
    """生成清理清单预览"""
    workspace_path = get_agent_workspace(agent_id)
    crons = get_agent_crons(agent_id)

    lines = [
        f"⚠️ 即将删除 Agent「{agent_id}」：",
        "",
        "【将清理的组件】",
        f"├── 🗂️ Workspace: {workspace_path}/",
        "│   ├── SOUL.md",
        "│   ├── USER.md",
        "│   ├── AGENTS.md",
        "│   ├── HEARTBEAT.md",
        "│   └── memory/",
        "",
        "├── ⏰ Cron 定时任务（将删除）：",
    ]
    for cron in crons:
        lines.append(f"│   ├── {cron}")
    lines.append("")

    if group_id:
        lines.append(f"├── 🔗 飞书群绑定: {group_id}")
        lines.append("│   └── 群消息将退回主 Agent")
    else:
        lines.append("├── 🔗 飞书群绑定: 未找到绑定记录")

    lines.extend([
        "",
        "└── 📋 Agent 注册: {agent_id}（从 agents.list 移除）",
        "",
        "【操作说明】",
        "• Workspace 使用 trash 而非 rm，可在系统 trash 中恢复",
        "• 删除后飞书群消息将由主 Agent 响应",
        "",
        "⚠️ 此操作不可逆！",
    ])

    return "\n".join(lines)


def delete_crons(agent_id: str) -> tuple[bool, list[str]]:
    """删除 Agent 的所有 Cron 任务"""
    crons = get_agent_crons(agent_id)
    deleted = []
    failed = []

    for cron_name in crons:
        try:
            result = subprocess.run(
                ["openclaw", "cron", "remove", cron_name],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                deleted.append(cron_name)
            else:
                failed.append(cron_name)
        except Exception:
            failed.append(cron_name)

    return len(failed) == 0, deleted + (["部分失败"] if failed else [])


def remove_binding(agent_id: str) -> tuple[bool, str]:
    """从 bindings 中移除该 Agent 的绑定"""
    config = load_config()
    bindings = config.get("bindings", [])

    original_count = len(bindings)
    bindings = [b for b in bindings if b.get("agentId") != agent_id]

    if len(bindings) == original_count:
        return True, "无绑定记录（可能已清除或未绑定）"

    config["bindings"] = bindings
    save_config(config)
    return True, f"已移除 bindings"


def remove_agent_from_list(agent_id: str) -> tuple[bool, str]:
    """从 agents.list 中移除该 Agent"""
    config = load_config()
    agents_list = config.get("agents", {}).get("list", [])

    original_count = len(agents_list)
    agents_list = [a for a in agents_list if a.get("id") != agent_id]

    if len(agents_list) == original_count:
        return False, "未在 agents.list 中找到该 Agent"

    # 确保结构完整
    if "agents" not in config:
        config["agents"] = {}
    config["agents"]["list"] = agents_list

    save_config(config)
    return True, f"已从 agents.list 移除"


def cleanup_residual_only(agent_id: str, force: bool = False) -> tuple[bool, str]:
    """仅清理残留 workspace（不处理 config / cron）；先尝试 trash，失败时询问用户"""
    workspace_path = AGENTS_BASE / agent_id
    if not workspace_path.exists():
        return True, "Workspace 不存在，跳过"

    # 先尝试 trash
    try:
        shutil.move(str(workspace_path), str(HOME / ".Trash" / agent_id))
        return True, f"已移至 trash: {HOME}/.Trash/{agent_id}"
    except Exception as trash_error:
        # trash 失败，返回错误让调用方处理，不静默永久删除
        return False, f"移至 trash 失败: {trash_error}（如需强制删除请使用 --force）"


def validate_agent_id(agent_id: str) -> bool:
    """校验 agent_id 格式，防止路径穿越。只允许小写字母、数字、短横线。"""
    if not re.match(r'^[a-z0-9-]+$', agent_id):
        return False
    if '..' in agent_id or '/' in agent_id or '\\' in agent_id:
        return False
    return True


def trash_workspace(agent_id: str) -> tuple[bool, str]:
    """将 Agent workspace 目录移至 trash；失败时返回 False 和错误信息，由调用方决定是否执行永久删除"""
    workspace_path = (AGENTS_BASE / agent_id).resolve()
    expected_base = AGENTS_BASE.resolve()

    # 路径安全校验：拒绝任何试图跳出 ~/.openclaw/agents/ 的路径
    if not str(workspace_path).startswith(str(expected_base)):
        return False, f"路径校验失败：拒绝危险路径 {workspace_path}"

    if not workspace_path.exists():
        return True, "Workspace 不存在，跳过"

    try:
        # macOS trash
        shutil.move(str(workspace_path), str(HOME / ".Trash" / agent_id))
        return True, f"已移至 trash: {HOME}/.Trash/{agent_id}"
    except Exception as e:
        # trash 失败，不静默降级为永久删除，而是返回错误让调用方处理
        return False, f"移至 trash 失败: {e}（将执行永久删除，请确认）"


def force_delete_workspace(agent_id: str) -> tuple[bool, str]:
    """强制永久删除 workspace（仅在用户明确确认后调用）"""
    workspace_path = (AGENTS_BASE / agent_id).resolve()
    if not workspace_path.exists():
        return True, "Workspace 不存在，跳过"
    try:
        shutil.rmtree(workspace_path)
        return True, "已永久删除"
    except Exception as e:
        return False, f"删除失败: {e}"


def restart_gateway() -> tuple[bool, str]:
    """重启 Gateway"""
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, "Gateway 重启成功"
        else:
            return False, f"Gateway 重启失败: {result.stderr}"
    except Exception as e:
        return False, f"Gateway 重启异常: {e}"


def main():
    parser = argparse.ArgumentParser(description="删除飞书群 Agent 或清理残留")
    parser.add_argument("agent_id", help="要删除的 Agent ID（只允许小写字母、数字、短横线）")
    parser.add_argument("--force", action="store_true", help="跳过活跃 Session 检查，强制删除")
    parser.add_argument("--no-restart", action="store_true", help="删除完成后不自动重启，询问用户何时重启")
    args = parser.parse_args()

    agent_id = args.agent_id

    # 校验 agent_id 格式，防止路径穿越
    if not validate_agent_id(agent_id):
        print(f"❌ 危险：Agent ID「{agent_id}」格式不合格。")
        print("   只允许：小写字母、数字、短横线（a-z, 0-9, -）")
        print("   禁止：空格、下划线、斜杠、点号等特殊字符")
        sys.exit(1)

    print(f"🔍 检查 Agent「{agent_id}」...")

    # Step 1: 检查 Agent 是否存在于注册列表
    agents = get_existing_agents()
    agent_entry = next((a for a in agents if a.get("id") == agent_id), None)
    
    # Step 1.5: 检查是否有残留 Workspace
    workspace_path = AGENTS_BASE / agent_id
    has_residual = workspace_path.exists()
    
    # 分两种情况：已注册 / 仅残留
    if not agent_entry:
        # Agent 未注册，检查是否有残留
        if not has_residual:
            # 都不存在，完全干净
            available = [a.get("id") for a in agents]
            print(f"❌ Agent「{agent_id}」不存在，也无残留。")
            if available:
                print(f"   可用的 Agent：{', '.join(available)}")
            sys.exit(1)
        else:
            # 有残留 Workspace
            print(f"⚠️  Agent「{agent_id}」未注册，但发现残留：")
            print(f"   残留目录: {workspace_path}")
            # 列出残留内容
            for subdir in ['workspace', 'agent', 'sessions']:
                subp = workspace_path / subdir
                if subp.exists():
                    print(f"   • {subdir}/")
            print("将清理这些残留目录。")
            
            reply = input('输入「确认删除」继续清理，或任意内容取消：').strip()
            if reply != "确认删除":
                print("\n❌ 已取消。")
                sys.exit(0)
            
            print("\n⏱️  清理残留...")
            ok, msg = cleanup_residual_only(agent_id)
            if ok:
                print(f"✅ 残留已清理：{workspace_path}")
            else:
                print(f"⚠️  移至 trash 失败：{msg}")
                reply = input("是否强制永久删除？（输入「强制删除」确认，任意内容取消）：").strip()
                if reply == "强制删除":
                    ok2, msg2 = force_delete_workspace(agent_id)
                    print(f"{'✅' if ok2 else '⚠️'} {msg2}")
                else:
                    print("❌ 已取消，残留保留。")
            print("（Agent 未注册，无其他清理操作）")
            sys.exit(0)
    
    # Agent 已注册，继续正常删除流程

    # 查找对应的 binding
    config = load_config()
    bindings = config.get("bindings", [])
    binding = next((b for b in bindings if b.get("agentId") == agent_id), None)
    group_id = binding.get("match", {}).get("peer", {}).get("id") if binding else None

    print(f"✅ 找到 Agent「{agent_id}」")
    if group_id:
        print(f"   绑定飞书群：{group_id}")

    # Step 2: 检查活跃 Session（除非 --force）
    if not args.force:
        active = get_active_sessions(agent_id)
        if active:
            print("")
            print(f"⚠️  Agent「{agent_id}」当前有活跃会话：")
            for s in active:
                print(f"   • {s.get('sessionKey', 'unknown')}（启动中）")
            print("")
            print("强行删除可能导致正在运行的任务异常中断。")
            print("")
            print("选项：")
            print("  1. 在飞书群发送「停止服务」指令，等待 Agent 回复后再试")
            print("  2. 回复「强制删除」继续（不推荐）")
            print("  3. 回复「取消」中止操作")
            print("")
            reply = input("请输入选项（1/2/3）或「取消」：").strip()
            if reply == "强制删除":
                print("\n⚠️ 强制删除模式：跳过活跃 Session 检查")
            elif reply != "强制删除":
                print("\n❌ 已取消删除操作。")
                sys.exit(0)

    # Step 3: 显示清理清单
    print("")
    print(list_cleanup_preview(agent_id, group_id))
    print("")

    # Step 4: 等待确认
    reply = input('输入「确认删除」继续，或任意内容取消：').strip()
    if reply != "确认删除":
        print("\n❌ 已取消删除操作。")
        sys.exit(0)

    print("\n⏱️  开始执行清理...")

    # Step 5: 执行清理
    results = {}

    # 5.1 删除 Cron
    print("\n📌 清理 Cron 定时任务...")
    ok, msg = delete_crons(agent_id)
    results["cron"] = (ok, msg)
    print(f"   {'✅' if ok else '⚠️'} {msg}")

    # 5.2 移除 bindings
    print("\n📌 清理飞书群绑定...")
    ok, msg = remove_binding(agent_id)
    results["binding"] = (ok, msg)
    print(f"   {'✅' if ok else '⚠️'} {msg}")

    # 5.3 移除 agents.list
    print("\n📌 清理 Agent 注册...")
    ok, msg = remove_agent_from_list(agent_id)
    results["agent_list"] = (ok, msg)
    print(f"   {'✅' if ok else '⚠️'} {msg}")

    # 5.4 删除 workspace（先尝试 trash，失败时询问是否强制删除）
    print("\n📌 清理 Workspace...")
    ok, msg = trash_workspace(agent_id)
    if ok:
        results["workspace"] = (True, msg)
        print(f"   ✅ {msg}")
    else:
        print(f"   ⚠️  {msg}")
        reply = input("是否强制永久删除？（输入「强制删除」确认，任意内容取消）：").strip()
        if reply == "强制删除":
            ok2, msg2 = force_delete_workspace(agent_id)
            results["workspace"] = (ok2, msg2)
            print(f"   {'✅' if ok2 else '⚠️'} {msg2}")
        else:
            results["workspace"] = (False, "已取消，workspace 保留")
            print("   ❌ 已取消，workspace 保留")

    # 5.5 重启 Gateway
    if args.no_restart:
        # 不自动重启，询问用户
        print("\n" + "=" * 50)
        print(f"✅ 删除完成！Agent「{agent_id}」已清理：")
        print("")
        for component, (ok, msg) in results.items():
            icon = "✅" if ok else "⚠️"
            print(f"  {icon} {component}: {msg}")
        print("")
        print("⚠️  config 已修改，重启后生效")
        print("")
        print("Gateway 重启选项：")
        print("  [1] 立即重启（推荐，删除立即生效）")
        print("  [2] 稍后手动重启")
        print("")
        reply = input("请回复 1 或 2：").strip()
        if reply == "1":
            print("\n📌 立即重启 Gateway...")
            ok, msg = restart_gateway()
            print(f"   {'✅' if ok else '⚠️'} {msg}")
            print("")
            print("=" * 50)
            print("🎉 删除完成，Gateway 已重启！现在可以继续对话。")
            if group_id:
                print("")
                print(f"📌 后续：飞书群 {group_id[:12]}... 的消息现在由主 Agent 响应")
        else:
            print("\n📌 删除步骤已全部完成。")
            print("   注意：config 已修改，重启后才生效。")
            print("")
            print("=" * 50)
            print("✅ 删除步骤完成。现在可以继续对话。")
            print("   （config 已修改，重启后生效）")
            print("")
            print("📌 记得稍后手动重启：openclaw gateway restart")
    else:
        # 正常自动重启
        print("\n📌 重启 Gateway...")
        ok, msg = restart_gateway()
        results["gateway"] = (ok, msg)
        print(f"   {'✅' if ok else '⚠️'} {msg}")

        # 汇总
        print("\n" + "=" * 50)
        print(f"✅ 删除完成！Agent「{agent_id}」已清理：")
        print("")
        for component, (ok, msg) in results.items():
            icon = "✅" if ok else "⚠️"
            print(f"  {icon} {component}: {msg}")
        print("")
        print("🎉 删除完成，Gateway 已重启！现在可以继续对话。")
        
        if group_id:
            print("")
            print(f"📌 后续：飞书群 {group_id[:12]}... 的消息现在由主 Agent 响应")


if __name__ == "__main__":
    main()
