#!/usr/bin/env python3
"""
卡片式书摘文章生成器
基于 article-template.html 模板，根据 JSON 数据生成完整的微信兼容 HTML 文章。

用法：
    python generate-book-article.py <json_data_file> [output_html_path]

示例：
    python generate-book-article.py book-data-dongye.json output/dongye-article.html

纯 Python 标准库，零依赖，任何 Windows 直接跑。浏览器打开 HTML 后「打印 → 另存为 PDF」即可。

JSON 数据结构参见同目录下的 book-data-dongye.json（示例）。
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATE_PATH = SCRIPT_DIR / "article-template.html"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR

# 书架相关路径
REGISTRY_PATH = SCRIPT_DIR / "capsule-registry.json"
BOOKSHELF_TEMPLATE_PATH = SCRIPT_DIR / "bookshelf-template.html"
BOOKSHELF_OUTPUT_PATH = SCRIPT_DIR / "bookshelf.html"


# ============================================================
# 卡片 HTML 片段模板（与 article-template.html 中的卡片结构 1:1 一致）
# ============================================================

CARD_TEMPLATE = """<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="background-color:#F7F5F0;padding:28px 20px 24px 20px;">

      <p style="font-size:42px;font-weight:200;color:#E63946;text-align:center;line-height:1.0;padding:0;">{NUMBER}</p>
      <p style="font-size:18px;font-weight:700;color:#1A1A1A;text-align:center;line-height:1.4;padding:4px 0 4px 0;">{BOOK_TITLE}</p>
      <p style="font-size:12px;color:#999999;text-align:center;line-height:1.7;padding:0 0 0 0;">{BOOK_INFO}</p>

      <hr style="width:30px;border:none;border-top:1px solid #DDDDDD;">

{QUOTES}
    </td>
  </tr>
</table>"""

QUOTE_ITEM_TEMPLATE = """      <p style="font-size:15px;color:#444444;line-height:1.8;padding:12px 0 0 0;">
        <span style="font-size:12px;font-weight:700;color:#CCBBAA;">{INDEX} </span>{TEXT}
      </p>"""

QUOTE_SEPARATOR = '      <hr style="border:none;border-top:1px solid #E8E4DC;">'

GOLD_QUOTE_BLOCK_TEMPLATE = """<hr style="width:40px;border:none;border-top:2px solid #E63946;">
<p style="font-size:17px;font-weight:700;color:#222222;text-align:center;line-height:1.9;padding:10px 20px 0 20px;">{TEXT}</p>
<p style="font-size:12px;font-weight:400;color:#AAAAAA;text-align:center;line-height:1.5;padding:6px 0 10px 0;">{SOURCE}</p>"""

GOLD_QUOTE_BLOCK_NO_SOURCE_TEMPLATE = """<hr style="width:40px;border:none;border-top:2px solid #E63946;">
<p style="font-size:17px;font-weight:700;color:#222222;text-align:center;line-height:1.9;padding:10px 20px 0 20px;">{TEXT}</p>"""

CLOSING_QUOTE_BLOCK = """<hr style="width:40px;border:none;border-top:2px solid #E63946;">
<p style="font-size:17px;font-weight:700;color:#222222;text-align:center;line-height:1.9;padding:10px 20px 0 20px;">{TEXT}</p>
<p style="font-size:13px;font-weight:400;color:#AAAAAA;text-align:center;line-height:1.5;padding:6px 0 0 0;">{SOURCE}</p>"""


# ============================================================
# 核心函数
# ============================================================

def load_json(json_path: str) -> dict:
    """加载并验证 JSON 数据文件。"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 基本验证
    required_fields = ['date', 'title', 'subtitle', 'cards']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"JSON 缺少必填字段: {field}")

    if not isinstance(data['cards'], list) or len(data['cards']) == 0:
        raise ValueError("cards 必须是非空数组")

    return data


def build_card_html(card: dict) -> str:
    """为单张卡片生成 HTML。"""
    number = card.get('number', '')
    book_title = card.get('book_title', '')
    book_info = card.get('book_info', '')
    quotes = card.get('quotes', [])

    # 构建金句列表
    quote_parts = []
    for j, q in enumerate(quotes):
        idx = q.get('index', f'{j + 1:02d}')
        text = q.get('text', '')
        quote_parts.append(
            QUOTE_ITEM_TEMPLATE.replace('{INDEX}', idx).replace('{TEXT}', text)
        )
        if j < len(quotes) - 1:
            quote_parts.append(QUOTE_SEPARATOR)

    quotes_html = '\n'.join(quote_parts) if quote_parts else ''

    return (CARD_TEMPLATE
            .replace('{NUMBER}', number)
            .replace('{BOOK_TITLE}', book_title)
            .replace('{BOOK_INFO}', book_info)
            .replace('{QUOTES}', quotes_html))


def build_gold_quote_html(gq: dict) -> str:
    """为一条金句生成独立 HTML 块。"""
    text = gq.get('text', '')
    source = gq.get('source', '')
    if source:
        return GOLD_QUOTE_BLOCK_TEMPLATE.replace('{TEXT}', text).replace('{SOURCE}', source)
    else:
        return GOLD_QUOTE_BLOCK_NO_SOURCE_TEMPLATE.replace('{TEXT}', text)


def build_cards_section(cards: list, gold_quotes: list) -> str:
    """
    构建完整的卡片区 HTML，含金句穿插。

    金句穿插规则：
    - after_card=0：引言后、第一张卡片前 → 由 GOLD_QUOTE_1 占位符处理，不在此处
    - after_card=N (N>0)：卡片 N 之后、卡片 N+1 之前
      在数组中即 cards[N-1] 与 cards[N] 之间

    实现：遍历 cards，在渲染 cards[i] 前，检查是否有 after_card==i 的金句要插入。
    after_card==i 意味着该金句应出现在 cards[i-1] 之后、cards[i] 之前。
    """
    # 按 after_card 分组金句（排除 after_card=0 的，它由 GOLD_QUOTE_1 处理）
    gq_map = {}
    for gq in gold_quotes:
        after = gq.get('after_card', 0)
        if after == 0:
            continue  # 由 GOLD_QUOTE_1 占位符处理
        gq_map[after] = gq

    parts = []
    for i, card in enumerate(cards):
        # 在渲染 cards[i] 前，检查是否有 after_card==i 的金句
        # after_card==i 表示"卡片 i 之后"，即 cards[i-1] 与 cards[i] 之间
        # 所以应在 cards[i] 之前插入
        if i in gq_map:
            parts.append(build_gold_quote_html(gq_map[i]))

        parts.append(build_card_html(card))

        if i < len(cards) - 1:
            parts.append('<br>')

    # 检查是否有在所有卡片之后的金句（after_card == len(cards)）
    after_last = len(cards)
    if after_last in gq_map:
        parts.append('<br>')
        parts.append(build_gold_quote_html(gq_map[after_last]))

    return '\n'.join(parts)


def generate(data: dict, output_path: str) -> str:
    """主生成函数：读取模板、替换占位符、输出 HTML。"""
    # 读取模板
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # ============================================================
    # 1. 替换全局占位符
    # ============================================================

    html = html.replace('{{DATE}}', data.get('date', ''))

    # 标题（支持 title_line2 换行）
    cards = data.get('cards', [])
    gold_quotes = data.get('gold_quotes', [])
    total_quotes = sum(len(c.get('quotes', [])) for c in cards)      # 仅卡片内金句
    total_all_quotes = total_quotes + len(gold_quotes)                # 卡片金句 + 穿越金句
    total_cards = len(cards)

    title = data.get('title', '')
    if data.get('title_line2'):
        line2 = data['title_line2']
        # {count}=卡片数  {quotes}=卡片内金句  {all_quotes}=含穿越句的全部金句
        line2 = (line2
                 .replace('{count}', str(total_cards))
                 .replace('{all_quotes}', str(total_all_quotes))
                 .replace('{quotes}', str(total_quotes)))
        title += '<br>' + line2
    html = html.replace('{{TITLE}}', title)

    html = html.replace('{{SUBTITLE}}', data.get('subtitle', ''))

    # 引言段落
    intro = data.get('intro_paragraphs', [])
    html = html.replace('{{INTRO_PARAGRAPH_1}}', intro[0] if len(intro) > 0 else '')
    html = html.replace('{{INTRO_PARAGRAPH_2}}', intro[1] if len(intro) > 1 else '')

    # ============================================================
    # 2. 金句处理
    # ============================================================
    gold_quotes = data.get('gold_quotes', [])

    # GOLD_QUOTE_1：取 after_card==0 的金句
    gq_0 = next((gq for gq in gold_quotes if gq.get('after_card', -1) == 0), None)
    if gq_0:
        html = html.replace('{{GOLD_QUOTE_1}}', gq_0.get('text', ''))
        html = html.replace('{{GOLD_QUOTE_1_SOURCE}}', gq_0.get('source', ''))
    else:
        html = html.replace('{{GOLD_QUOTE_1}}', '')
        html = html.replace('{{GOLD_QUOTE_1_SOURCE}}', '')

    # 清理 GOLD_QUOTE_2 / GOLD_QUOTE_3 占位符（它们通过卡片穿插实现，模板中仅注释）
    for i in [2, 3]:
        html = html.replace(f'{{{{GOLD_QUOTE_{i}}}}}', '')
        html = html.replace(f'{{{{GOLD_QUOTE_{i}_SOURCE}}}}', '')

    # ============================================================
    # 3. 页脚
    # ============================================================
    html = html.replace('{{COLLECTION_TITLE}}', data.get('footer_collection_title', ''))

    # footer_subtitle：优先用 JSON 指定值；留空则自动生成
    footer_subtitle = data.get('footer_subtitle', '')
    if not footer_subtitle:
        footer_subtitle = f"{total_cards}张卡片 · {total_quotes}句精华"
    else:
        # {count}=卡片数  {quotes}=卡片内金句  {all_quotes}=含穿越句的全部金句
        footer_subtitle = (footer_subtitle
                           .replace('{count}', str(total_cards))
                           .replace('{all_quotes}', str(total_all_quotes))
                           .replace('{quotes}', str(total_quotes)))
    html = html.replace('{{FOOTER_SUBTITLE}}', footer_subtitle)

    # 结尾金句
    end_quote = data.get('footer_end_quote', {})
    html = html.replace('{{CLOSING_QUOTE}}', end_quote.get('text', ''))
    html = html.replace('{{CLOSING_QUOTE_SOURCE}}', end_quote.get('source', ''))

    # 页脚引用句：优先用 JSON 的 footer_quote 字段，否则用结尾金句完整文本
    footer_quote = data.get('footer_quote', '')
    if not footer_quote:
        footer_quote = end_quote.get('text', '')
    html = html.replace('{{FOOTER_QUOTE}}', f'"{footer_quote}"' if footer_quote else '')

    # ============================================================
    # 4. 构建卡片区（含穿插金句）并替换 {{#each CARDS}} 块
    # ============================================================
    cards = data.get('cards', [])
    cards_html = build_cards_section(cards, gold_quotes)

    # 替换 {{#each CARDS}}...{{/each}} 整个块
    # 使用深度计数正确匹配 {{/each}}，避免被内部嵌套的 {{#each QUOTES}}...{{/each}} 误导
    start_marker = '{{#each CARDS}}'
    end_marker = '{{/each}}'
    idx_start = html.find(start_marker)
    if idx_start != -1:
        pos = idx_start + len(start_marker)
        depth = 1
        search_from = pos
        while depth > 0:
            next_open = html.find('{{#each', search_from)
            next_close = html.find(end_marker, search_from)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                search_from = next_open + len('{{#each')
            else:
                depth -= 1
                if depth == 0:
                    pos = next_close
                    break
                search_from = next_close + len(end_marker)
        html = html[:idx_start] + cards_html + html[pos + len(end_marker):]

    # ============================================================
    # 5. 清理残留占位符（防止未替换的占位符留在输出中）
    # ============================================================
    html = re.sub(r'\{\{[A-Z_0-9]+\}\}', '', html)

    # ============================================================
    # 6. 写入输出文件（包裹完整 HTML 骨架 + charset 声明）
    # ============================================================
    html = f'<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=600">\n<title>{data.get("title", "")}</title>\n</head>\n<body style="margin:0;padding:0;">\n{html}\n</body>\n</html>'
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] 文章已生成: {output.resolve()}")
    print(f"     卡片 {len(cards)} 张 | 金句 {len(gold_quotes)} 条")

    return str(output.resolve())


# ============================================================
# 书架功能（内联，零外部依赖）
# ============================================================

def _load_registry():
    """加载胶囊注册表，不存在则返回默认结构"""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"bookshelf_title": "我的阅读书架", "bookshelf_subtitle": "每一颗胶囊，都是一次思维的沉淀", "capsules": [], "stats": {}}


def _save_registry(registry):
    """写入注册表"""
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def _register_capsule(book_title, author, html_path, cover_line):
    """将新胶囊注册到书架（去重更新）"""
    if not REGISTRY_PATH.parent.exists():
        return  # 书架模板不存在则跳过

    registry = _load_registry()
    capsules = registry.get("capsules", [])

    today = datetime.now().strftime("%Y-%m-%d")
    found = False
    for cap in capsules:
        if cap["book_title"] == book_title:
            cap["html_path"] = html_path
            cap["date_generated"] = today
            cap["cover_line"] = cover_line
            found = True
            break
    if not found:
        capsules.append({"book_title": book_title, "author": author, "date_generated": today, "html_path": html_path, "cover_line": cover_line})

    registry["capsules"] = capsules
    authors = set(c["author"] for c in capsules)
    registry["stats"] = {"total_books": len(capsules), "total_authors": len(authors), "last_updated": today}
    _save_registry(registry)


def _generate_bookshelf():
    """基于注册表和模板生成书架 HTML"""
    if not REGISTRY_PATH.exists() or not BOOKSHELF_TEMPLATE_PATH.exists():
        return

    registry = _load_registry()
    template = BOOKSHELF_TEMPLATE_PATH.read_text(encoding='utf-8')
    capsules = registry.get("capsules", [])
    stats = registry.get("stats", {})

    # 构建卡片 HTML（整张卡片可点击，内嵌阅读）
    cards_parts = []
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
        cards_parts.append(card)
    cards_block = "\n".join(cards_parts)

    # 读取每颗胶囊 HTML，提取 body 内容嵌入书架
    capsule_contents = []
    script_dir = SCRIPT_DIR
    for i, cap in enumerate(capsules):
        html_path_abs = script_dir / cap["html_path"]
        if html_path_abs.exists():
            body_html = html_path_abs.read_text(encoding='utf-8')
            # 提取 body 标签之间的内容
            body_start = body_html.find("<body")
            body_end = body_html.find("</body>")
            if body_start != -1 and body_end != -1:
                # 跳过 <body ...> 开标签
                inner_start = body_html.find(">", body_start) + 1
                body_content = body_html[inner_start:body_end].strip()
            else:
                body_content = body_html  # 兜底
            capsule_contents.append(f'<div id="capsule-{i}">{body_content}</div>')
        else:
            capsule_contents.append(f'<div id="capsule-{i}"><p style="color:#999;">胶囊文件未找到</p></div>')
    capsule_store = "\n".join(capsule_contents)

    # 占位符替换
    html = template.replace("{{BOOKSHELF_TITLE}}", registry.get("bookshelf_title", "胶囊书架"))
    html = html.replace("{{BOOKSHELF_SUBTITLE}}", registry.get("bookshelf_subtitle", ""))
    html = html.replace("{{TOTAL_BOOKS}}", str(stats.get("total_books", len(capsules))))
    html = html.replace("{{TOTAL_AUTHORS}}", str(stats.get("total_authors", 0)))
    html = html.replace("{{LAST_UPDATED}}", stats.get("last_updated", datetime.now().strftime("%Y-%m-%d")))
    html = html.replace("{{GENERATE_DATE}}", datetime.now().strftime("%Y-%m-%d"))
    html = html.replace("{{CAPSULE_CONTENTS}}", capsule_store)

    # 替换卡片循环块
    start_tag = "{{#each CAPSULES}}"
    end_tag = "{{/each}}"
    start = html.find(start_tag)
    end = html.find(end_tag)
    if start != -1 and end != -1:
        html = html[:start] + cards_block + html[end + len(end_tag):]

    BOOKSHELF_OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f"[书架] 已更新，共 {len(capsules)} 本书")


# ============================================================
# CLI 入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("用法: python generate-book-article.py <json_data_file> [output_html_path]")
        print("示例: python generate-book-article.py book-data-dongye.json output/dongye-article.html")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(
        DEFAULT_OUTPUT_DIR / (Path(json_path).stem + '-article.html')
    )

    try:
        data = load_json(json_path)
        html_path = generate(data, output_path)

        # 自动注册到书架并刷新
        gold_quotes = data.get("gold_quotes", [])
        cover_line = gold_quotes[0]["text"].replace("<br>", " ") if gold_quotes else ""
        book_title = data.get("title", Path(json_path).stem)
        author = data.get("author", book_title)
        rel_path = Path(os.path.relpath(html_path, SCRIPT_DIR)).as_posix()
        _register_capsule(book_title, author, rel_path, cover_line)
        _generate_bookshelf()

        print(f"[OK] HTML 已生成: {Path(html_path).resolve()}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
