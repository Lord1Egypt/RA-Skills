#!/usr/bin/env python3
"""
API Doc Generator CLI
命令行工具：从代码自动生成 API 文档
"""

import argparse
import sys
import os
import glob
from generator import generate_docs, batch_generate, analyze_code


def cmd_analyze(args):
    """分析代码并生成文档"""
    if args.code:
        code = args.code
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        print("❌ Please provide --code or --file", file=sys.stderr)
        sys.exit(1)

    result = generate_docs(
        code,
        output_format=args.format,
        title=args.title,
        language=args.language,
        framework=args.framework
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ Documentation saved to {args.output}")
    else:
        print(result)


def cmd_batch(args):
    """批量处理目录"""
    pattern = os.path.join(args.directory, "**/*." + args.extension)
    files = glob.glob(pattern, recursive=True)

    if args.include:
        included_files = []
        for pattern2 in args.include:
            included_files.extend(glob.glob(os.path.join(args.directory, "**/" + pattern2), recursive=True))
        files = list(set(files) | set(included_files))

    if not files:
        print(f"❌ No files found matching {pattern}", file=sys.stderr)
        sys.exit(1)

    print(f"📁 Found {len(files)} files to process...")

    os.makedirs(args.output, exist_ok=True)
    results = batch_generate(
        files,
        output_format=args.format,
        language=args.language,
        framework=args.framework,
        output_dir=args.output
    )

    success = sum(1 for v in results.values() if not v.startswith("ERROR"))
    for path, output in results.items():
        status = "✅" if not output.startswith("ERROR") else "❌"
        print(f"  {status} {path} → {output}")

    print(f"\n🎉 Done! {success}/{len(files)} files processed successfully")


def cmd_preview(args):
    """预览提取的端点"""
    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    endpoints = analyze_code(code, language=args.language, framework=args.framework)

    if not endpoints:
        print("⚠️ No endpoints found")
        sys.exit(0)

    print(f"🔍 Found {len(endpoints)} endpoint(s):\n")
    for i, ep in enumerate(endpoints, 1):
        print(f"  [{i}] {ep.get('method', 'AUTO'):6} {ep['path']}")
        print(f"       Function: {ep.get('function', 'N/A')}")
        print(f"       Framework: {ep.get('framework', 'unknown')}")
        if ep.get("description"):
            print(f"       Description: {ep['description']}")
        params = ep.get("parameters", {})
        if params:
            print(f"       Parameters: {', '.join(params.keys())}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="🛠️ API Doc Generator — 从代码自动生成 API 文档",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="分析代码并生成文档")
    analyze_parser.add_argument("--code", "-c", type=str, help="直接传入代码字符串")
    analyze_parser.add_argument("--file", "-f", type=str, help="从文件读取代码")
    analyze_parser.add_argument("--format", "-o", type=str, choices=["markdown", "openapi", "openapi-yaml", "postman"],
                               default="markdown", help="输出格式 (default: markdown)")
    analyze_parser.add_argument("--title", "-t", type=str, default="API Documentation", help="文档标题")
    analyze_parser.add_argument("--language", "-l", type=str, choices=["python", "javascript", "auto"],
                               default="auto", help="代码语言")
    analyze_parser.add_argument("--framework", "-w", type=str,
                               choices=["fastapi", "flask", "django", "express", "nestjs", "auto"],
                               default="auto", help="Web 框架")
    analyze_parser.add_argument("--output", "-p", type=str, help="输出文件路径")
    analyze_parser.set_defaults(func=cmd_analyze)

    # batch command
    batch_parser = subparsers.add_parser("batch", help="批量处理目录中的文件")
    batch_parser.add_argument("directory", type=str, help="要处理的目录路径")
    batch_parser.add_argument("--format", "-o", type=str, choices=["markdown", "openapi", "openapi-yaml", "postman"],
                             default="markdown", help="输出格式")
    batch_parser.add_argument("--extension", "-e", type=str, default="py", help="文件扩展名过滤 (default: py)")
    batch_parser.add_argument("--include", "-i", type=str, nargs="+", help="额外包含的文件模式")
    batch_parser.add_argument("--language", "-l", type=str, choices=["python", "javascript", "auto"],
                             default="auto", help="代码语言")
    batch_parser.add_argument("--framework", "-w", type=str,
                             choices=["fastapi", "flask", "django", "express", "nestjs", "auto"],
                             default="auto", help="Web 框架")
    batch_parser.add_argument("--output", "-p", type=str, default="docs", help="输出目录")
    batch_parser.set_defaults(func=cmd_batch)

    # preview command
    preview_parser = subparsers.add_parser("preview", help="预览检测到的端点列表")
    preview_parser.add_argument("--file", "-f", type=str, required=True, help="要分析的文件")
    preview_parser.add_argument("--language", "-l", type=str, choices=["python", "javascript", "auto"],
                               default="auto", help="代码语言")
    preview_parser.add_argument("--framework", "-w", type=str,
                               choices=["fastapi", "flask", "django", "express", "nestjs", "auto"],
                               default="auto", help="Web 框架")
    preview_parser.set_defaults(func=cmd_preview)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
