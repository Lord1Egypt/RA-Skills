"""
SKILL.md 模板生成器 —— 为生成的项目创建标准 AI 技能元数据头
"""


def generate_skill_md(project_name: str, description: str) -> str:
    return f"""---
name: {project_name}
description: "{description}"
allowed-tools:
  - read
  - write
  - edit
  - exec
---

# {project_name}

{description}

## 使用方法

直接运行 `python src/main.py` 或 `bash run.sh`。

## 项目结构

见 ASSET_MANIFEST.md 获取完整资源地图。
"""
