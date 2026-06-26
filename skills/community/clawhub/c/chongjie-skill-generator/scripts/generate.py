#!/usr/bin/env python3
"""
Skill生成器 - MVP版本
将自然语言需求转换为Skill结构
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Skill模板
SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

{body}

## 使用方式

{usage}
"""

def generate_skill_json(user_input: str) -> dict:
    """生成Skill结构的JSON"""
    
    # 构建LLM prompt
    prompt = f"""你是一个专业的AI Agent Skill架构师。

用户需求: {user_input}

请根据需求生成Skill结构，输出JSON格式:

```json
{{
  "name": "技能名称(英文kebab-case)",
  "description": "功能描述(说明做什么和何时使用，包含使用场景)",
  "triggers": ["触发关键词列表(中英文)"],
  "body": "Markdown格式的详细使用说明"
}}
```

要求:
- name使用kebab-case(如: ppt-generator)
- description要包含"使用场景"说明
- triggers包含常见触发词
- body使用Markdown格式，包含##功能、##使用方式等章节

只输出JSON，不要其他内容。"""

    return {
        "name": "placeholder",
        "description": "placeholder", 
        "triggers": [],
        "body": "placeholder",
        "_prompt": prompt
    }

def parse_llm_response(text: str) -> dict:
    """解析LLM响应，生成Skill结构"""
    
    # 尝试解析JSON
    try:
        # 提取JSON部分
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "name": data.get("name", "untitled-skill"),
                "description": data.get("description", ""),
                "triggers": data.get("triggers", []),
                "body": data.get("body", "")
            }
    except (json.JSONDecodeError, AttributeError):
        pass
    
    # 备用解析：从文本提取
    return parse_text_format(text)

def parse_text_format(text: str) -> dict:
    """从文本格式解析Skill信息"""
    
    # 提取name
    name_match = re.search(r'name[:：]\s*([a-z0-9-]+)', text, re.IGNORECASE)
    name = name_match.group(1) if name_match else "untitled-skill"
    
    # 提取description
    desc_match = re.search(r'description[:：]\s*(.+?)(?:\n\n|\n[^#]|$)', text, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else ""
    
    # 提取triggers
    triggers = []
    triggers_match = re.search(r'triggers?[:：]\s*\[(.+?)\]', text, re.IGNORECASE)
    if triggers_match:
        triggers = [t.strip().strip('"\'') for t in triggers_match.group(1).split(',')]
    
    # 提取body (到下一个---之前)
    body_match = re.search(r'---[\s\S]+?---\s*\n(.+?)(?=\n---|\Z)', text, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    
    return {
        "name": name,
        "description": description,
        "triggers": triggers,
        "body": body
    }

def format_skill(skill: dict) -> str:
    """格式化Skill为Markdown"""
    
    name = skill.get("name", "untitled-skill")
    description = skill.get("description", "")
    title = name.replace("-", " ").title()
    body = skill.get("body", "")
    triggers = skill.get("triggers", [])
    
    # 生成usage部分
    if triggers:
        usage = "\n".join([f"- \"{t}\"" for t in triggers])
    else:
        usage = "- 直接说出你的需求"
    
    # 如果body为空，生成默认内容
    if not body:
        body = f"""## 功能

- 根据用户需求自动生成内容
- 支持多种场景和用途

## 触发方式

使用以下关键词触发: {', '.join(triggers) if triggers else '直接描述需求'}"""
    
    return SKILL_TEMPLATE.format(
        name=name,
        description=description,
        title=title,
        body=body,
        usage=usage
    )

def save_skill(skill: dict, output_dir: Path) -> Path:
    """保存Skill到文件"""
    
    skill_name = skill.get("name", "untitled-skill")
    skill_dir = output_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入SKILL.md
    skill_file = skill_dir / "SKILL.md"
    content = format_skill(skill)
    skill_file.write_text(content, encoding="utf-8")
    
    # 写入_meta.json
    meta_file = skill_dir / "_meta.json"
    meta = {
        "generated": True,
        "generatedAt": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    return skill_dir

def generate_from_input(user_input: str, output_dir: Path = None) -> dict:
    """主生成函数"""
    
    if output_dir is None:
        output_dir = Path.home() / ".openclaw/workspace/skills"
    
    # 解析需求 (这里返回prompt，实际由LLM调用)
    skill_info = generate_skill_json(user_input)
    
    # 返回结构供LLM调用
    return skill_info

def demo():
    """演示生成过程"""
    
    test_inputs = [
        "我需要一个查天气的skill",
        "创建一个帮我写Python代码注释的skill",
        "做一个管理Apple提醒事项的skill"
    ]
    
    print("=" * 60)
    print("Skill生成器演示")
    print("=" * 60)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n【示例 {i}】")
        print(f"输入: {test_input}")
        
        # 生成结构
        skill = generate_skill_json(test_input)
        
        print(f"\n生成的JSON结构:")
        print(json.dumps({
            "name": "weather-query",  # 模拟LLM返回
            "description": "查询天气和预报。使用场景：(1)了解当前天气 (2)查看未来预报",
            "triggers": ["查天气", "天气怎么样", "weather"],
            "body": "## 功能\n- 查询当前天气\n- 查看预报"
        }, indent=2, ensure_ascii=False))
        
        print("\n生成的SKILL.md:")
        demo_skill = {
            "name": "weather-query",
            "description": "查询天气和预报。使用场景：(1)了解当前天气 (2)查看未来预报",
            "triggers": ["查天气", "天气怎么样", "weather"],
            "body": "## 功能\n- 查询当前天气\n- 查看3-7天预报\n\n## 使用方式\n直接告诉SC想查询的城市"
        }
        print(format_skill(demo_skill))
        
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        user_input = " ".join(sys.argv[1:])
        print(f"输入: {user_input}")
        skill = generate_skill_json(user_input)
        
        # 显示prompt供LLM调用
        print("\n=== LLM Prompt ===")
        print(skill["_prompt"])
    else:
        # 演示模式
        demo()
