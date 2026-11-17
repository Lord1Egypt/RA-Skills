#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把源站整理成一份**对外发布**的静态产物目录（零第三方依赖，纯 stdlib）。

存在的理由：很多站有两份产物——内部完整版（含草稿/未核实/敏感数据）和对外发布版。
默认目录往往是前者，直接传上去就把没治理过的数据暴露了。本脚本干的是
「挑选 + 清洗 + 校验」这一步，产出物再交给 deploy_oss.py 上传。

做什么：
    1. 复制 --src 到 --out，跳过源码、密钥、VCS、内部草稿等绝不该上线的文件
    2. 替换站点 URL 占位符：__SITE_URL__ / {{SITE_URL}} / %SITE_URL%
    3. --no-inbox 额外剔除未核实/待审数据目录（对外版不该含未核实数据）
    4. 收尾校验：必须有入口页；打印产物清单供人工核对

用法：
    python build_static.py --out public
    python build_static.py --src web --out public --site-url https://demo.example.com
    python build_static.py --src dist --out public --no-inbox --exclude "*.bak,staging/"
    python build_static.py --src dist --out public --dry-run   # 只看会做什么

退出码：0 成功；1 校验失败
"""
import argparse
import fnmatch
import os
import shutil
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 绝不该出现在对外产物里的东西
NEVER_EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
                      ".idea", ".vscode", ".github", ".svn", ".DS_Store",
                      "private", "drafts", ".internal", ".cache"}
NEVER_INCLUDE_FILES = {".env", ".gitignore", ".npmrc", ".netrc", "docker-compose.yml",
                       "Dockerfile", "Makefile", "package.json", "package-lock.json",
                       "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "requirements.txt",
                       "manifest.yaml", "SKILL.md", "README.md", "LICENSE"}
NEVER_INCLUDE_GLOB = [
    "*.py", "*.pyc", "*.pyo", "*.ps1", "*.bat", "*.sh", "*.sql", "*.sqlite",
    "*.db", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", ".env.*",
    "*.bak", "*.tmp", "*.orig", "*.local.*",
]
# --no-inbox 时要剔除的「未核实/待审」数据
INBOX_DIRS = {"inbox", "review", "pending", "staging", "_drafts", "unverified"}
INBOX_GLOB = ["inbox*", "*_inbox*", "*_pending*", "*_unverified*", "*.review.*"]

URL_PLACEHOLDERS = ["__SITE_URL__", "{{SITE_URL}}", "%SITE_URL%", "{SITE_URL}"]

TEXT_EXT = {".html", ".htm", ".css", ".js", ".json", ".xml", ".txt", ".md",
            ".svg", ".yml", ".yaml", ".csv", ".map"}


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def matches(name, patterns):
    low = name.lower()
    for p in patterns:
        if fnmatch.fnmatch(low, p.lower()):
            return True
    return False


def should_skip(rel_path, is_dir, args):
    """返回排除原因，不排除则返回 None。"""
    parts = rel_path.replace("\\", "/").split("/")
    base = parts[-1]

    for d in parts[:-1]:
        if d in NEVER_EXCLUDE_DIRS:
            return "版本控制/依赖/私有目录: %s" % d
        if args.no_inbox and d.lower() in INBOX_DIRS:
            return "未核实目录(--no-inbox): %s" % d

    if is_dir:
        return None

    if base in NEVER_INCLUDE_FILES:
        return "不该上线的文件: %s" % base
    if matches(base, NEVER_INCLUDE_GLOB):
        return "源码/密钥/备份: %s" % base
    if args.no_inbox and matches(base, INBOX_GLOB):
        return "未核实数据(--no-inbox): %s" % base
    if parts[0] == ".git":
        return "VCS 元数据"

    # 用户自定义排除：支持按路径 glob 匹配
    for p in args.exclude_list:
        if fnmatch.fnmatch(rel_path.replace("\\", "/"), p) or \
           fnmatch.fnmatch(base, p) or fnmatch.fnmatch(base, p.rstrip("/")):
            return "用户 --exclude: %s" % p
    return None


def replace_placeholders(text, site_url):
    for ph in URL_PLACEHOLDERS:
        text = text.replace(ph, site_url)
    # 常见的相对占位（(site.url) 之类）
    return text


def copy_tree(src, out, args):
    copied, skipped, cleaned = [], [], []
    root = os.path.abspath(src)
    dest = os.path.abspath(out)

    if os.path.exists(dest):
        if not args.force:
            log("✗ 输出目录已存在：%s（加 --force 覆盖，或用新目录避免混淆）" % dest)
            sys.exit(1)
        shutil.rmtree(dest)

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir
        dirnames[:] = sorted(d for d in dirnames
                             if not should_skip(os.path.join(rel_dir, d) if rel_dir else d,
                                                True, args))
        os.makedirs(os.path.join(dest, rel_dir) if rel_dir else dest, exist_ok=True)

        for fn in sorted(filenames):
            rel = os.path.join(rel_dir, fn) if rel_dir else fn
            reason = should_skip(rel, False, args)
            if reason:
                skipped.append((rel, reason))
                continue
            s = os.path.join(dirpath, fn)
            d = os.path.join(dest, rel)
            ext = os.path.splitext(fn)[1].lower()
            if args.site_url and ext in TEXT_EXT:
                try:
                    text = open(s, "r", encoding="utf-8").read()
                    new = replace_placeholders(text, args.site_url)
                    if new != text:
                        cleaned.append(rel)
                    if not args.dry_run:
                        open(d, "w", encoding="utf-8", newline="").write(new)
                    copied.append(rel)
                    continue
                except (UnicodeDecodeError, OSError):
                    pass  # 二进制或非 utf-8，走普通复制
            if not args.dry_run:
                shutil.copy2(s, d)
            copied.append(rel)
    return copied, skipped, cleaned


def main():
    ap = argparse.ArgumentParser(description="整理对外发布的静态产物")
    ap.add_argument("--src", default=".", help="源目录，默认当前目录")
    ap.add_argument("--out", required=True, help="输出目录（建议 public/，并加进 .gitignore）")
    ap.add_argument("--site-url", default="", help="站点绝对 URL，用于替换 URL 占位符")
    ap.add_argument("--index", default="index.html", help="入口页文件名，默认 %(default)s")
    ap.add_argument("--exclude", default="", help="额外排除 glob，逗号分隔")
    ap.add_argument("--no-inbox", action="store_true",
                    help="剔除未核实/待审数据目录与文件")
    ap.add_argument("--force", action="store_true", help="输出目录已存在时覆盖")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件")
    args = ap.parse_args()

    args.exclude_list = [p.strip() for p in args.exclude.split(",") if p.strip()]
    src = os.path.abspath(args.src)
    if not os.path.isdir(src):
        log("✗ 源目录不存在：%s" % src); sys.exit(1)

    log("源=%s  输出=%s  %s" % (src, os.path.abspath(args.out),
                                "[dry-run]" if args.dry_run else ""))
    if not args.no_inbox:
        log("! 未加 --no-inbox：产物会保留草稿/待核实数据。对外发布请确认这是你要的。")

    copied, skipped, cleaned = copy_tree(src, args.out, args)

    log("复制 %d 个文件%s" % (len(copied), ""
                             if not cleaned else "，其中 %d 个做了 URL 占位符替换" % len(cleaned)))
    if skipped:
        log("排除 %d 项：" % len(skipped))
        for rel, reason in skipped[:15]:
            log("   - %-45s %s" % (rel, reason))
        if len(skipped) > 15:
            log("   ... 还有 %d 项" % (len(skipped) - 15))

    # 收尾校验：必须有入口页；也顺便提醒别把内部数据混进来
    problems = []
    if args.index not in copied and not any(
            c.endswith("/" + args.index) or c == args.index for c in copied):
        problems.append("产物里找不到入口页 %s" % args.index)
    for bad in copied:
        low = bad.lower()
        if args.no_inbox and ("inbox" in low or "unverified" in low or "_pending" in low):
            problems.append("产物中仍疑似含未核实数据：%s" % bad)
        if low.endswith((".pem", ".key", ".p12", ".pfx")) or low.startswith(".env"):
            problems.append("产物中疑似含密钥/环境变量：%s" % bad)

    if problems:
        for p in problems:
            log("✗ %s" % p)
        sys.exit(1)

    log("✓ 产物就绪：%s" % os.path.abspath(args.out))
    log("  下一步：python deploy_oss.py --bucket <桶> --region cn-hongkong "
        "--dir %s --setup-website --verify-public --verify" % args.out)


if __name__ == "__main__":
    main()
