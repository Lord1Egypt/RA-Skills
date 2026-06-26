#!/usr/bin/env python3
"""多Agent协调分析 - 付费版

用法:
    python3 multi_agent_coordinator.py --action dependencies
    python3 multi_agent_coordinator.py --action topology
    python3 multi_agent_coordinator.py --action conflicts
    python3 multi_agent_coordinator.py --action health
"""

import argparse
import json
import os
import sys
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SKILLS_DIR = os.path.expanduser("~/.openclaw/skills")
SYSTEM_SKILLS_DIR = os.path.expanduser(
    "~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/skills"
)


def discover_agents():
    """发现已配置的Agent"""
    agents = []

    # 扫描 workspace 目录
    if os.path.isdir(WORKSPACE):
        for name in os.listdir(WORKSPACE):
            agent_dir = os.path.join(WORKSPACE, name)
            if os.path.isdir(agent_dir):
                agent_info = {
                    "name": name,
                    "path": agent_dir,
                    "has_soul": os.path.exists(os.path.join(agent_dir, "SOUL.md")),
                    "has_memory": os.path.isdir(os.path.join(agent_dir, "memory")),
                }
                # 尝试读取 SOUL.md 获取角色信息
                soul_path = os.path.join(agent_dir, "SOUL.md")
                if os.path.exists(soul_path):
                    try:
                        with open(soul_path, "r") as f:
                            content = f.read(500)
                        # 尝试提取角色描述
                        for line in content.split("\n")[:10]:
                            line = line.strip()
                            if any(kw in line.lower() for kw in ["agent", "角色", "role"]):
                                agent_info["role_hint"] = line[:80]
                                break
                    except Exception:
                        pass
                agents.append(agent_info)

    return agents


def discover_skills():
    """发现可用技能"""
    skills = []
    for base_dir in [SKILLS_DIR, SYSTEM_SKILLS_DIR]:
        if os.path.isdir(base_dir):
            for name in os.listdir(base_dir):
                skill_dir = os.path.join(base_dir, name)
                skill_md = os.path.join(skill_dir, "SKILL.md")
                if os.path.exists(skill_md):
                    skills.append({
                        "name": name,
                        "path": skill_dir,
                        "source": "user" if base_dir == SKILLS_DIR else "system",
                    })
    return skills


def analyze_dependencies(agents, skills):
    """分析Agent间依赖关系"""
    deps = {}
    for agent in agents:
        agent_deps = []
        # 检查 agent 是否有子Agent或调用其他agent的痕迹
        for root, dirs, files in os.walk(agent["path"]):
            if "memory" in root or ".git" in root:
                dirs.clear()
                continue
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8", errors="replace") as fh:
                            content = fh.read()
                        # 检查是否引用其他Agent
                        for other in agents:
                            if other["name"] != agent["name"] and other["name"] in content:
                                agent_deps.append({
                                    "type": "reference",
                                    "target": other["name"],
                                    "file": os.path.relpath(path, agent["path"]),
                                })
                        # 检查是否使用特定技能
                        for skill in skills:
                            if skill["name"] in content:
                                agent_deps.append({
                                    "type": "skill",
                                    "target": skill["name"],
                                    "file": os.path.relpath(path, agent["path"]),
                                })
                    except Exception:
                        pass
        deps[agent["name"]] = agent_deps
    return deps


def analyze_conflicts(agents):
    """分析Agent间潜在冲突"""
    conflicts = []

    # 检查同名文件冲突
    for i, a1 in enumerate(agents):
        for a2 in agents[i + 1:]:
            if a1["name"] == a2["name"]:
                conflicts.append({
                    "type": "name_collision",
                    "agents": [a1["name"], a2["name"]],
                    "severity": "high",
                    "description": f"发现同名Agent: {a1['name']}",
                })

    # 检查资源竞争（相同目录）
    paths = [a["path"] for a in agents]
    # 检查是否有Agent workspace重叠
    workspace_names = set()
    for agent in agents:
        for root, dirs, files in os.walk(agent["path"]):
            if "memory" in root:
                dirs.clear()
                continue
            break

    if not conflicts:
        conflicts.append({
            "type": "none",
            "severity": "info",
            "description": "未发现Agent间冲突",
        })

    return conflicts


def main():
    parser = argparse.ArgumentParser(description="OpenClaw多Agent协调分析")
    parser.add_argument(
        "--action",
        choices=["dependencies", "topology", "conflicts", "health"],
        default="health",
        help="分析类型",
    )
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    agents = discover_agents()
    skills = discover_skills()

    result = {
        "timestamp": datetime.now().isoformat(),
        "agents_found": len(agents),
        "skills_found": len(skills),
        "agents": [{"name": a["name"], "path": a["path"]} for a in agents],
        "skills": [{"name": s["name"], "source": s["source"]} for s in skills],
    }

    if args.action == "dependencies":
        deps = analyze_dependencies(agents, skills)
        result["dependencies"] = deps
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n🔗 Agent依赖分析")
            print("=" * 45)
            for agent_name, deps_list in deps.items():
                print(f"  {agent_name}:")
                if deps_list:
                    for d in deps_list:
                        print(f"    → [{d['type']}] {d['target']} (via {d['file']})")
                else:
                    print(f"    (无依赖)")

    elif args.action == "topology":
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n🗺️ Agent拓扑")
            print("=" * 45)
            print(f"  已发现Agent: {len(agents)}")
            print(f"  可用技能: {len(skills)}")
            print("")
            for agent in agents:
                status = "✅" if agent["has_soul"] else "❌"
                mem = "🧠" if agent["has_memory"] else "—"
                print(f"  {status} {mem} {agent['name']}")
                if "role_hint" in agent:
                    print(f"     {agent['role_hint']}")
            print("")
            print("  技能分布:")
            user_skills = [s for s in skills if s["source"] == "user"]
            sys_skills = [s for s in skills if s["source"] == "system"]
            print(f"    用户技能: {len(user_skills)}")
            print(f"    系统技能: {len(sys_skills)}")

    elif args.action == "conflicts":
        conflicts = analyze_conflicts(agents)
        result["conflicts"] = conflicts
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n⚡ Agent冲突检测")
            print("=" * 45)
            for c in conflicts:
                sev = {"high": "🔴", "medium": "🟡", "info": "🔵"}.get(c["severity"], "⚪")
                print(f"  {sev} [{c['severity']}] {c['description']}")

    elif args.action == "health":
        health = {}
        for agent in agents:
            health[agent["name"]] = {
                "soul_exists": agent["has_soul"],
                "memory_exists": agent["has_memory"],
            }
        result["health"] = health
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n🏥 多Agent健康总览")
            print("=" * 45)
            for name, h in health.items():
                soul = "✅" if h["soul_exists"] else "❌"
                mem = "✅" if h["memory_exists"] else "❌"
                print(f"  {soul} SOUL.md  {mem} memory/  → {name}")


if __name__ == "__main__":
    main()
