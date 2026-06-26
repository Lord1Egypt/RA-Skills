#!/usr/bin/env python3
"""
ClawHub技能打包与上传工具
用于准备技能包并生成上传说明

用法:
    python clawhub_packer.py <技能目录> [--output <输出目录>]

示例:
    python clawhub_packer.py ../chinese-content-humanizer
    python clawhub_packer.py ../botstreet-task-agent --output ./ready-to-upload
"""

import os
import sys
import json
import shutil
import zipfile
import re
from pathlib import Path
from datetime import datetime

# ANSI 颜色代码
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️ {msg}{RESET}")

def print_header(msg):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{msg}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

def validate_skill_name(name):
    """验证技能名称是否合法"""
    # 只能是字母、数字、短横线
    if not re.match(r'^[a-z0-9\-]+$', name):
        return False, "名称只能包含小写字母、数字和短横线"
    # 不能以短横线开头或结尾
    if name.startswith('-') or name.endswith('-'):
        return False, "名称不能以短横线开头或结尾"
    # 长度检查
    if len(name) < 3:
        return False, "名称长度至少3个字符"
    if len(name) > 50:
        return False, "名称长度最多50个字符"
    return True, "名称合法"

def check_skill_md(skill_dir):
    """检查SKILL.md文件"""
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return False, "SKILL.md 文件不存在"
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 检查是否有frontmatter
    if not content.startswith('---'):
        return False, "SKILL.md 缺少 YAML frontmatter"
    
    # 提取frontmatter
    lines = content.split('\n')
    frontmatter_lines = []
    in_frontmatter = False
    
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            frontmatter_lines.append(line)
    
    frontmatter = '\n'.join(frontmatter_lines)
    
    # 检查name字段
    if 'name:' not in frontmatter:
        return False, "frontmatter 缺少 name 字段"
    
    # 检查description字段
    if 'description:' not in frontmatter:
        return False, "frontmatter 缺少 description 字段"
    
    return True, "SKILL.md 格式正确"

def check_files(skill_dir):
    """检查文件是否符合要求"""
    forbidden_files = ['.git', '.DS_Store', 'Thumbs.db', 'LICENSE', 'COPYING']
    forbidden_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.exe', '.dll', '.so']
    
    issues = []
    
    for root, dirs, files in os.walk(skill_dir):
        # 检查目录名
        for d in dirs:
            if d in forbidden_files or d.startswith('.'):
                issues.append(f"禁止的目录: {d}")
        
        # 检查文件名
        for f in files:
            if f in forbidden_files or f.startswith('.'):
                issues.append(f"禁止的文件: {f}")
            ext = Path(f).suffix.lower()
            if ext in forbidden_extensions:
                issues.append(f"禁止的文件类型: {f}")
    
    if issues:
        return False, '\n'.join(issues)
    return True, "文件检查通过"

def extract_skill_info(skill_dir):
    """提取技能信息"""
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding='utf-8')
    
    # 提取frontmatter
    lines = content.split('\n')
    frontmatter_lines = []
    in_frontmatter = False
    
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            frontmatter_lines.append(line)
    
    frontmatter = '\n'.join(frontmatter_lines)
    
    # 提取name和description
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    
    info = {
        'name': name_match.group(1).strip() if name_match else 'unknown',
        'description': desc_match.group(1).strip() if desc_match else 'unknown',
        'slug': name_match.group(1).strip().lower().replace(' ', '-') if name_match else 'unknown'
    }
    
    return info

def pack_skill(skill_dir, output_dir=None):
    """打包技能"""
    skill_name = skill_dir.name
    
    print_header(f"打包技能: {skill_name}")
    
    # 检查目录是否存在
    if not skill_dir.exists():
        print_error(f"技能目录不存在: {skill_dir}")
        return False
    
    # 检查SKILL.md
    print_info("检查 SKILL.md...")
    valid, msg = check_skill_md(skill_dir)
    if not valid:
        print_error(f"SKILL.md 检查失败: {msg}")
        return False
    print_success(msg)
    
    # 检查文件
    print_info("检查文件...")
    valid, msg = check_files(skill_dir)
    if not valid:
        print_error(f"文件检查失败:\n{msg}")
        return False
    print_success(msg)
    
    # 提取技能信息
    info = extract_skill_info(skill_dir)
    print_info(f"技能名称: {info['name']}")
    print_info(f"技能Slug: {info['slug']}")
    print_info(f"技能描述: {info['description']}")
    
    # 确定输出目录
    if output_dir is None:
        output_dir = Path("clawhub-ready")
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制技能到输出目录
    dest_dir = output_dir / skill_name
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    
    print_info(f"复制技能到 {output_dir}...")
    shutil.copytree(skill_dir, dest_dir)
    
    # 创建ZIP包
    zip_name = f"{skill_name}.zip"
    zip_path = output_dir / zip_name
    
    print_info(f"创建ZIP包: {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dest_dir)
                zipf.write(file_path, arcname)
    
    print_success(f"技能包已准备完成!")
    print_info(f"输出目录: {output_dir}")
    print_info(f"ZIP文件: {zip_path}")
    
    # 生成上传说明
    generate_upload_guide(skill_name, info, output_dir)
    
    return True

def generate_upload_guide(skill_name, info, output_dir):
    """生成上传指南"""
    guide = f"""# ClawHub 上传指南

## 技能信息
- **技能名称**: {info['name']}
- **Slug**: {info['slug']}
- **描述**: {info['description']}

## 上传步骤

### 1. 登录 ClawHub
1. 访问 https://clawhub.ai/import
2. 点击 "Sign in with GitHub"
3. 使用你的 GitHub 账号登录

### 2. 填写技能信息
| 字段 | 值 |
|------|-----|
| Slug | `{info['slug']}` |
| Display name | `{info['name']}` |
| Version | `1.0.0` |
| Tags | `latest` |

### 3. 上传文件
- 拖拽 `skills/{skill_name}/` 文件夹到上传区域
- 或直接使用已打包的 `{skill_name}.zip`

### 4. 等待验证
确保以下检查通过:
- ✅ Slug 格式正确
- ✅ Display name 已填写
- ✅ MIT-0 协议已勾选
- ✅ SKILL.md 已检测到

### 5. 填写 Changelog
```
v1.0.0 初始版本
- 发布 {info['name']}
- 功能: {info['description']}
```

### 6. 发布
点击 "Publish skill" 完成发布!

## 验证发布成功
- 访问 https://clawhub.ai/{info['slug']}
- 或在 ClawHub 搜索框搜索技能名称
"""
    
    guide_path = output_dir / f"{skill_name}_上传指南.md"
    guide_path.write_text(guide, encoding='utf-8')
    print_success(f"上传指南已生成: {guide_path}")

def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <技能目录> [--output <输出目录>]")
        print(f"示例: {sys.argv[0]} ../chinese-content-humanizer")
        sys.exit(1)
    
    skill_dir = Path(sys.argv[1])
    output_dir = None
    
    # 解析参数
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
    
    success = pack_skill(skill_dir, output_dir)
    
    if success:
        print_success("打包完成!")
        sys.exit(0)
    else:
        print_error("打包失败!")
        sys.exit(1)

if __name__ == '__main__':
    main()
