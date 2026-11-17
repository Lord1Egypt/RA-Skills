#!/usr/bin/env python3
"""
booklist_generator.py — 主題書單生成器
根據場景（求職/創業/寫作/育兒…）自動生成結構化書單
包含：閱讀順序指引、必讀/選讀標記、難度星級、摘要一句話
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
import re
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".bookshelf-plus" / "recommendations"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = DATA_DIR / "booklists"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ── 主題書單資料庫（內建）───────────────────────────────────────────────────

BUILT_IN_LISTS: dict[str, dict] = {
    "startup": {
        "title": "🚀 創業必讀書單",
        "subtitle": "從 0 到 1 的必備知識地圖",
        "category": "商業",
        "books": [
            {"title": "Zero to One", "author": "Peter Thiel",
             "why": "重新思考創新：從 0 到 1 才是真正的創造",
             "难度": 3, "required": True},
            {"title": "The Lean Startup", "author": "Eric Ries",
             "why": "最小可行產品、快速驗證、持續迭代的核心方法論",
             "难度": 2, "required": True},
            {"title": "Hard Things About Hard Things", "author": "Ben Horowitz",
             "why": "創業維艱，沒有捷徑，只有真實經驗",
             "难度": 3, "required": False},
            {"title": "The Harder Thing", "author": "Daniel Harkavy",
             "why": "把事業看成一支球隊，建立取勝文化",
             "难度": 2, "required": False},
            {"title": "Inspired", "author": "Marty Cagan",
             "why": "頂尖產品團隊如何打造用戶願意付費的產品",
             "难度": 3, "required": True},
        ],
    },
    "writing": {
        "title": "✍️ 寫作修煉書單",
        "subtitle": "從文字新手到專業作者的階梯",
        "category": "寫作",
        "books": [
            {"title": "On Writing Well", "author": "William Zinsser",
             "why": "英語非虛構寫作經典，中文作者同樣適用",
             "难度": 2, "required": True},
            {"title": "The Elements of Style", "author": "Strunk & White",
             "why": "簡潔寫作的聖經，每句話都該問：是否必要？",
             "难度": 1, "required": True},
            {"title": "Story", "author": "Robert McKee",
             "why": "敘事結構的深度解析，影視/小說/商業報告都適用",
             "难度": 4, "required": False},
            {"title": "Draft No. 4", "author": "John McPhee",
             "why": "《紐約客》傳奇記者的寫作心法",
             "难度": 2, "required": False},
            {"title": "Writing Tools", "author": "Roy Peter Clark",
             "why": "55 種具體可操作的寫作技巧",
             "难度": 1, "required": True},
        ],
    },
    "parenting": {
        "title": "👶 育兒成長書單",
        "subtitle": "理解孩子，也理解自己",
        "category": "家庭",
        "books": [
            {"title": "正面管教", "author": "Jane Nelsen",
             "why": "和善而堅定：不懲罰、不溺愛的有效教養",
             "难度": 2, "required": True},
            {"title": "父母的語言", "author": "Dana Suskind",
             "why": "3000 萬字差異：父母的語言如何塑造孩子的大腦",
             "难度": 2, "required": True},
            {"title": "全齡家人的自在相處", "author": "王浩一",
             "why": "以華人家庭為本的心理學視角",
             "难度": 1, "required": False},
            {"title": "孩子如何學會說故事", "author": "Jerome Bruner",
             "why": "認知科學視角：敘事思維如何影響學習",
             "难度": 3, "required": False},
        ],
    },
    "thinking": {
        "title": "🧠 思考力書單",
        "subtitle": "升級認知模型，避免思維盲區",
        "category": "思維",
        "books": [
            {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman",
             "why": "系統一/系統二：為何人們總是犯同樣的錯",
             "难度": 4, "required": True},
            {"title": "The Psychology of Intelligence", "author": "Jean Piaget",
             "why": "智力結構的經典理論",
             "难度": 3, "required": False},
            {"title": "批判性思考", "author": "Moore & Parker",
             "why": "如何避免邏輯謬誤、識別偽論證",
             "难度": 2, "required": True},
            {"title": "模型思維", "author": "Scott Page",
             "why": "24 種思考模型，用多視角理解複雜世界",
             "难度": 4, "required": False},
            {"title": "原則", "author": "Ray Dalio",
             "why": "建立一套演算法來做決策",
             "难度": 3, "required": False},
        ],
    },
    "career": {
        "title": "💼 求職與職涯書單",
        "subtitle": "找到方向，提升不可替代性",
        "category": "職涯",
        "books": [
            {"title": "The 2-Hour Job Search", "author": "Steve Dalton",
             "why": "用系統化的方式提升求職效率",
             "难度": 1, "required": True},
            {"title": "So Good They Can't Ignore You", "author": "Cal Newport",
             "why": "累積稀缺技能比追隨熱情更重要",
             "难度": 2, "required": True},
            {"title": "Deep Work", "author": "Cal Newport",
             "why": "如何在高干擾時代保持深度專注",
             "难度": 2, "required": False},
            {"title": "The Career Manifesto", "author": "Michael Streeter",
             "why": "81 個具體行動讓你重新思考職涯",
             "难度": 1, "required": False},
        ],
    },
    "investing": {
        "title": "📈 投資理財書單",
        "subtitle": "建立穩健的財富思維",
        "category": "理財",
        "books": [
            {"title": "The Intelligent Investor", "author": "Benjamin Graham",
             "why": "價值投資的聖經，長期主義者的指南",
             "难度": 4, "required": True},
            {"title": "A Random Walk Down Wall Street", "author": "Burton Malkiel",
             "why": "市場效率與指數化投資的經典論證",
             "难度": 3, "required": True},
            {"title": "The Psychology of Money", "author": "Morgan Housel",
             "why": "金錢的真正意義是什麼？財務決策背後的心理學",
             "难度": 1, "required": True},
            {"title": "巴菲特的投資哲學", "author": "Janet Lowe",
             "why": "理解股神的長期價值投資原則",
             "难度": 2, "required": False},
        ],
    },
    "philosophy": {
        "title": "🏛️ 哲學入門書單",
        "subtitle": "從蘇格拉底到現代思想的精華路徑",
        "category": "哲學",
        "books": [
            {"title": "哲學的40堂課", "author": "Ben Dupré",
             "why": "50+ 重要思想家的核心主張，一頁一個哲學家",
             "难度": 1, "required": True},
            {"title": "The Story of Philosophy", "author": "Will Durant",
             "why": "從柏拉圖到尼采，用敘事串起西方哲學史",
             "难度": 2, "required": False},
            {"title": "蘇菲的世界", "author": "Jostein Gaarder",
             "why": "以小說包裹的哲學史，適合零基礎讀者",
             "难度": 1, "required": True},
            {"title": "西方哲學史", "author": "羅素",
             "why": "大師筆下的哲學思想史，觀點犀利",
             "难度": 3, "required": False},
        ],
    },
    "science": {
        "title": "🔬 科普閱讀書單",
        "subtitle": "理解宇宙與生命的壯闊",
        "category": "科普",
        "books": [
            {"title": "宇宙的結構", "author": "Brian Greene",
             "why": "從量子到宇宙，物理學的最前沿敘事",
             "难度": 4, "required": True},
            {"title": "自私的基因", "author": "Richard Dawkins",
             "why": "用基因視角重新理解演化與生命",
             "难度": 3, "required": True},
            {"title": "從一到無窮大", "author": "George Gamow",
             "why": "用簡單語言解釋最深奧的科學概念",
             "难度": 2, "required": True},
            {"title": "萬物簡史", "author": "Bill Bryson",
             "why": "宇宙到生命的完整科學史，輕鬆好讀",
             "难度": 1, "required": False},
        ],
    },
}


# ── 網路補充搜尋 ───────────────────────────────────────────────────────────

def _web_search(query: str, limit: int = 3) -> list[dict]:
    """用 DuckDuckGo HTML 搜尋（無 API key）"""
    url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        # Extract snippets
        results = []
        for match in re.finditer(
            r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL
        ):
            snippet = re.sub(r"<[^>]+>", "", match.group(1)).strip()[:150]
            if snippet:
                results.append({"snippet": snippet})
                if len(results) >= limit:
                    break
        return results
    except Exception:
        return []


# ── 書單渲染 ───────────────────────────────────────────────────────────────

def _stars(n: int) -> str:
    return "⭐" * n


def render_booklist(data: dict, include_web: bool = False) -> str:
    title     = data.get("title", "未命名書單")
    subtitle  = data.get("subtitle", "")
    category  = data.get("category", "")
    books     = data.get("books", [])
    timestamp = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# {title}",
        "",
        f"**{subtitle}**  |  {category}  |  生成：{timestamp}",
        "",
        "---",
        "",
        "## 📖 閱讀順序指引",
        "",
    ]

    required = [b for b in books if b.get("required")]
    optional = [b for b in books if not b.get("required")]

    lines.append("### 🔴 必讀（按順序）")
    for i, b in enumerate(required, 1):
        stars = _stars(b.get("难度", 1))
        lines.extend([
            f"\n**{i}. 《{b['title']}》**  {stars}",
            f"   作者：{b.get('author','')}",
            f"   為什麼讀：{b.get('why','')}",
        ])

    if optional:
        lines.append("\n### ⚪ 選讀")
        for b in optional:
            stars = _stars(b.get("难度", 1))
            lines.extend([
                f"\n- 《{b['title']}》{stars}",
                f"  作者：{b.get('author','')} — {b.get('why','')}",
            ])

    # Web context
    if include_web and books:
        lines.append("\n---\n## 🌐 網路延伸閱讀\n")
        for b in books[:3]:
            query = f"{b['title']} {b.get('author','')} book summary"
            web = _web_search(query, 1)
            if web:
                snippet = web[0].get("snippet","")
                lines.append(f"- **{b['title']}**：{snippet}")
            else:
                lines.append(f"- **{b['title']}**：{b.get('why','')}")

    lines.extend([
        "\n---",
        "",
        f"_*Generated by QClaw Book Recommendation Engine · {timestamp}_*",
    ])
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="📚 主題書單生成器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list",    help="列出所有內建書單")
    p.add_argument("-s", "--search", help="關鍵字過濾")

    p = sub.add_parser("generate", help="生成書單")
    p.add_argument("topic", help="主題：startup / writing / parenting / thinking / career / investing / philosophy / science 或任意關鍵字")
    p.add_argument("-o", "--output", type=Path, help="輸出 Markdown 檔案")
    p.add_argument("--web", action="store_true", help="同時搜尋網路摘要")

    p = sub.add_parser("custom",  help="自訂書單（互動式）")
    p.add_argument("-t", "--title",    required=True)
    p.add_argument("-c", "--category")
    p.add_argument("-b", "--books", nargs="+",
                   help="書籍，格式：「書名|作者|一句話|難度|必讀」")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    if args.cmd == "list":
        topics = sorted(BUILT_IN_LISTS.keys())
        log(f"\n📚 內建書單（共 {len(topics)} 個主題）：\n")
        for key in topics:
            d  = BUILT_IN_LISTS[key]
            nb = len([b for b in d["books"] if b.get("required")])
            tb = len(d["books"])
            log(f"  {key:<15} {d['title']}（{nb}/{tb} 必讀）")

    elif args.cmd == "generate":
        topic_key = args.topic.lower().replace(" ", "_")
        # Exact match first
        data = BUILT_IN_LISTS.get(topic_key)
        if not data:
            # Keyword match
            for key, d in BUILT_IN_LISTS.items():
                if topic_key in key or topic_key in d.get("title","").lower():
                    data = d
                    break
        if not data:
            # Build a generic list
            data = {
                "title": f"🔍 主題書單：{args.topic}",
                "subtitle": "根據關鍵字生成",
                "category": "自訂",
                "books": [],
            }
            # Try web search
            if args.web:
                query = f"best books about {args.topic} reading list"
                web_results = _web_search(query, 5)
                for r in web_results:
                    data["books"].append({
                        "title": r.get("snippet","")[:60],
                        "author": "搜尋結果",
                        "why": r.get("snippet",""),
                        "难度": 2,
                        "required": False,
                    })

        output = render_booklist(data, include_web=args.web)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
            log(f"✅ 書單已儲存：{args.output}")
        else:
            log(output)

    elif args.cmd == "custom":
        books = []
        for entry in (args.books or []):
            parts = entry.split("|")
            books.append({
                "title":    parts[0].strip() if len(parts) > 0 else "未知",
                "author":   parts[1].strip() if len(parts) > 1 else "",
                "why":      parts[2].strip() if len(parts) > 2 else "",
                "难度":     int(parts[3].strip()) if len(parts) > 3 else 2,
                "required": (parts[4].strip().lower() == "true"
                            if len(parts) > 4 else False),
            })
        data = {
            "title":    args.title,
            "subtitle": "自訂書單",
            "category": args.category or "自訂",
            "books":    books,
        }
        output = render_booklist(data)
        log(output)


if __name__ == "__main__":
    main()
