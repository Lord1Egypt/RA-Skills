#!/usr/bin/env python3
"""
agent-factory: 一键批量创建 OpenClaw agent + 飞书 channel 配置
用法:
  python3 setup_agents.py --config '<JSON 字符串>'
  python3 setup_agents.py --config-file agents.json
  python3 setup_agents.py --list       # 查看已有 agents
  python3 setup_agents.py --remove <id>  # 删除 agent

输入 JSON 格式:
{
  "agents": [
    {
      "id": "coder",
      "name": "代码专家",
      "emoji": "💻",
      "description": "负责写代码",         (可选)
      "feishu_app_id": "cli_xxx",
      "feishu_app_secret": "xxxxxx",
      "feishu_domain": "feishu"            (可选, 默认 feishu)
    }
  ]
}
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPENCLAW_DIR = Path.home() / ".openclaw"
CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"

# agent id 白名单：小写字母、数字、连字符，首字符必须为字母或数字，最长 32
_ID_PATTERN = re.compile(r'^[a-z0-9][a-z0-9\-]{0,31}$')


def validate_agent_id(agent_id: str) -> str:
    """校验 agent id，防止路径穿越攻击"""
    aid = agent_id.strip().lower()
    if not _ID_PATTERN.match(aid):
        raise ValueError(
            f"非法 agent id '{agent_id}'：只允许小写字母、数字、连字符，"
            f"首字符须为字母或数字，最长 32 位"
        )
    # 额外防止路径穿越（双重保险）
    if ".." in aid or "/" in aid or "\\" in aid:
        raise ValueError(f"非法 agent id '{agent_id}'：包含路径穿越字符")
    return aid


def mask_secret(secret: str) -> str:
    """只显示前 4 位，其余替换为 ****"""
    if not secret:
        return "(未提供)"
    return secret[:4] + "****"


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 配置已写入 {CONFIG_PATH}")

def get_main_auth_profiles() -> None:
    """占位：auth-profiles 由用户通过 openclaw configure 配置，不自动复制"""
    return None


# ─── 列出现有 agents ──────────────────────────────────────────────────────────

def cmd_list():
    cfg = load_config()
    agents = cfg.get("agents", {}).get("list", [])
    feishu_accounts = cfg.get("channels", {}).get("feishu", {}).get("accounts", {})

    print(f"\n{'ID':<20} {'名称':<18} {'飞书 AppId':<30} {'状态'}")
    print("─" * 80)
    for a in agents:
        aid = a["id"]
        name = a.get("name", "")
        emoji = a.get("identity", {}).get("emoji", "")
        feishu = feishu_accounts.get(aid, {})
        app_id = feishu.get("appId", "—")
        enabled = "✅" if feishu.get("enabled") else ("—" if not feishu else "❌")
        print(f"{aid:<20} {emoji+' '+name:<18} {app_id:<30} {enabled}")
    print(f"\n共 {len(agents)} 个 agents")


# ─── 删除 agent ───────────────────────────────────────────────────────────────

def cmd_remove(agent_id: str, dry_run: bool = False):
    if agent_id == "main":
        print("❌ 不允许删除 main agent")
        sys.exit(1)

    cfg = load_config()
    agent_list = cfg.get("agents", {}).get("list", [])
    existing = next((a for a in agent_list if a["id"] == agent_id), None)
    if not existing:
        print(f"❌ agent '{agent_id}' 不存在")
        sys.exit(1)

    if dry_run:
        print(f"[dry-run] 将删除 agent: {agent_id}")
        return

    # 从 agents.list 移除
    cfg["agents"]["list"] = [a for a in agent_list if a["id"] != agent_id]

    # 从 feishu accounts 移除
    feishu = cfg.get("channels", {}).get("feishu", {}).get("accounts", {})
    feishu.pop(agent_id, None)

    # 从 bindings 移除
    cfg["bindings"] = [b for b in cfg.get("bindings", [])
                       if b.get("agentId") != agent_id]

    # 从 agentToAgent.allow 移除
    allow = cfg.get("tools", {}).get("agentToAgent", {}).get("allow", [])
    if agent_id in allow:
        allow.remove(agent_id)

    save_config(cfg)
    print(f"✅ agent '{agent_id}' 已从配置中移除")
    print(f"   ⚠️  工作区目录未删除，请手动确认是否清除:")
    print(f"   rm -rf {OPENCLAW_DIR}/workspace-{agent_id}")
    print(f"   rm -rf {OPENCLAW_DIR}/agents/{agent_id}")


# ─── 创建单个 agent ───────────────────────────────────────────────────────────

def create_agent(cfg: dict, agent_cfg: dict, dry_run: bool = False) -> dict:
    """
    返回 {'status': 'created'|'skipped', 'id': ..., 'notes': [...]}
    """
    try:
        aid = validate_agent_id(agent_cfg["id"])
    except ValueError as e:
        return {"id": agent_cfg["id"], "status": "skipped", "notes": [str(e)]}
    name       = agent_cfg["name"]
    emoji      = agent_cfg.get("emoji", "🤖")
    desc       = agent_cfg.get("description", "")
    app_id     = agent_cfg.get("feishu_app_id", "")
    app_secret = agent_cfg.get("feishu_app_secret", "")
    domain     = agent_cfg.get("feishu_domain", "feishu")

    result = {"id": aid, "status": "created", "notes": []}

    # ── 检查重复 ───────────────────────────────────────────────────────────────
    agent_list  = cfg.get("agents", {}).get("list", [])
    if any(a["id"] == aid for a in agent_list):
        result["status"] = "skipped"
        result["notes"].append(f"agent id '{aid}' 已存在，跳过")
        return result

    workspace_path = OPENCLAW_DIR / f"workspace-{aid}"
    agent_dir      = OPENCLAW_DIR / "agents" / aid / "agent"

    if dry_run:
        result["notes"].append(f"[dry-run] 将创建 workspace: {workspace_path}")
        result["notes"].append(f"[dry-run] 将创建 agentDir:  {agent_dir}")
        return result

    # ── 1. 创建 workspace 目录 ─────────────────────────────────────────────────
    workspace_path.mkdir(parents=True, exist_ok=True)
    identity_md = workspace_path / "IDENTITY.md"
    if not identity_md.exists():
        identity_md.write_text(
            f"# IDENTITY.md\n\n"
            f"- **Name:** {name}\n"
            f"- **Emoji:** {emoji}\n"
            f"- **Description:** {desc or name}\n"
            f"- **Created:** {datetime.now().strftime('%Y-%m-%d')}\n",
            encoding="utf-8"
        )
        result["notes"].append(f"创建 IDENTITY.md → {identity_md}")

    # 创建基础 workspace 文件
    for fname, content in [
        ("AGENTS.md",    "# AGENTS.md\n\n多 agent 协作说明。\n"),
        ("SOUL.md",      f"# SOUL.md\n\n{name} 的行为准则与人格设定。\n"),
        ("TOOLS.md",     "# TOOLS.md\n\n工具说明与注意事项。\n"),
        ("HEARTBEAT.md", "# HEARTBEAT.md\n\n"),
    ]:
        fp = workspace_path / fname
        if not fp.exists():
            fp.write_text(content, encoding="utf-8")

    # ── 2. 创建 agentDir ──────────────────────────────────────────────────────
    agent_dir.mkdir(parents=True, exist_ok=True)

    # defaults.json — 继承全局模型配置
    defaults_file = agent_dir / "defaults.json"
    if not defaults_file.exists():
        global_defaults = cfg.get("agents", {}).get("defaults", {})
        mini_defaults = {}
        if "model" in global_defaults:
            mini_defaults["model"] = global_defaults["model"]
        defaults_file.write_text(
            json.dumps(mini_defaults, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # auth-profiles.json — 由用户通过 `openclaw configure` 配置
    result["notes"].append(f"请运行 `openclaw configure` 为 '{aid}' 配置 API key")

    # ── 3. 更新 agents.list ───────────────────────────────────────────────────
    new_agent_entry = {
        "id":        aid,
        "name":      name,
        "workspace": str(workspace_path),
        "agentDir":  str(agent_dir),
        "identity": {
            "name":  name,
            "emoji": emoji
        }
    }
    cfg.setdefault("agents", {}).setdefault("list", []).append(new_agent_entry)

    # ── 4. 添加飞书 account ───────────────────────────────────────────────────
    if app_id and app_secret:
        accounts = (cfg.setdefault("channels", {})
                       .setdefault("feishu", {})
                       .setdefault("accounts", {}))
        if aid not in accounts:
            accounts[aid] = {
                "appId":          app_id,
                "appSecret":      app_secret,
                "connectionMode": "websocket",
                "domain":         domain,
                "enabled":        True
            }
            result["notes"].append(f"飞书 account '{aid}' 已添加 (AppId: {app_id}, Secret: {mask_secret(app_secret)})")
        else:
            result["notes"].append(f"飞书 account '{aid}' 已存在，跳过")
    else:
        result["notes"].append("未提供飞书凭据，跳过飞书 channel 配置")

    # ── 5. 添加 binding ───────────────────────────────────────────────────────
    if app_id and app_secret:
        bindings = cfg.setdefault("bindings", [])
        already_bound = any(
            b.get("agentId") == aid and
            b.get("match", {}).get("channel") == "feishu" and
            b.get("match", {}).get("accountId") == aid
            for b in bindings
        )
        if not already_bound:
            bindings.append({
                "agentId": aid,
                "match": {
                    "channel":   "feishu",
                    "accountId": aid
                }
            })

    # ── 6. 加入 agentToAgent.allow ────────────────────────────────────────────
    allow = (cfg.setdefault("tools", {})
                .setdefault("agentToAgent", {})
                .setdefault("allow", []))
    if aid not in allow:
        allow.append(aid)

    return result


# ─── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 多 agent 批量配置工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config",      help="内联 JSON 字符串")
    group.add_argument("--config-file", help="JSON 配置文件路径")
    group.add_argument("--list",        action="store_true", help="列出现有 agents")
    group.add_argument("--remove",      metavar="ID", help="删除指定 agent")

    parser.add_argument("--dry-run",    action="store_true", help="仅预览，不写入")
    parser.add_argument("--restart",    action="store_true", help="完成后重启 gateway")

    args = parser.parse_args()

    if args.list:
        cmd_list()
        return

    if args.remove:
        cmd_remove(args.remove, dry_run=args.dry_run)
        if args.restart and not args.dry_run:
            print("\n🔄 重启 gateway...")
            subprocess.run(["openclaw", "gateway", "restart"], check=False)
        return

    # 解析 JSON 输入
    if args.config:
        try:
            payload = json.loads(args.config)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            sys.exit(1)
    else:
        with open(args.config_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

    agents_to_create = payload.get("agents", [])
    if not agents_to_create:
        print("❌ 未找到 agents 列表")
        sys.exit(1)

    cfg = load_config()
    results = []

    print(f"\n{'─'*50}")
    print(f"  🏭 agent-factory — 批量创建 {len(agents_to_create)} 个 agent")
    print(f"{'─'*50}")

    for a in agents_to_create:
        print(f"\n  ▶ {a.get('emoji','🤖')} {a['name']} (id: {a['id']})")
        r = create_agent(cfg, a, dry_run=args.dry_run)
        results.append(r)
        if r["status"] == "skipped":
            print(f"    ⚠️  跳过: {'; '.join(r['notes'])}")
        else:
            for note in r["notes"]:
                print(f"    • {note}")

    if not args.dry_run:
        save_config(cfg)

    # 汇总
    created = [r for r in results if r["status"] == "created"]
    skipped = [r for r in results if r["status"] == "skipped"]
    print(f"\n{'─'*50}")
    print(f"  ✅ 创建: {len(created)} 个   ⚠️  跳过: {len(skipped)} 个")
    if created:
        print(f"  新 agents: {', '.join(r['id'] for r in created)}")

    if args.restart and created and not args.dry_run:
        print("\n🔄 重启 gateway...")
        subprocess.run(["openclaw", "gateway", "restart"], check=False)
    elif created and not args.dry_run:
        print("\n  ⚡ 请手动重启 gateway 使配置生效:")
        print("     openclaw gateway restart")

    print()


if __name__ == "__main__":
    main()
