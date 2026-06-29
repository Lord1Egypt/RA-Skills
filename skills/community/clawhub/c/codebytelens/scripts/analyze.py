#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Code Intel - 代码分析工具箱
原创实现，受 Claude Code LSPTool 设计模式启发。
使用开源工具：ast (Python标准库)、pyright、ripgrep
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import ast
import os
import subprocess
from pathlib import Path
from collections import defaultdict


def extract_symbols(source_path):
    """提取 Python 文件中的符号定义"""
    path = Path(source_path)
    if not path.exists() or path.suffix != '.py':
        print(f"❌ 仅支持 Python 文件 (.py)")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(path))
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return

    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            base_names = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    base_names.append(base.id)
                elif isinstance(base, ast.Attribute):
                    base_names.append(f"{base.value.id}.{base.attr}" if isinstance(base.value, ast.Name) else base.attr)
            classes.append({
                'name': node.name,
                'line': node.lineno,
                'bases': base_names or None,
                'methods': methods,
                'docstring': ast.get_docstring(node, clean=True),
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 只取顶层函数，不包括类方法
            is_method = False
            for parent_node in ast.walk(tree):
                if isinstance(parent_node, ast.ClassDef) and node in parent_node.body:
                    is_method = True
                    break
            if not is_method:
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'async': isinstance(node, ast.AsyncFunctionDef),
                    'docstring': ast.get_docstring(node, clean=True),
                })
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({'module': alias.name, 'alias': alias.asname, 'line': node.lineno})
            else:
                module = node.module or ''
                for alias in node.names:
                    imports.append({'module': f"{module}.{alias.name}", 'alias': alias.asname, 'line': node.lineno})

    print(f"\n{'='*60}")
    print(f"📊 文件分析: {path.name}")
    print(f"{'='*60}")

    # 导入
    if imports:
        print(f"\n📦 导入 ({len(imports)}):")
        for imp in imports[:20]:
            print(f"  📥 第{imp['line']}行  {imp['module']}"
                  + (f" as {imp['alias']}" if imp['alias'] else ''))

    # 类
    if classes:
        print(f"\n🏛️  类 ({len(classes)}):")
        for cls in classes:
            bases = f"({', '.join(cls['bases'])})" if cls['bases'] else ''
            print(f"  📋 第{cls['line']}行  class {cls['name']}{bases}")
            for m in cls['methods'][:10]:
                print(f"       └─ def {m}()")
            if len(cls['methods']) > 10:
                print(f"       └─ ... 还有{len(cls['methods'])-10}个方法")
            if cls['docstring']:
                print(f"       📝 {cls['docstring'][:60]}")

    # 函数
    if functions:
        print(f"\n🔧 函数 ({len(functions)}):")
        for func in functions:
            prefix = 'async ' if func['async'] else ''
            print(f"  🛠️  第{func['line']}行  {prefix}def {func['name']}()")
            if func['docstring']:
                print(f"       📝 {func['docstring'][:60]}")

    return {'classes': classes, 'functions': functions, 'imports': imports}


def search_definition(name, search_path):
    """搜索函数/类定义位置"""
    path = Path(search_path)
    if not path.exists():
        print(f"❌ 路径不存在: {search_path}")
        return

    # 使用 ripgrep 搜索类和函数定义
    patterns = [
        rf"class\s+{re.escape(name)}[\s\(:]",
        rf"def\s+{re.escape(name)}\s*\(",
        rf"async\s+def\s+{re.escape(name)}\s*\(",
        rf"{re.escape(name)}\s*=\s*(?:lambda|class|def)",
    ]

    print(f"\n🔍 搜索定义: {name}")
    print(f"{'='*50}")

    for pattern in patterns:
        try:
            result = subprocess.run(
                ['rg', '-n', '--color=always', pattern, str(path)],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout.strip():
                print(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # ripgrep 不可用时用 Python 遍历
    print("\n💡 提示: 安装 ripgrep 获得更快搜索: winget install BurntSushi.ripgrep.MSVC")


def analyze_complexity(source_path):
    """分析代码复杂度"""
    path = Path(source_path)
    if not path.exists() or path.suffix != '.py':
        print(f"❌ 仅支持 Python 文件 (.py)")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content, filename=str(path))
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return

    lines = content.split('\n')
    total_lines = len(lines)
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    blank_lines = sum(1 for l in lines if not l.strip())

    # 统计复杂度
    func_count = 0
    class_count = 0
    branching = 0
    loops = 0
    try_except = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_count += 1
        elif isinstance(node, ast.ClassDef):
            class_count += 1
        elif isinstance(node, (ast.If, ast.IfExp)):
            branching += 1
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            loops += 1
        elif isinstance(node, (ast.Try, ast.TryStar)):
            try_except += 1

    # 圈复杂度 (粗略)
    cyclomatic = branching + loops + 1

    print(f"\n📊 代码复杂度报告: {path.name}")
    print(f"{'='*60}")
    print(f"  📄 总行数:    {total_lines}")
    print(f"  ✅ 代码行:    {code_lines}")
    print(f"  💬 注释行:    {comment_lines}")
    print(f"  ⬜ 空行:      {blank_lines}")
    print(f"  ──────────────────────────")
    print(f"  🏛️  类:       {class_count}")
    print(f"  🔧 函数:      {func_count}")
    print(f"  🔀 分支:      {branching}")
    print(f"  🔄 循环:      {loops}")
    print(f"  ⚠️  异常处理:  {try_except}")
    print(f"  ──────────────────────────")

    qual = ("低" if cyclomatic <= 10
            else "中" if cyclomatic <= 20
            else "高" if cyclomatic <= 40
            else "极高")
    print(f"  🔢 圈复杂度:   {cyclomatic} ({qual})")
    print(f"{'='*60}")


def main():
    if len(sys.argv) < 3:
        print("用法: python analyze.py <symbols|define|complexity|calls> <path> [search_name]")
        print("\n命令:")
        print("  symbols <file.py>       — 提取符号定义")
        print("  define <name> <dir/>    — 搜索定义位置")
        print("  complexity <file.py>    — 分析代码复杂度")
        print("  calls <file.py>         — 分析调用关系")
        sys.exit(1)

    command = sys.argv[1]
    path_arg = sys.argv[2]

    if command == 'symbols':
        extract_symbols(path_arg)
    elif command == 'define':
        if len(sys.argv) < 4:
            print("❌ 需要指定搜索名称: python analyze.py define <name> <dir/>")
            sys.exit(1)
        search_definition(sys.argv[3], path_arg)
    elif command == 'complexity':
        analyze_complexity(path_arg)
    elif command == 'calls':
        extract_symbols(path_arg)
        print("\n💡 调用关系分析需要安装 pyright，稍后完善")
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
