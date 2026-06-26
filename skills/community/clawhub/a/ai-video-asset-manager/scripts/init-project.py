"""
初始化新AI视频项目目录结构
用法: python init-project.py "C:\\path\\to\\project" "项目名"
"""
import os
import sys
import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "assets" / "templates"

SUBDIRS = [
    "01_资产库/角色",
    "01_资产库/场景",
    "01_资产库/道具",
    "02_分镜",
    "03_参考图索引/CHAR_001",
    "03_参考图索引/SCENE_001",
    "03_参考图索引/TPL_001",
    "03_参考图索引/SHOT_001",
    "04_生成记录",
    "05_一致性检查",
    "06_返工记录",
]

TEMPLATE_FILES = {
    "00_总览.md": "00_总览.md",
    "01_资产库/角色/00_角色资产卡_模板.md": "01_资产库/角色/00_角色资产卡_模板.md",
    "01_资产库/场景/00_场景资产卡_模板.md": "01_资产库/场景/00_场景资产卡_模板.md",
    "01_资产库/道具/00_道具资产卡_模板.md": "01_资产库/道具/00_道具资产卡_模板.md",
    "02_分镜/00_分镜表_模板.md": "02_分镜/00_分镜表_模板.md",
    "02_分镜/00_镜头卡_模板.md": "02_分镜/00_镜头卡_模板.md",
    "03_参考图索引/00_参考图索引_模板.md": "03_参考图索引/00_参考图索引_模板.md",
    "04_生成记录/00_生成记录_模板.md": "04_生成记录/00_生成记录_模板.md",
    "05_一致性检查/00_一致性检查表_模板.md": "05_一致性检查/00_一致性检查表_模板.md",
    "06_返工记录/00_返工记录_模板.md": "06_返工记录/00_返工记录_模板.md",
}

OVERVIEW_CONTENT = '''# {project_name} — AI视频制作工作流

> 基于 ViMax 多智能体视频生成框架

---

## 项目状态

| 维度 | 状态 |
|------|------|
| 角色资产 | 🔄 初始化中 |
| 场景资产 | 🔄 初始化中 |
| 叙事序列 | — |
| 口播模板 | — |

---

## 资产目录

{directory_tree}

---

## 核心原则

1. **资产优先** — 角色/场景/道具未锁定前不开始生成
2. **版本不覆盖** — 每次生成和返工均另存新版本
3. **检查前置** — 一致性检查是进入下一镜头的门槛

---

## 状态流转

```
草稿 → 审核中 → 已锁定 → 使用中 → 已废弃
  ↑                      ↓
  ← ← ← ← ← ← ← 返工 ← ←
```

---

## 下一步

1. 填写角色资产卡
2. 填写场景资产卡
3. 锁定资产
4. 新建第一个镜头
'''

def create_directory_tree(base_path):
    """生成目录树字符串"""
    lines = []
    for subdir in SUBDIRS:
        full_path = Path(base_path) / subdir
        full_path.mkdir(parents=True, exist_ok=True)
        depth = subdir.count('/')
        prefix = "├── " if depth > 0 else ""
        lines.append(f"{prefix}{Path(subdir).name}/")
    return '\n'.join(lines)

def init_project(project_path: str, project_name: str):
    base = Path(project_path)
    
    # 创建目录
    for subdir in SUBDIRS:
        (base / subdir).mkdir(parents=True, exist_ok=True)
    
    # 生成总览
    tree = create_directory_tree(base)
    overview = OVERVIEW_CONTENT.format(
        project_name=project_name,
        directory_tree=tree
    )
    (base / "00_总览.md").write_text(overview, encoding='utf-8')
    
    # 复制模板文件
    for src_name, dst_name in TEMPLATE_FILES.items():
        dst_path = base / dst_name
        if not dst_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            # 创建空模板占位
            dst_path.write_text(f"# {dst_name} — 待填充\n", encoding='utf-8')
    
    print(f"[OK] 项目初始化完成: {base}")
    print(f"[OK] 项目名: {project_name}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python init-project.py \"项目路径\" \"项目名\"")
        sys.exit(1)
    
    init_project(sys.argv[1], sys.argv[2])
