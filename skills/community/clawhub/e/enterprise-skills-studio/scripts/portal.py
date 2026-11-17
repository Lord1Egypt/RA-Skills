#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""portal.py - 技能门户生成器（技能库 -> 目录/README/HTML）

把散落在各目录的技能聚合为一个可被"发现"的全局视图：
  - 解决可发现性问题：业务/新人一眼看到有什么技能、干嘛的、谁维护
  - 治理可视化：结合 lifecycle registry 标注状态(Plan/Operate/弃用)
  - 复用防重：与 dupe_check 互补，先看到全貌再查重

输入：
  --skills-dir ROOT   技能库根目录（递归找各子目录的 SKILL.md）
  --registry reg.json 可选，lifecycle_track 的注册表，用于标注状态
输出：
  --out PORTAL.md     默认写到 ROOT/PORTAL.md
  --html              同时生成同名的 .html 静态页

解析 SKILL.md frontmatter：name / description / owner / version（可选）。
纯标准库。
"""

import argparse
import html
import json
import os
import re
import sys

RE_NAME = re.compile(r"^name:\s*(.+)$", re.M)
RE_DESC = re.compile(r"^description:\s*(.+)$", re.M)
RE_OWNER = re.compile(r"^owner:\s*(.+)$", re.M)
RE_VERSION = re.compile(r"^version:\s*(.+)$", re.M)


def parse_frontmatter(path):
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return {}
    def grab(rx, strip=True):
        m = rx.search(text)
        if not m:
            return ""
        v = m.group(1).strip()
        if strip:
            v = v.strip('"').strip("'").strip()
        return v
    return {
        "name": grab(RE_NAME),
        "description": grab(RE_DESC),
        "owner": grab(RE_OWNER),
        "version": grab(RE_VERSION),
    }


def collect(skills_dir):
    items = []
    for root, dirs, files in os.walk(skills_dir):
        if "SKILL.md" in files:
            fm = parse_frontmatter(os.path.join(root, "SKILL.md"))
            rel = os.path.relpath(root, skills_dir)
            # 去掉明显的非技能目录
            if fm.get("name"):
                items.append({"path": rel, "fm": fm})
    items.sort(key=lambda x: x["fm"].get("name", x["path"]))
    return items


def load_registry(path):
    if not path or not os.path.isfile(path):
        return {}
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out = {}
    for row in data if isinstance(data, list) else []:
        if isinstance(row, dict) and row.get("name"):
            out[row["name"]] = row
    return out


def render_md(items, reg, skills_dir):
    # 防御：技能元数据可能含 '<' '>' '&'（HTML 实体）或 '|'（表格分隔符），
    # 统一转义后再入表，避免恶意技能元数据在 Markdown 渲染器中注入。
    def esc_md(s):
        return html.escape(str(s).replace("|", "/"))
    lines = ["# 企业技能门户（Skill Portal）", ""]
    lines.append(f"生成自：`{html.escape(os.path.abspath(skills_dir))}`")
    lines.append(f"技能总数：**{len(items)}**")
    lines.append("")
    lines.append("| 技能 | 简介 | Owner | 版本 | 状态 | 路径 |")
    lines.append("|------|------|-------|------|------|------|")
    for it in items:
        fm = it["fm"]
        name = fm.get("name", "?")
        desc = fm.get("description", "")
        owner = fm.get("owner") or "-"
        ver = fm.get("version") or "-"
        stage = "-"
        if name in reg:
            stage = reg[name].get("stage", "-")
        lines.append(
            f"| {esc_md(name)} | {esc_md(desc)} | {esc_md(owner)} | {esc_md(ver)} | {esc_md(stage)} | `{esc_md(it['path'])}` |")
    lines.append("")
    lines.append("> 由 enterprise-skills-studio 的 portal.py 生成。")
    return "\n".join(lines)


def render_html(items, reg, skills_dir):
    # 防御（存储型 XSS）：技能元数据来自各 SKILL.md，可能由不可信作者编写，
    # 必须对所有插值字段做 html.escape，否则打开门户页即触发脚本注入。
    rows = []
    for it in items:
        fm = it["fm"]
        name = html.escape(fm.get("name", "?"))
        desc = html.escape(fm.get("description", ""))
        owner = html.escape(fm.get("owner") or "-")
        ver = html.escape(fm.get("version") or "-")
        stage = html.escape(reg.get(name, {}).get("stage", "-") if name in reg else "-")
        rows.append(
            f"<tr><td>{name}</td><td>{desc}</td><td>{owner}</td>"
            f"<td>{ver}</td><td>{stage}</td><td><code>{html.escape(it['path'])}</code></td></tr>")
    return f"""<!doctype html>
<html lang="zh"><head><meta charset="utf-8">
<title>企业技能门户</title>
<style>
body{{font-family:system-ui,'Segoe UI',sans-serif;margin:2rem;color:#222}}
h1{{font-size:1.4rem}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ddd;padding:.5rem;text-align:left;vertical-align:top}}
th{{background:#f5f5f5}}code{{background:#f0f0f0;padding:1px 4px;border-radius:3px}}
</style></head><body>
<h1>企业技能门户（Skill Portal）</h1>
<p>生成自 <code>{html.escape(os.path.abspath(skills_dir))}</code> · 技能总数：<b>{len(items)}</b></p>
<table><thead><tr>
<th>技能</th><th>简介</th><th>Owner</th><th>版本</th><th>状态</th><th>路径</th>
</tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<p><small>由 enterprise-skills-studio 的 portal.py 生成。</small></p>
</body></html>"""


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="portal", description="技能库 -> 门户目录/README/HTML")
    p.add_argument("--skills-dir", required=True, help="技能库根目录")
    p.add_argument("--registry", default=None,
                   help="可选 lifecycle 注册表 JSON")
    p.add_argument("--out", default=None, help="PORTAL.md 输出路径")
    p.add_argument("--html", action="store_true",
                   help="同时生成同名 .html 静态页")
    args = p.parse_args(argv)

    if not os.path.isdir(args.skills_dir):
        sys.stderr.write(f"[portal] 目录不存在: {args.skills_dir}\n")
        return 2

    items = collect(args.skills_dir)
    reg = load_registry(args.registry)

    out = args.out or os.path.join(args.skills_dir, "PORTAL.md")
    md = render_md(items, reg, args.skills_dir)
    with open(out, "w", encoding="utf-8") as f:
        f.write(md + "\n")
    print(f"已生成门户: {out}  （{len(items)} 个技能）")

    if args.html:
        html_path = os.path.splitext(out)[0] + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_html(items, reg, args.skills_dir))
        print(f"已生成 HTML: {html_path}")

    # 安全提示（企业合规）：产物含技能名称/描述/Owner/版本/路径等元数据，
    # 对外发布或挂到内网门户前，请先审查是否泄露内部能力、项目名或治理状态。
    sys.stderr.write(
        "[portal] 提示：生成的门户含技能元数据（名称/描述/Owner/路径等）。"
        "对外发布或挂内网前，请先确认无敏感信息泄露。\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
