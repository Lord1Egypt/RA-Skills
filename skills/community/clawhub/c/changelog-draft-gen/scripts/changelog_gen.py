#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 更新日志生成器（零依赖 / conventional commits 归类 / last-good 原子写 / JSON IR）
import argparse, json, os, re, subprocess, sys, tempfile
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CONV = re.compile(r"^(feat|fix|perf|refactor|docs|test|chore|style|build|ci|revert)(\(([^)]*)\))?(!)?:\s*(.*)$")
MAP = {"feat": "Added", "fix": "Fixed", "perf": "Changed", "refactor": "Changed",
       "docs": "Docs", "test": "Other", "style": "Other", "build": "Other",
       "ci": "Other", "chore": "Other", "revert": "Other"}


def git(repo, args):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(prog="changelog_gen", description="从 conventional commits 生成 CHANGELOG 草稿")
    ap.add_argument("--repo", default=".", help="git 仓库路径")
    ap.add_argument("--from", dest="frm", help="起始 ref（默认最近 tag，无 tag 则全量最近 500 条）")
    ap.add_argument("--to", default="HEAD")
    ap.add_argument("--version", help="版本号标签，如 v1.2.0")
    ap.add_argument("--out", help="写入文件（临时文件+原子替换，校验失败不覆盖）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(os.path.join(a.repo, ".git")) and "git" not in subprocess.run(
            ["git", "-C", a.repo, "rev-parse", "--git-dir"], capture_output=True, text=True).stdout:
        print(json.dumps({"errors": [{"code": "CHG_E_NO_GIT", "subject": a.repo,
                                      "evidence": "不是 git 仓库", "fixes": ["在仓库根目录运行或用 --repo 指定"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    frm = a.frm
    if not frm:
        t = git(a.repo, ["describe", "--tags", "--abbrev=0"])
        frm = t.stdout.strip() if t.returncode == 0 and t.stdout.strip() else None
    rng_args = ["%s..%s" % (frm, a.to)] if frm else ["-n", "500", a.to]
    p = git(a.repo, ["log", "--pretty=%x1e%H%x1f%s%x1f%b"] + rng_args)
    if p.returncode != 0:
        print(json.dumps({"errors": [{"code": "CHG_E_GIT_FAIL", "subject": " ".join(rng_args),
                                      "evidence": (p.stderr or "").strip()[:200], "fixes": ["确认 git 可用且 ref 存在"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    entries = [e for e in p.stdout.split("\x1e") if e.strip()]
    sections = {"Breaking": [], "Added": [], "Changed": [], "Fixed": [], "Docs": [], "Other": []}
    for e in entries:
        parts = e.split("\x1f")
        if len(parts) < 2:
            continue
        h, subj = parts[0].strip()[:7], parts[1].strip()
        body = parts[2] if len(parts) > 2 else ""
        m = CONV.match(subj)
        if m:
            sec = MAP.get(m.group(1), "Other")
            line = "- `%s` %s" % (h, subj)
            if m.group(4) or "BREAKING CHANGE" in body:
                sections["Breaking"].append(line)
            else:
                sections[sec].append(line)
        else:
            sections["Other"].append("- `%s` %s" % (h, subj))
    if not any(sections.values()):
        print(json.dumps({"errors": [{"code": "CHG_E_NO_COMMITS", "subject": " ".join(rng_args),
                                      "evidence": "区间内没有提交", "fixes": ["检查 --from/--to 或先提交"]}]},
                         ensure_ascii=False))
        sys.exit(1)
    ver = a.version or "Unreleased"
    lines = ["## %s - %s" % (ver, date.today().isoformat()), ""]
    zh = {"Breaking": "Breaking / 破坏性变更", "Added": "Added / 新增", "Changed": "Changed / 变更",
          "Fixed": "Fixed / 修复", "Docs": "Docs / 文档", "Other": "Other / 其他"}
    for k in ("Breaking", "Added", "Changed", "Fixed", "Docs", "Other"):
        if sections[k]:
            lines.append("### %s" % zh[k])
            lines.extend(sections[k])
            lines.append("")
    lines.append("<!-- 草稿由 conventional commits 归类生成，发布前请人工润色 -->")
    text = "\n".join(lines)
    if a.json:
        print(json.dumps({"version": ver, "sections": {k: v for k, v in sections.items() if v}},
                         ensure_ascii=False, indent=2))
    else:
        print(text)
    if a.out:
        d = os.path.dirname(os.path.abspath(a.out))
        fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="\n") as fh:
            fh.write(text + "\n")
        os.replace(tmp, a.out)
    sys.exit(0)


if __name__ == "__main__":
    main()
