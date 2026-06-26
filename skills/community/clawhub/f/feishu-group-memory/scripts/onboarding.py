#!/usr/bin/env python3
"""
onboarding.py — 行业知识包配置（纯文件读写，不调用 LLM）

命令：
  check   --workspace DIR                检查是否已配置，返回配置内容
  setup   --industry SLUG --workspace    加载内置行业包
  save    --content TEXT --workspace     保存任意内容（由 AI 生成后传入）
"""

import argparse, json, sys
from pathlib import Path

SKILL_DIR        = Path(__file__).parent.parent
INDUSTRIES_DIR   = SKILL_DIR / "industries"
CONTEXT_FILENAME = "feishu-memory-context.md"

BUILTIN_INDUSTRIES = {
    "sales":            "sales.md",
    "customer-service": "customer-service.md",
    "legal":            "legal.md",
    "project":          "project.md",
}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def err(msg):
    out({"error": msg})
    sys.exit(1)

def context_path(workspace):
    return Path(workspace).expanduser() / CONTEXT_FILENAME


def cmd_check(args):
    path = context_path(args.workspace)
    if path.exists() and path.stat().st_size > 0:
        content = path.read_text(encoding="utf-8")
        first_line = content.split("\n")[0].strip("# ").strip()
        out({"configured": True, "context_file": str(path),
             "summary": first_line, "context": content})
    else:
        out({"configured": False})


def cmd_setup(args):
    slug = args.industry.lower().strip()
    if slug not in BUILTIN_INDUSTRIES:
        err(f"未知行业: {slug}。可用: {', '.join(BUILTIN_INDUSTRIES.keys())}")
    src = INDUSTRIES_DIR / BUILTIN_INDUSTRIES[slug]
    if not src.exists():
        err(f"行业文件不存在: {src}")
    content = src.read_text(encoding="utf-8")
    dest = context_path(args.workspace)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    out({"success": True, "industry": slug, "context_file": str(dest),
         "message": f"已加载「{slug}」行业知识包"})


def cmd_save(args):
    """保存 AI 生成的自定义知识包内容。"""
    content = args.content.strip()
    if not content:
        err("content 不能为空")
    dest = context_path(args.workspace)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    out({"success": True, "context_file": str(dest),
         "chars": len(content), "message": "自定义知识包已保存"})


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("check")
    c.add_argument("--workspace", default="~/.openclaw/workspace")

    s = sub.add_parser("setup")
    s.add_argument("--industry", required=True)
    s.add_argument("--workspace", default="~/.openclaw/workspace")

    sv = sub.add_parser("save")
    sv.add_argument("--content", required=True)
    sv.add_argument("--workspace", default="~/.openclaw/workspace")

    args = p.parse_args()
    if   args.cmd == "check": cmd_check(args)
    elif args.cmd == "setup": cmd_setup(args)
    elif args.cmd == "save":  cmd_save(args)
    else: err("请指定命令: check | setup | save")

if __name__ == "__main__":
    main()
