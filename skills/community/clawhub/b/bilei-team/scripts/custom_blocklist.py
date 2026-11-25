#!/usr/bin/env python3
"""用户自定义信源名单管理：add / remove / list / check。

存放于技能目录之外（~/.bilei/user-blocklist.md），更新技能不会丢失。
与随包分发的 references/source-blocklist.md 合并执行；用户名单优先。

用法（AI 直接调用，用户零操作）：
  python3 custom_blocklist.py add <域名> [--class A|B] [--reason "理由"]
  python3 custom_blocklist.py remove <域名>
  python3 custom_blocklist.py list [--json]
  python3 custom_blocklist.py check <域名>        # 查该域名在哪份名单、哪一类
  python3 custom_blocklist.py path                # 打印用户名单路径
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

USER_PATH = os.path.expanduser("~/.bilei/user-blocklist.md")
OFFICIAL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "references", "source-blocklist.md")

HEADER = """# 我的自定义信源名单

本文件由「避雷.skill」自动维护，也可手动编辑。
更新技能不会删除本文件。命中的来源按类别硬处理。

"""
A_SECTION = "## A 类 · 禁用\n\n"
B_SECTION = "\n## B 类 · 限用\n\n"


def normalize(domain):
    """去协议、去 www、去路径，只留主域名。"""
    d = domain.strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = re.sub(r"^www\.", "", d)
    d = d.split("/")[0].split("?")[0]
    return d


def ensure_file():
    os.makedirs(os.path.dirname(USER_PATH), exist_ok=True)
    if not os.path.exists(USER_PATH):
        with open(USER_PATH, "w", encoding="utf-8") as f:
            f.write(HEADER + A_SECTION + "（暂无）\n" + B_SECTION + "（暂无）\n")


def parse():
    """返回 {A:[(domain,reason)], B:[(domain,reason)]}。"""
    ensure_file()
    result = {"A": [], "B": []}
    current = None
    with open(USER_PATH, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("## A 类"):
                current = "A"
            elif line.startswith("## B 类"):
                current = "B"
            elif line.startswith("- ") and current:
                body = line[2:].strip()
                if body.startswith("（暂无）") or not body:
                    continue
                parts = re.split(r"\s+[—–-]\s+", body, 1)
                domain = normalize(parts[0])
                reason = parts[1] if len(parts) > 1 else ""
                if domain:
                    result[current].append((domain, reason))
    return result


def write(entries):
    def block(items):
        return "\n".join("- %s%s" % (d, (" — " + r) if r else "") for d, r in items) or "（暂无）"
    with open(USER_PATH, "w", encoding="utf-8") as f:
        f.write(HEADER + A_SECTION + block(entries["A"]) + B_SECTION + block(entries["B"]) + "\n")


def parse_official():
    """读随包名单位，返回 {A:[domain], B:[domain]}；不存在则返回空。"""
    out = {"A": [], "B": []}
    if not os.path.exists(OFFICIAL_PATH):
        return out
    current = None
    with open(OFFICIAL_PATH, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("## A 类"):
                current = "A"
            elif line.startswith("## B 类"):
                current = "B"
            elif line.startswith("|") and current:
                cells = [c.strip() for c in line.strip("|").split("|")]
                for cell in cells:
                    for m in re.findall(r"`([a-z0-9.-]+\.[a-z]{2,})`", cell):
                        out[current].append(m)
    return out


def cmd_add(args):
    entries = parse()
    domain = normalize(args.domain)
    cls = args.cls.upper()
    reason = args.reason or ("用户添加 " + datetime.now().strftime("%Y-%m-%d"))
    # 先从两类里都删掉，避免重复
    for k in ("A", "B"):
        entries[k] = [(d, r) for d, r in entries[k] if d != domain]
    entries[cls].append((domain, reason))
    write(entries)
    print("已加入 %s 类：%s（%s）" % (cls, domain, reason))


def cmd_remove(args):
    entries = parse()
    domain = normalize(args.domain)
    before = sum(len(v) for v in entries.values())
    for k in ("A", "B"):
        entries[k] = [(d, r) for d, r in entries[k] if d != domain]
    write(entries)
    after = sum(len(v) for v in entries.values())
    print("已移除：%s" % domain if after < before else "名单里没有：%s" % domain)


def cmd_list(args):
    entries = parse()
    if args.json:
        print(json.dumps(entries, ensure_ascii=False))
        return
    print("用户名单：" + USER_PATH)
    for k, label in (("A", "A 类 · 禁用"), ("B", "B 类 · 限用")):
        print("\n%s" % label)
        if entries[k]:
            for d, r in entries[k]:
                print("  - %s%s" % (d, (" — " + r) if r else ""))
        else:
            print("  （暂无）")


def cmd_check(args):
    domain = normalize(args.domain)
    off = parse_official()
    user = parse()
    hits = []
    for cls in ("A", "B"):
        if any(domain == d or domain.endswith("." + d) for d in off[cls]):
            hits.append("官方名单 %s 类" % cls)
        if any(domain == d or domain.endswith("." + d) for d, _ in user[cls]):
            hits.append("用户名单 %s 类" % cls)
    print("%s → %s" % (domain, " / ".join(hits) if hits else "未命中（走特征判定）"))


def main():
    ap = argparse.ArgumentParser(description="用户自定义信源名单管理")
    sub = ap.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="加入名单")
    p_add.add_argument("domain")
    p_add.add_argument("--class", dest="cls", choices=["A", "B"], default="A")
    p_add.add_argument("--reason", default="")
    p_add.set_defaults(func=cmd_add)

    p_rm = sub.add_parser("remove", help="移出名单")
    p_rm.add_argument("domain")
    p_rm.set_defaults(func=cmd_remove)

    p_ls = sub.add_parser("list", help="查看名单")
    p_ls.add_argument("--json", action="store_true")
    p_ls.set_defaults(func=cmd_list)

    p_ck = sub.add_parser("check", help="查域名命中情况")
    p_ck.add_argument("domain")
    p_ck.set_defaults(func=cmd_check)

    sub.add_parser("path", help="打印用户名单路径").set_defaults(
        func=lambda _a: print(USER_PATH))

    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
