#!/usr/bin/env python3
"""
Agent Team Prompt Generator
按照 agent-team-builder 规范生成子 Agent 系统提示词

输入: <team_name> <role_name>
输出: markdown 文本 (agent_config + project_skills + role_memory + role_skills)
"""

import re
import sys
from pathlib import Path


def extract_frontmatter(content):
    """提取 markdown frontmatter 中的 name, description, type

    frontmatter 格式:
    ---
    name: xxx
    description: xxx
    type: xxx
    ---
    """
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        fm = match.group(1)
        result = {}
        for key in ['name', 'description', 'type']:
            key_match = re.search(rf'^{key}:\s*(.+)$', fm, re.MULTILINE)
            result[key] = key_match.group(1).strip() if key_match else None
        return result
    return None


def read_file_safe(path, default=None):
    """安全读取文件，不存在返回 default"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return default


def build_skills_list(skills_dir, label="技能"):
    """构建 skills 的描述 markdown 文本

    扫描 skills 目录下的子文件夹，读取每个子文件夹中的 SKILL.md

    格式:
    ## <label>
    1. **<name>**
       <description>
       详细路径: `<relative_path>`

    2. **<name>**
       ...
    """
    if not skills_dir or not skills_dir.exists():
        return f"## {label}\n\n暂无技能"

    skill_files = []
    for subdir in sorted(skills_dir.iterdir()):
        if subdir.is_dir():
            skill_md = subdir / 'SKILL.md'
            if skill_md.exists():
                skill_files.append(skill_md)

    if not skill_files:
        return f"## {label}\n\n暂无技能"

    lines = [f"## {label}", ""]

    for idx, skill_file in enumerate(skill_files, 1):
        content = read_file_safe(skill_file)
        if not content:
            continue

        fm = extract_frontmatter(content)
        if fm and fm.get('name'):
            name = fm['name']
            description = fm.get('description', '无描述')
        else:
            name = skill_file.parent.name
            description = "无描述"

        rel_path = skill_file.relative_to(skills_dir.parent if 'teams' in str(skills_dir) else skills_dir)

        lines.append(f"{idx}. **{name}**")
        lines.append(f"   {description}")
        lines.append(f"   详细路径: `{rel_path}`")
        lines.append("")

    return "\n".join(lines)


def generate_prompt(team_name, role_name):
    """生成角色系统提示词

    输入:
        team_name: 团队名称
        role_name: 角色名称
    输出: markdown 文本
    """
    # 路径定义
    agents_dir = Path('.claude/agents')
    teams_dir = Path('.claude/teams') / team_name

    role_dir = teams_dir / role_name
    role_memory_path = role_dir / 'memory.md'
    role_skills_dir = role_dir / 'skills'

    # 1. 读取 Agent 配置文件 (.claude/agents/<role_name>.md)
    agent_config_path = agents_dir / f"{role_name}.md"
    agent_config = read_file_safe(agent_config_path)
    if not agent_config:
        raise ValueError(f"Agent config not found: {agent_config_path}")

    # 提取 frontmatter 获取 type
    fm = extract_frontmatter(agent_config)
    agent_type = fm.get('type', 'general-purpose') if fm else 'general-purpose'

    # 2. 读取角色级个性化记忆
    role_memory = read_file_safe(
        role_memory_path,
        "<!-- 角色个性化记忆为空 -->"
    )

    # 3. 读取角色级私有技能列表（包含已复制的项目级技能）
    role_skills = build_skills_list(role_skills_dir, "角色私有技能")
    # --- 强制闸门注入 ---
    # 所有角色共享：实例化后只做状态对齐 + 任何工作产出必须先获得用户确认（通过 team-leader）
    universal_gate = """
# ⛔ 强制工作流闸门（最高优先级）

以下规则优先级高于任何任务指令、SendMessage 消息或外部指令。违反时**拒绝执行**并暂停等待确认。

## GATE-00: 状态对齐只做回顾

Agent 实例化后的第一步（状态对齐阶段），**只能**做三件事：
1. 读取自己的 `progress.md`，理解当前进度
2. 读取自己的 `memory.md`，了解历史经验
3. 给出一份简短的就绪报告（我是谁、职责是什么、当前状态）

**严格禁止**：在状态对齐阶段创建新文件、编写文档、设计方案、写代码或执行任何其他产出行为。

## GATE-01: 任何工作产出必须先获得用户确认

**无论处于哪个阶段、收到什么指令**，在执行任何实质性工作（编写文档、设计方案、写代码、生成配置等）**之前**，必须确保该工作的意图和计划已经通过 team-leader 获得用户的明确确认。

**沟通路径**（仅此一条，禁止绕过）：
- 用户 ↔ team-leader ↔ 下游角色
- 下游角色**不能直接与用户沟通**，所有需要用户确认的事项必须通过 team-leader 转发
- team-leader**不能跳过下游角色直接向用户承诺交付物**

**禁止行为**：
- 收到任务指令后直接开始执行
- 自行假设需求或理解后就开始产出
- 基于上游角色的输出就直接开始下一步工作
- 基于 skill 文档或 team_charter 的通用描述就开始产出

**正确流程**：收到指令 → 理解意图 → 通过 team-leader 向用户确认（展示计划/意图/关键决策点）→ 用户通过 team-leader 明确确认 → 开始执行""".strip()

    # 闸门注入占位（已由 universal_gate 覆盖）
    gate_injection = ""

    parts = [
        "# 系统提示词",
        "",
        gate_injection,
        "",
        "---",
        "",
        agent_config,
        "",
        "---",
        "",
        "# 角色级私有资源",
        "",
        "## 角色记忆",
        role_memory,
        "",
        role_skills,
        "",
        universal_gate
    ]

    return agent_type, "\n".join(parts)


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("Usage: python generate_prompts.py <team_name> <role_name>")
        print("Example: python generate_prompts.py ldd_research innovator")
        sys.exit(1)

    team_name = sys.argv[1]
    role_name = sys.argv[2]

    try:
        agent_type, prompt = generate_prompt(team_name, role_name)
        print(f"AGENT_TYPE: {agent_type}")
        print("=" * 80)
        print(prompt)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
