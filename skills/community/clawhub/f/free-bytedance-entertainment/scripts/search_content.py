"""Unified local search across short dramas, novels, and comics."""
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(SKILL_DIR, "references", "content.json")

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def score(item, query):
    s = 0
    q = query.lower()
    for c in item.get("category", []):
        if q in c.lower():
            s += 3
    for t in item.get("tags", []):
        if q in t.lower():
            s += 2
    if q in item["title"].lower():
        s += 5
    if q in item.get("synopsis", "").lower():
        s += 1
    if q in item.get("author", "").lower():
        s += 2
    return s

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not query:
        print("Usage: python search_content.py <query>")
        sys.exit(0)

    db = load_db()
    results = []
    for item in db:
        s = score(item, query)
        if s > 0:
            results.append((s, item))

    results.sort(key=lambda x: x[0], reverse=True)

    for score_val, item in results[:10]:
        cat = item.get("category", [])
        cat_str = ", ".join(cat)
        kind_emoji = "🎬" if item.get("kind") == "drama" else ("🎨" if item.get("kind") == "comic" else "📖")
        print(f"{kind_emoji} 《{item['title']}》 [score={score_val}]")
        extra = f"  ✍️ {item['author']} |" if item.get("author") else ""
        eps = f"  📺 {item['episodes']}集" if item.get("episodes") else ""
        wc = f"  📊 {item.get('word_count', '')}" if item.get("word_count") else ""
        print(f"  {extra} 📂 {cat_str}{eps}{wc}")
        print(f"  📝 {item.get('synopsis', '')[:80]}...")
        print()
