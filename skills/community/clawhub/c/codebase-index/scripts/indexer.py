#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codebase Index — 代码库索引器
递归扫描项目目录，提取符号并构建可搜索的 JSON 索引。
支持：Python (ast)、通用文本 (ripgrep)
"""
import sys
import io
import ast
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.env', 'dist', 'build', '.next', 'target', 'bin', 'obj',
    '.openclaw', '.claude', '.vscode', '.idea',
}


def extract_python_symbols(filepath, rel_path):
    """用 ast 提取 Python 文件中的符号"""
    symbols = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            tree = ast.parse(f.read(), filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError):
        return symbols

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({
                        'name': item.name,
                        'line': item.lineno,
                        'docstring': ast.get_docstring(item, clean=True),
                    })
            symbols.append({
                'name': node.name,
                'type': 'class',
                'file': rel_path,
                'line': node.lineno,
                'end_line': node.end_lineno,
                'docstring': ast.get_docstring(node, clean=True),
                'methods': methods,
                'method_count': len(methods),
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 只记顶层函数
            is_method = False
            for parent in ast.walk(tree):
                if isinstance(parent, ast.ClassDef) and node in parent.body:
                    is_method = True
                    break
            if not is_method:
                symbols.append({
                    'name': node.name,
                    'type': 'function',
                    'file': rel_path,
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'docstring': ast.get_docstring(node, clean=True),
                    'async': isinstance(node, ast.AsyncFunctionDef),
                })
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # 模块级变量
                    if isinstance(target.ctx, ast.Store):
                        symbols.append({
                            'name': target.id,
                            'type': 'variable',
                            'file': rel_path,
                            'line': node.lineno,
                            'value': ast.dump(node.value)[:80],
                        })
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno,
                    })
            else:
                module = node.module or ''
                for alias in node.names:
                    imports.append({
                        'module': f"{module}.{alias.name}",
                        'alias': alias.asname,
                        'line': node.lineno,
                    })

    return symbols, imports


def scan_project(project_path, output=None):
    """扫描项目目录，构建符号索引"""
    root = Path(project_path).resolve()
    if not root.exists():
        print(f"❌ 路径不存在: {project_path}")
        return

    print(f"📚 扫描: {root}")
    print(f"⏳ 正在索引...")

    all_symbols = []
    all_imports = []
    file_count = 0
    py_count = 0
    errors = []

    for filepath in root.rglob('*'):
        if not filepath.is_file():
            continue

        rel_path = str(filepath.relative_to(root))
        # 跳过忽略目录（只检查相对路径部分）
        rel_parts = Path(rel_path).parts
        if any(part in IGNORE_DIRS for part in rel_parts):
            continue
        file_count += 1

        if filepath.suffix == '.py':
            py_count += 1
            try:
                result = extract_python_symbols(filepath, rel_path)
                if result:
                    syms, imps = result
                    all_symbols.extend(syms)
                    all_imports.extend(imps)
            except Exception as e:
                errors.append(f"{rel_path}: {e}")

    # 构建索引
    index = {
        'metadata': {
            'project': root.name,
            'path': str(root),
            'scanned_at': datetime.now().isoformat(),
            'total_files': file_count,
            'python_files': py_count,
            'total_symbols': len(all_symbols),
        },
        'symbols': all_symbols,
        'imports': all_imports,
        'errors': errors,
    }

    # 按类型统计
    by_type = {}
    for s in all_symbols:
        t = s['type']
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(s['name'])
    index['statistics'] = {t: len(names) for t, names in by_type.items()}

    # 按文件统计
    by_file = {}
    for s in all_symbols:
        f = s['file']
        if f not in by_file:
            by_file[f] = 0
        by_file[f] += 1
    index['files_with_symbols'] = len(by_file)

    # 输出
    if output:
        output_path = Path(output)
        output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n✅ 索引已保存: {output_path}")
    else:
        print(json.dumps(index, ensure_ascii=False, indent=2))

    # 打印摘要
    print(f"\n{'='*50}")
    print(f"📊 索引摘要")
    print(f"{'='*50}")
    print(f"  文件总数:    {file_count}")
    print(f"  Python文件:  {py_count}")
    print(f"  符号总数:    {len(all_symbols)}")
    for t, count in index['statistics'].items():
        print(f"    {t}: {count}")
    print(f"  有符号的文件: {index['files_with_symbols']}")
    if errors:
        print(f"  ⚠️  错误: {len(errors)}")
        for e in errors[:5]:
            print(f"      {e}")

    return index


def query_index(index_path, query_text, filter_type=None):
    """查询符号索引"""
    if not Path(index_path).exists():
        print(f"❌ 索引文件不存在: {index_path}")
        return

    index = json.loads(Path(index_path).read_text(encoding='utf-8'))
    symbols = index.get('symbols', [])
    query_lower = query_text.lower()

    results = []
    for s in symbols:
        if filter_type and s['type'] != filter_type:
            continue
        if (query_lower in s['name'].lower() or
            (s.get('docstring') and query_lower in s['docstring'].lower())):
            results.append(s)

    # 排序：名称前缀匹配优先
    results.sort(key=lambda x: (
        0 if x['name'].lower().startswith(query_lower) else 1,
        x['name'],
    ))

    print(f"\n🔍 搜索: \"{query_text}\"")
    if filter_type:
        print(f"   过滤类型: {filter_type}")
    print(f"   找到 {len(results)} 个结果")
    print(f"{'='*50}")

    for r in results[:30]:
        doc = f" — {r['docstring'][:60]}" if r.get('docstring') else ''
        extra = ""
        if r['type'] == 'class' and r.get('method_count', 0) > 0:
            extra = f" ({r['method_count']} methods)"
        print(f"  {r['type']:10} {r['name']:25}  {r['file']}:{r['line']}{doc}{extra}")

    if len(results) > 30:
        print(f"  ... 还有 {len(results) - 30} 个结果")

    return results


def list_files(index_path):
    """列出索引中的所有文件"""
    index = json.loads(Path(index_path).read_text(encoding='utf-8'))
    files = set(s['file'] for s in index['symbols'])
    print(f"\n📁 文件列表 ({len(files)} 个):")
    for f in sorted(files):
        print(f"  📄 {f}")


def main():
    if len(sys.argv) < 2:
        print("Codebase Index — 代码库索引器")
        print()
        print("用法: python indexer.py <scan|query|files|stats> [参数]")
        print()
        print("  scan <目录> [--output index.json]")
        print("    — 扫描项目构建索引")
        print()
        print("  query <关键词> --index index.json [--type class|function|variable]")
        print("    — 搜索符号")
        print()
        print("  files --index index.json")
        print("    — 列出所有文件")
        print()
        print("  stats --index index.json")
        print("    — 索引统计")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'scan':
        if len(sys.argv) < 3:
            print("❌ 需要指定扫描目录")
            sys.exit(1)
        project_path = sys.argv[2]
        output = None
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
                output = sys.argv[i + 1]
        scan_project(project_path, output)

    elif command == 'query':
        if len(sys.argv) < 3:
            print("❌ 需要指定查询关键词")
            sys.exit(1)
        query = sys.argv[2]
        index_path = None
        filter_type = None
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--index' and i + 1 < len(sys.argv):
                index_path = sys.argv[i + 1]
            if sys.argv[i] == '--type' and i + 1 < len(sys.argv):
                filter_type = sys.argv[i + 1]
        if not index_path:
            print("❌ 需要 --index <index.json>")
            sys.exit(1)
        query_index(index_path, query, filter_type)

    elif command == 'files':
        index_path = None
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == '--index' and i + 1 < len(sys.argv):
                index_path = sys.argv[i + 1]
        if not index_path:
            print("❌ 需要 --index <index.json>")
            sys.exit(1)
        list_files(index_path)

    elif command == 'stats':
        index_path = None
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == '--index' and i + 1 < len(sys.argv):
                index_path = sys.argv[i + 1]
        if not index_path:
            print("❌ 需要 --index <index.json>")
            sys.exit(1)
        index = json.loads(Path(index_path).read_text(encoding='utf-8'))
        meta = index.get('metadata', {})
        stats = index.get('statistics', {})
        print(f"\n📊 索引统计")
        print(f"{'='*50}")
        for k, v in meta.items():
            print(f"  {k}: {v}")
        if stats:
            print(f"\n  符号分布:")
            for t, count in stats.items():
                print(f"    {t}: {count}")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
