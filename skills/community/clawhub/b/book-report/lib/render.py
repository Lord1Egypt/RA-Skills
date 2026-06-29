"""
lib/render.py - 把源数据渲染成 HTML 报告 + 弹药库

流程：
  1. 调 fetch.py 抓源数据
  2. LLM（本进程内）结构化抽取 9 字段
  3. 用 Jinja2 套模板 → 写 reports/
  4. 输出两个文件路径
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from jinja2 import Template, Environment, FileSystemLoader

ROOT = Path(__file__).parent.parent
TEMPLATES = ROOT / "templates"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def call_fetch(title: str, author: str, out_path: Path) -> dict:
    """调 fetch.py 抓源数据"""
    cmd = ["python3", str(ROOT / "lib" / "fetch.py"), "--title", title]
    if author:
        cmd += ["--author", author]
    cmd += ["--out", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[render] fetch.py 失败：{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out_path.read_text(encoding="utf-8"))


def extract_fields(sources: dict) -> dict:
    """
    从源数据中抽取 9 个固定字段
    重要：本函数是机械抽取 + 启发式，复杂内容由 LLM 接管
    但当前实现走轻量抽取 + 调用方在模板里展示原文
    """
    title = sources["title"]
    author = sources.get("author", "")
    baidu = sources["sources"]["baidu"]
    wiki = sources["sources"]["wiki_zh"]
    zhihu = sources["sources"]["zhihu"]

    summary = baidu.get("summary") or wiki.get("body_excerpt", "")[:500] or f"《{title}》研究数据。"

    info_box = {}
    info_box.update(baidu.get("info_box", {}))
    info_box.update(wiki.get("info_box", {}))

    return {
        "title": title,
        "author": author,
        "summary": summary.strip(),
        "info_box": info_box,
        "baidu_body": baidu.get("summary", ""),
        "wiki_body": wiki.get("body_excerpt", "")[:3000],
        "zhihu_snippets": zhihu.get("snippets", []),
        "source_urls": {
            "baidu": baidu.get("url", ""),
            "wiki": wiki.get("url", ""),
            "zhihu": zhihu.get("url", ""),
        },
    }


def render_html(data: dict, today: str) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)
    tpl = env.get_template("report.html.j2")
    return tpl.render(d=data, today=today)


def render_chat(data: dict, today: str) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)
    tpl = env.get_template("chat-kit.md.j2")
    return tpl.render(d=data, today=today)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--author", default="")
    p.add_argument("--mode", choices=["html", "chat", "both"], default="both")
    p.add_argument("--cache", action="store_true", help="使用缓存的源数据，不重新抓取")
    args = p.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c for c in args.title if c.isalnum() or c in "._-").strip() or "book"
    cache_json = ROOT / "sources" / f"raw__{safe_title}.json"

    if args.cache and cache_json.exists():
        print(f"[render] 使用缓存 {cache_json}", file=sys.stderr)
        sources = json.loads(cache_json.read_text(encoding="utf-8"))
    else:
        sources = call_fetch(args.title, args.author, cache_json)

    fields = extract_fields(sources)
    print(f"[render] 字段抽取完成：title={fields['title']!r}, summary 长度={len(fields['summary'])}", file=sys.stderr)

    outputs = []

    if args.mode in ("html", "both"):
        html = render_html(fields, today)
        html_path = REPORTS / f"{args.title}-{today}.html"
        html_path.write_text(html, encoding="utf-8")
        outputs.append(str(html_path))
        print(f"[render] HTML → {html_path}", file=sys.stderr)

    if args.mode in ("chat", "both"):
        chat = render_chat(fields, today)
        chat_path = REPORTS / f"chat-弹药库-{args.title}-v1.md"
        chat_path.write_text(chat, encoding="utf-8")
        outputs.append(str(chat_path))
        print(f"[render] 弹药库 → {chat_path}", file=sys.stderr)

    # 输出 JSON 给上层 caller 解析
    print(json.dumps({
        "outputs": outputs,
        "summary_excerpt": fields["summary"][:200],
        "source_ok": {
            "baidu": sources["sources"]["baidu"]["ok"],
            "wiki_zh": sources["sources"]["wiki_zh"]["ok"],
            "zhihu": sources["sources"]["zhihu"]["ok"],
        }
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
