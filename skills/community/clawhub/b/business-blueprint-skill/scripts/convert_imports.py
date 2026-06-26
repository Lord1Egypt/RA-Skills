"""
批量修改相对导入为绝对导入

将scripts/business_blueprint/*.py中的相对导入改为绝对导入
"""

import re
from pathlib import Path


def convert_relative_import(file_path: Path):
    """转换相对导入为绝对导入"""
    content = file_path.read_text()

    # 替换 from .xxx import 为 from xxx import
    pattern = r'from \.(\w+) import'
    replacement = r'from \1 import'
    new_content = re.sub(pattern, replacement, content)

    # 替换 from .xxx.yyy import 为 from xxx.yyy import
    pattern2 = r'from \.(\w+)\.(\w+) import'
    replacement2 = r'from \1.\2 import'
    new_content = re.sub(pattern2, replacement2, new_content)

    if new_content != content:
        file_path.write_text(new_content)
        return True

    return False


def batch_convert(directory: str):
    """批量转换目录下的所有Python文件"""
    dir_path = Path(directory)
    converted_count = 0

    for py_file in dir_path.glob("**/*.py"):
        # 跳过测试文件和迁移器（它们有自己的导入逻辑）
        if "tests" in str(py_file) or "migrations" in str(py_file):
            continue

        try:
            if convert_relative_import(py_file):
                print(f"✓ Converted: {py_file.name}")
                converted_count += 1
            else:
                print(f"  No change: {py_file.name}")
        except Exception as e:
            print(f"✗ Error: {py_file.name} - {str(e)}")

    print(f"\n转换完成: {converted_count} 个文件")


if __name__ == "__main__":
    batch_convert("scripts/business_blueprint")