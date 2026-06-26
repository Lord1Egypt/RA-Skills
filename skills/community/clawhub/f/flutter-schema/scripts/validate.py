#!/usr/bin/env python3
"""
GetX Page Generator - 自动生成 Flutter GetX 页面文件结构

Usage:
    python validate.py <page_name> [target_directory]

说明：
- page_name 仅允许小写字母、数字和下划线（snake_case）
- target_directory（如果提供）必须位于项目 lib 目录下
"""

import os
import re
import sys
from datetime import datetime


def _find_project_root(start_dir: str) -> str:
    """向上查找包含 pubspec.yaml 的目录，用于定位项目根目录。"""
    current = os.path.abspath(start_dir)
    for _ in range(8):  # 限制最大向上层级，避免死循环
        pubspec = os.path.join(current, "pubspec.yaml")
        if os.path.exists(pubspec):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.abspath(start_dir)


def get_package_name() -> str:
    """从 pubspec.yaml 读取包名，找不到时回退为通用名称。"""
    project_root = _find_project_root(os.path.dirname(__file__))
    pubspec_path = os.path.join(project_root, "pubspec.yaml")
    if os.path.exists(pubspec_path):
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            match = re.search(r'^name:\s*["\']?([\w_]+)["\']?', f.read(), re.MULTILINE)
            if match:
                return match.group(1)
    return 'app'  # 默认回退


def to_pascal_case(snake_str: str) -> str:
    """将 snake_case 转换为 PascalCase"""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


def _validate_page_name(name: str) -> str:
    """校验并规范化页面名称，防止注入和路径穿越。"""
    normalized = name.strip().lower().replace('-', '_')
    if not re.fullmatch(r'[a-z0-9_]+', normalized):
        raise ValueError(
            f"非法的页面名称: {name!r}，仅支持小写字母、数字和下划线（snake_case）。"
        )
    return normalized


def generate_binding(name: str, pascal_name: str, package_path: str) -> str:
    """生成 binding 文件内容"""
    pkg = get_package_name()
    return f"""import 'package:get/get.dart';
import 'package:{pkg}/{package_path}/{name}_logic.dart';

class {pascal_name}Binding extends Bindings {{
  @override
  void dependencies() {{
    Get.lazyPut<{pascal_name}Logic>(() => {pascal_name}Logic());
  }}
}}
"""


def generate_state(pascal_name: str) -> str:
    """生成 state 文件内容"""
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""/// @description:
/// @author 
/// @date: {date_str}
class {pascal_name}State {{
  {pascal_name}State() {{
    ///Initialize variables
  }}
}}
"""


def generate_logic(name: str, pascal_name: str) -> str:
    """生成 logic 文件内容"""
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""import 'package:get/get.dart';

import '{name}_state.dart';

/// @description:
/// @author 
/// @date: {date_str}
class {pascal_name}Logic extends GetxController {{
  final state = {pascal_name}State();
}}
"""


def generate_view(name: str, pascal_name: str) -> str:
    """生成 view 文件内容"""
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '{name}_logic.dart';
import '{name}_state.dart';

/// @description:
/// @author
/// @date: {date_str}
class {pascal_name}Page extends StatelessWidget {{
  final {pascal_name}Logic logic = Get.find<{pascal_name}Logic>();
  final {pascal_name}State state = Get.find<{pascal_name}Logic>().state;

  {pascal_name}Page({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold();
  }}
}}
"""


def create_getx_page(name: str, target_dir: str | None = None):
    """
    创建 GetX 页面文件结构（带输入校验，防止路径穿越）

    Args:
        name: 页面名称 (snake_case, 如 user_profile)
        target_dir: 目标目录，相对于项目根目录或绝对路径；
                    最终必须位于项目 lib 目录下
    """
    # 规范化并校验页面名称
    name = _validate_page_name(name)
    pascal_name = to_pascal_case(name)

    # 解析项目根目录和 lib 根目录
    project_root = _find_project_root(os.path.dirname(__file__))
    lib_root = os.path.join(project_root, "lib")

    # 计算目标目录的绝对路径，并限制在 lib 目录内
    if target_dir is None:
        abs_target_dir = os.path.join(lib_root, "modules", name)
    else:
        # 允许绝对路径或相对项目根目录的路径
        if os.path.isabs(target_dir):
            abs_target_dir = os.path.normpath(target_dir)
        else:
            abs_target_dir = os.path.normpath(
                os.path.join(project_root, target_dir)
            )

    # 防止路径穿越：强制要求在 lib 目录下
    common_prefix = os.path.commonpath([lib_root, abs_target_dir])
    if common_prefix != os.path.abspath(lib_root):
        raise ValueError(
            f"目标目录不安全或超出 lib 目录范围: {target_dir!r} "
            f"(解析为: {abs_target_dir})"
        )

    page_dir = os.path.join(abs_target_dir, name)

    # 计算用于 package import 的相对路径（相对于 lib 根目录）
    package_path = os.path.relpath(page_dir, lib_root).replace(os.sep, "/")

    os.makedirs(page_dir, exist_ok=True)

    files = {
        f"{name}_binding.dart": generate_binding(name, pascal_name, package_path),
        f"{name}_state.dart": generate_state(pascal_name),
        f"{name}_logic.dart": generate_logic(name, pascal_name),
        f"{name}_view.dart": generate_view(name, pascal_name),
    }

    created_files = []
    for filename, content in files.items():
        file_path = os.path.join(page_dir, filename)
        if os.path.exists(file_path):
            print(f"⚠️  文件已存在，跳过: {file_path}")
            continue
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(file_path)
        print(f"✅ 创建文件: {file_path}")

    if created_files:
        print(f"\n🎉 成功创建 {len(created_files)} 个文件在 {page_dir}/")
    else:
        print(f"\n⚠️  没有创建任何文件（可能都已存在）")

    return created_files


def print_usage():
    """打印使用说明"""
    print("GetX Page Generator - 自动生成 Flutter GetX 页面文件结构")
    print("\nUsage: python validate.py <page_name> [target_directory]")
    print("\nExamples:")
    print("  python validate.py user_profile")
    print("  python validate.py user_profile lib/modules/user")
    print("\nThis will create:")
    print("  - {name}_binding.dart")
    print("  - {name}_state.dart")
    print("  - {name}_logic.dart")
    print("  - {name}_view.dart")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0 if len(sys.argv) > 1 else 1)

    name = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        create_getx_page(name, target_dir)
    except ValueError as e:
        # 输入非法时给出明确提示并返回非 0 状态码，方便上层工具处理
        print(f"❌ 参数错误: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
