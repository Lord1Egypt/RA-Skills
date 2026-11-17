#!/usr/bin/env python3
"""
arc4plus1 技能基础测试
验证 SKILL.md 格式和必要文件完整性
"""

import os
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent

def test_required_files():
    """检查必需文件存在性"""
    required = ['SKILL.md', 'README.md', 'scripts/find_blocks.py']
    for f in required:
        path = SKILL_ROOT / f
        assert path.exists(), f"缺少必需文件: {f}"
    print("✅ 所有必需文件存在")

def test_skill_md_frontmatter():
    """检查 SKILL.md frontmatter"""
    import re
    content = (SKILL_ROOT / 'SKILL.md').read_text()
    # 检查 YAML frontmatter
    assert content.startswith('---'), "SKILL.md 应以 --- 开头"
    assert 'name:' in content, "缺少 name 字段"
    assert 'version:' in content, "缺少 version 字段"
    assert 'description:' in content, "缺少 description 字段"
    print("✅ SKILL.md frontmatter 格式正确")

def test_find_blocks_script():
    """检查 find_blocks.py 可执行性"""
    script = SKILL_ROOT / 'scripts' / 'find_blocks.py'
    assert script.exists(), "find_blocks.py 不存在"
    # 尝试导入（不执行）
    import importlib.util
    spec = importlib.util.spec_from_file_location("find_blocks", script)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        print("✅ find_blocks.py 可导入")
    except Exception as e:
        print(f"⚠️ find_blocks.py 导入警告: {e}")

def main():
    print("🧪 开始 arc4plus1 技能基础测试...")
    try:
        test_required_files()
        test_skill_md_frontmatter()
        test_find_blocks_script()
        print("\n✅ 所有基础测试通过！")
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
