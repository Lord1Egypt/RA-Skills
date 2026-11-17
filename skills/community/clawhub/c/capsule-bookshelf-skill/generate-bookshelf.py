#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书摘胶囊 · 书架生成器
读取 capsule-registry.json，基于 bookshelf-template.html 生成书架总页面。
纯 Python 标准库，零依赖。
"""

import json
import os
import sys
from datetime import datetime


def _is_path_safe(base_dir, relative_path):
    """校验 relative_path 在 join base_dir 后不会通过 ../ 逃逸出 base_dir。

    Returns:
        bool: True 表示安全（路径在 base_dir 内），False 表示路径逃逸。
    """
    base_dir_resolved = os.path.realpath(base_dir)
    path_resolved = os.path.realpath(os.path.join(base_dir, relative_path))
    return os.path.commonpath([base_dir_resolved, path_resolved]) == base_dir_resolved


# 模块级路径常量，供 generate-book-article.py 引用
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(SCRIPT_DIR, "capsule-registry.json")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "bookshelf-template.html")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "bookshelf.html")


def load_template(template_path):
    """加载 HTML 模板"""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def load_registry(registry_path):
    """加载胶囊注册表"""
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_capsule_cards(capsules):
    """为每本胶囊构建书架卡片 HTML，索引从 0 开始，整卡可点击内嵌阅读"""
    cards_html = []
    for i, cap in enumerate(capsules):
        card = f"""<div onclick="openCapsule({i})" style="background:linear-gradient(to right,#FFFDF7 50%,#D9C2A0 50%);border-radius:40px;padding:20px 24px;margin-bottom:20px;box-shadow:0 2px 16px rgba(0,0,0,0.04),0 6px 24px rgba(180,150,110,0.06);border:1px solid rgba(196,168,130,0.08);text-align:left;position:relative;cursor:pointer;transition:all 0.2s;display:flex;gap:0;" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.08),0 8px 28px rgba(180,150,110,0.12)';this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='0 2px 16px rgba(0,0,0,0.04),0 6px 24px rgba(180,150,110,0.06)';this.style.transform='translateY(0)'">
  <!-- 胶囊左右分割线 -->
  <div style="position:absolute;top:0;left:50%;width:1px;bottom:0;background:rgba(196,168,130,0.3);"></div>
  <!-- 左侧：序号+书名+作者+按钮 -->
  <div style="flex:0 0 50%;padding-right:20px;display:flex;align-items:center;">
    <div>
      <div style="font-size:11px;color:#9E8E7D;margin-bottom:8px;">No.{i + 1}</div>
      <div style="font-size:18px;font-weight:bold;color:#3A2E2A;margin-bottom:4px;">{cap["book_title"]}</div>
      <div style="font-size:12px;color:#A89888;margin-bottom:16px;">{cap["author"]} · {cap["date_generated"]}</div>
      <div style="display:inline-block;padding:8px 20px;background:linear-gradient(135deg,#C4A882,#8B6F50);color:#FFF;border-radius:20px;font-size:13px;letter-spacing:1px;">点击阅读</div>
    </div>
  </div>
  <!-- 右侧：金句描述 -->
  <div style="flex:0 0 50%;padding-left:0;display:flex;align-items:center;">
    <div style="font-size:14px;color:#4A3B30;line-height:1.8;padding-left:2px;border-left:3px solid #C4A882;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;">"{cap["cover_line"]}"</div>
  </div>
</div>"""
        cards_html.append(card)
    return "\n".join(cards_html)


def generate_bookshelf(registry_path, template_path, output_path):
    """主流程：生成书架 HTML"""
    base_dir = os.path.dirname(os.path.abspath(registry_path))

    registry = load_registry(registry_path)
    template = load_template(template_path)

    capsules = registry.get("capsules", [])
    stats = registry.get("stats", {})

    # 构建卡片 HTML
    cards_block = build_capsule_cards(capsules)

    # 读取每颗胶囊 HTML，提取 body 内容嵌入书架
    capsule_contents = []
    for i, cap in enumerate(capsules):
        html_path_abs = os.path.join(base_dir, cap["html_path"])
        if not _is_path_safe(base_dir, cap["html_path"]):
            print(f"WARN: 胶囊文件路径不安全，已跳过: {cap['html_path']}", file=sys.stderr)
            capsule_contents.append(
                f'<div id="capsule-{i}"><p style="color:#999;">胶囊文件路径不安全，已跳过</p></div>'
            )
        elif os.path.exists(html_path_abs):
            with open(html_path_abs, "r", encoding="utf-8") as f:
                body_html = f.read()
            body_start = body_html.find("<body")
            body_end = body_html.find("</body>")
            if body_start != -1 and body_end != -1:
                inner_start = body_html.find(">", body_start) + 1
                body_content = body_html[inner_start:body_end].strip()
            else:
                body_content = body_html
            capsule_contents.append(f'<div id="capsule-{i}">{body_content}</div>')
        else:
            capsule_contents.append(f'<div id="capsule-{i}"><p style="color:#999;">胶囊文件未找到</p></div>')
    capsule_store = "\n".join(capsule_contents)

    # 占位符替换
    html = template.replace("{{BOOKSHELF_TITLE}}", registry.get("bookshelf_title", "胶囊书架"))
    html = html.replace("{{BOOKSHELF_SUBTITLE}}", registry.get("bookshelf_subtitle", ""))
    html = html.replace("{{TOTAL_BOOKS}}", str(stats.get("total_books", len(capsules))))
    html = html.replace("{{TOTAL_AUTHORS}}", str(stats.get("total_authors", len(set(c["author"] for c in capsules)))))
    html = html.replace("{{LAST_UPDATED}}", stats.get("last_updated", datetime.now().strftime("%Y-%m-%d")))
    html = html.replace("{{GENERATE_DATE}}", datetime.now().strftime("%Y-%m-%d"))
    html = html.replace("{{CAPSULE_CONTENTS}}", capsule_store)

    # 替换卡片循环块
    html = html.replace("{{#each CAPSULES}}", "<!-- CAPSULE CARDS START -->")
    html = html.replace("{{/each}}", "<!-- CAPSULE CARDS END -->")

    # 在卡片区插入实际卡片
    start = html.find("<!-- CAPSULE CARDS START -->")
    end = html.find("<!-- CAPSULE CARDS END -->")
    if start != -1 and end != -1:
        html = html[:start] + cards_block + html[end + len("<!-- CAPSULE CARDS END -->"):]

    # 写入输出
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"书架已生成 → {output_path}")
    print(f"共收录 {len(capsules)} 本书")
    return output_path


def update_registry_stats(registry_path):
    """自动更新注册表统计字段"""
    registry = load_registry(registry_path)
    capsules = registry.get("capsules", [])

    authors = set(c["author"] for c in capsules)
    registry["stats"] = {
        "total_books": len(capsules),
        "total_authors": len(authors),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def register_capsule(registry_path, book_title, author, html_path, cover_line):
    """将新胶囊注册到书架。已存在则更新日期和路径。"""
    if not _is_path_safe(os.path.dirname(registry_path), html_path):
        raise ValueError(f"html_path 路径不安全，拒绝注册: {html_path}")

    registry = load_registry(registry_path)
    capsules = registry.get("capsules", [])

    # 查找是否已注册（按书名匹配）
    found = False
    for cap in capsules:
        if cap["book_title"] == book_title:
            cap["html_path"] = html_path
            cap["date_generated"] = datetime.now().strftime("%Y-%m-%d")
            cap["cover_line"] = cover_line
            found = True
            break

    if not found:
        capsules.append({
            "book_title": book_title,
            "author": author,
            "date_generated": datetime.now().strftime("%Y-%m-%d"),
            "html_path": html_path,
            "cover_line": cover_line
        })

    registry["capsules"] = capsules
    update_registry_stats(registry_path)

    # 写入
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    print(f"已注册 → {book_title}（{'更新' if found else '新增'}）")


# ---------- CLI ----------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 默认：更新统计 + 生成书架
        update_registry_stats(REGISTRY_PATH)
        generate_bookshelf(REGISTRY_PATH, TEMPLATE_PATH, OUTPUT_PATH)
    elif sys.argv[1] == "register":
        # python generate-bookshelf.py register "书名" "作者" "html路径" "金句"
        if len(sys.argv) == 6:
            register_capsule(REGISTRY_PATH, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            generate_bookshelf(REGISTRY_PATH, TEMPLATE_PATH, OUTPUT_PATH)
        else:
            print("用法: python generate-bookshelf.py register <书名> <作者> <html路径> <金句>")
    elif sys.argv[1] == "--help":
        print("书架生成器")
        print("  python generate-bookshelf.py                          更新统计并生成书架")
        print("  python generate-bookshelf.py register <书名> <作者> <html路径> <金句>  注册新书并生成书架")
    else:
        print("未知命令，使用 --help 查看用法")
