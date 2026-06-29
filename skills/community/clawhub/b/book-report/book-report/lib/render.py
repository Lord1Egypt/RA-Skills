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


def call_fetch(title: str, author: str, out_path: Path, lang: str = "zh") -> dict:
    """调 fetch.py 抓源数据"""
    cmd = ["python3", str(ROOT / "lib" / "fetch.py"), "--title", title]
    if author:
        cmd += ["--author", author]
    if lang:
        cmd += ["--lang", lang]
    cmd += ["--out", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[render] fetch.py 失败：{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out_path.read_text(encoding="utf-8"))


def call_pdf_extract(pdf_path: str) -> dict:
    """调 pdf_extract.py 抽 PDF"""
    if not Path(pdf_path).exists():
        return {"ok": False, "error": f"PDF 文件不存在: {pdf_path}"}
    # 直接 import 拿结构化数据（不通过 stdout）
    import importlib.util
    spec = importlib.util.spec_from_file_location("pdf_extract", str(ROOT / "lib" / "pdf_extract.py"))
    if spec is None or spec.loader is None:
        return {"ok": False, "error": "无法加载 pdf_extract.py"}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.extract_text(pdf_path)


def extract_fields(sources: dict, pdf_data: dict | None = None) -> dict:
    """
    从源数据中抽取 9 个固定字段
    pdf_data: 可选，从 PDF 抽的字段（覆盖能稳抽的 4 个）
    """
    title = sources["title"]
    author = sources.get("author", "")
    lang = sources.get("lang", "zh")
    baidu = sources["sources"]["baidu"]
    wiki = sources["sources"]["wiki"]
    zhihu = sources["sources"]["zhihu"]

    summary = baidu.get("summary") or wiki.get("body_excerpt", "")[:500] or f"《{title}》研究数据。"

    info_box = {}
    info_box.update(baidu.get("info_box", {}))
    info_box.update(wiki.get("info_box", {}))

    # 如果有 PDF 数据，标注哪些字段来自 PDF（让 LLM 知道边界）
    pdf_note = ""
    if pdf_data and pdf_data.get("ok"):
        pdf_note = f"\n\n> 📄 **PDF 抽取来源**（共 {pdf_data['page_count']} 页 / {pdf_data['char_count']} 字符）：\n"
        pdf_note += f"> - 4 字段可从 PDF 稳抽：情节梗概 / 人物 / 金句 / 创作背景\n"
        pdf_note += f"> - 5 字段仍走 web：主题 / 获奖 / 作者其他作品 / 关系图 / 书名\n"

    return {
        "title": title,
        "author": author,
        "lang": lang,
        "summary": summary.strip() + pdf_note,
        "info_box": info_box,
        "baidu_body": baidu.get("summary", ""),
        "wiki_body": wiki.get("body_excerpt", "")[:3000],
        "zhihu_snippets": zhihu.get("snippets", []),
        "source_urls": {
            "baidu": baidu.get("url", ""),
            "wiki": wiki.get("url", ""),
            "zhihu": zhihu.get("url", ""),
        },
        "pdf_data": pdf_data if (pdf_data and pdf_data.get("ok")) else None,
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
    p.add_argument("--lang", choices=["zh", "en"], default="zh", help="语言（zh=中文经典, en=英文经典）")
    p.add_argument("--pdf", help="PDF 路径（可选，提供则从 PDF 抽 4 字段，web 抽其余 5 字段）")
    p.add_argument("--mode", choices=["html", "chat", "both"], default="both")
    p.add_argument("--cache", action="store_true", help="使用缓存的源数据，不重新抓取")
    args = p.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c for c in args.title if c.isalnum() or c in "._-").strip() or "book"
    cache_json = ROOT / "sources" / f"raw__{safe_title}__{args.lang}.json"

    # 1) 抓源（除非 --cache 且缓存存在）
    if args.cache and cache_json.exists():
        print(f"[render] 使用缓存 {cache_json}", file=sys.stderr)
        sources = json.loads(cache_json.read_text(encoding="utf-8"))
    else:
        sources = call_fetch(args.title, args.author, cache_json, args.lang)

    # 2) PDF 抽取（如果提供）
    pdf_data = None
    if args.pdf:
        print(f"[render] 抽 PDF: {args.pdf}", file=sys.stderr)
        pdf_data = call_pdf_extract(args.pdf)
        if pdf_data.get("ok"):
            print(f"[render] PDF OK: {pdf_data['page_count']} 页 / {pdf_data['char_count']} 字符", file=sys.stderr)
        else:
            print(f"[render] PDF FAIL: {pdf_data.get('error', '?')}", file=sys.stderr)

    # 3) 字段抽取
    fields = extract_fields(sources, pdf_data or {})
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
            "wiki": sources["sources"]["wiki"]["ok"],
            "zhihu": sources["sources"]["zhihu"]["ok"],
            **({"goodreads": sources["sources"].get("goodreads", {}).get("ok", False)} if args.lang == "en" else {}),
            **({"douban_en": sources["sources"].get("douban_en", {}).get("ok", False)} if args.lang == "en" else {}),
        }
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
