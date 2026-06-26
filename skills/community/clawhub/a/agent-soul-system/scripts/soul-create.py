#!/usr/bin/env python3
"""Create a new agent with SOUL.md template."""
import os, sys

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")
TEMPLATE = """# SOUL - {name}

## 人格
[选择一个人物] — [核心理念]
参考: ~/.openclaw/workspace/skills/agent-soul-system/references/personality-library.md

## 核心特质
- 从导师继承的特质1
- 从导师继承的特质2

## 说话风格
- 典型口头禅/句式

## 核心职责
1. 职责1
2. 职责2

## 核心原则
1. 原则1
2. 原则2

## 与上级的协作协议
- 直接上级：小咪
- 日常汇报：完成后/每小时/实时
- 升级触发：[什么情况下需要上报]
- 决策权限：[可以自主决定的范围]

## 输出标准
- 产出格式要求
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: soul-create.py <agent-name>")
        print("示例: soul-create.py my-new-agent")
        sys.exit(1)

    name = sys.argv[1]
    path = os.path.join(AGENTS_DIR, name)
    soul = os.path.join(path, "SOUL.md")

    if os.path.exists(soul):
        print(f"⚠️ {name} 已有 SOUL.md，要覆盖吗？(y/n)")
        if input().lower() != 'y':
            sys.exit(0)

    os.makedirs(path, exist_ok=True)
    with open(soul, 'w') as f:
        f.write(TEMPLATE.format(name=name))

    print(f"✅ {name}/SOUL.md 已创建")
    print(f"   路径: {soul}")
    print(f"   下一步: 编辑 {soul}，选择人格，填写职责和原则")
    print(f"   参考: references/personality-library.md")
