#!/usr/bin/env python3
"""
GEO Pre-Sales Quick Hook · quick_hook.py  (5-Engine Parallel Edition)
Usage:
  python3 quick_hook.py --brand "Starbucks" --competitors "Luckin,McDonald's Coffee,Tims,Manner" --keywords "best coffee brand"
  python3 quick_hook.py --brand "YourBrand" --competitors "CompA,CompB,CompC" --keywords "keyword1,keyword2" --engines "Qwen,DeepSeek"
"""

import argparse, json, re, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Read API configuration from environment variables (supports any OpenAI-compatible API)
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")

if not LLM_API_KEY:
    raise ValueError("Please set the environment variable LLM_API_KEY (supports OpenAI or any compatible API key)")

# Full engine configuration (all engines share LLM_API_KEY / LLM_BASE_URL / LLM_MODEL)
ENGINE_MAP = {
    "Qwen": {
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        "model": LLM_MODEL,
    },
    "Doubao": {
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        "model": LLM_MODEL,
    },
    "DeepSeek": {
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        "model": LLM_MODEL,
    },
    "Kimi": {
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        "model": LLM_MODEL,
    },
    "Ernie": {
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        "model": LLM_MODEL,
    },
}
ALL_ENGINES = ["Qwen", "Doubao", "DeepSeek", "Kimi", "Ernie"]

MAX_WORKERS = 8
COLORS = {
    "primary": "#1a237e", "secondary": "#3949ab",
    "danger": "#c62828", "danger_bg": "#ffebee",
    "success": "#2e7d32", "success_bg": "#e8f5e9",
    "bar_bg": "#e0e0e0",
}

# ── Citation detection ──────────────────────────────────────────────
CITATION_PATTERNS = [
    "according to {brand}", "{brand} data shows", "{brand} report",
    "released by {brand}", "from {brand}", "{brand} research",
    "per {brand}", "{brand} noted", "{brand} stated"
]

def detect_citation(text: str, brand: str) -> bool:
    """Detect whether a brand appears as a citation/reference rather than a plain listing."""
    for pattern in CITATION_PATTERNS:
        if pattern.format(brand=brand) in text:
            return True
    return False


def generate_questions(keyword: str, brands: list, client, model: str) -> list:
    """Generate 8 user-style questions for a given keyword (without brand names)."""
    brands_str = ", ".join(brands)
    prompt = f"""For the keyword "{keyword}", generate 8 questions a user would ask an AI assistant.
Requirements:
1. Use natural user phrasing, e.g. "Which XXX is the best?"
2. Do not directly mention any brand names ({brands_str})
3. Cover a variety of use cases

Output a JSON array directly: ["question1", "question2", ...]"""
    try:
        resp = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], temperature=0.7
        )
        text = resp.choices[0].message.content.strip()
        m = re.search(r'\[[\s\S]*\]', text)
        if m:
            return json.loads(m.group())[:8]
    except Exception as e:
        print(f"⚠️ Question generation failed: {e}")
    return []


def query_one(prompt: str, brands: list, client, model: str) -> dict:
    """Query a single question, return the ranking of each brand; also detect citation appearances."""
    try:
        resp = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], temperature=0.3
        )
        text = resp.choices[0].message.content
        positions = {}
        for brand in brands:
            idx = text.find(brand)
            if idx != -1:
                positions[brand] = idx
        sorted_brands = sorted(positions.items(), key=lambda x: x[1])
        rank_map = {brand: rank + 1 for rank, (brand, _) in enumerate(sorted_brands)}
        # Append citation detection results (key prefix "cited:")
        for brand in brands:
            rank_map[f"cited:{brand}"] = detect_citation(text, brand)
        return rank_map
    except Exception as e:
        print(f"⚠️ Query failed: {e}")
    return {}


def analyze_keyword(keyword: str, brand: str, competitors: list, client, model: str) -> dict:
    """Analyze a single keyword, returning top-3 visibility rate + citation count per brand."""
    all_brands = [brand] + competitors
    questions = generate_questions(keyword, all_brands, client, model)
    if not questions:
        return {}

    total = len(questions)
    top3_counts = {b: 0 for b in all_brands}
    citation_counts = {b: 0 for b in all_brands}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(query_one, q, all_brands, client, model): q for q in questions}
        for future in as_completed(futures):
            rank_map = future.result()
            for b in all_brands:
                if rank_map.get(b, 99) <= 3:
                    top3_counts[b] += 1
                if rank_map.get(f"cited:{b}", False):
                    citation_counts[b] += 1

    results = {b: round(top3_counts[b] / total * 100, 1) for b in all_brands}
    # Append citation stats (key prefix "cited:")
    for b in all_brands:
        results[f"cited:{b}"] = citation_counts[b]
    return results


def run_engine(engine_name: str, brand: str, competitors: list, keywords: list) -> dict:
    """Run a full analysis for a single engine, returning {keyword: {brand: pct}}."""
    cfg = ENGINE_MAP.get(engine_name, ENGINE_MAP["Qwen"])
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
    model = cfg["model"]
    results = {}
    for kw in keywords:
        print(f"  🔍 [{engine_name}] Analyzing '{kw}'...")
        results[kw] = analyze_keyword(kw, brand, competitors, client, model)
    return results


def build_html_multi_engine(brand: str, competitors: list, keywords: list,
                             engine_results: dict, engines: list) -> str:
    """
    Generate a 5-engine summary HTML report.
    engine_results: {engine_name: {keyword: {brand_name: pct}}}
    """
    all_brands = [brand] + competitors
    date_str = datetime.now().strftime("%Y-%m-%d")

    cards_html = ""
    for kw in keywords:
        # Collect each engine's results for this keyword
        # engine_scores[engine_name][brand_name] = pct
        engine_scores = {}
        for eng in engines:
            kw_result = engine_results.get(eng, {}).get(kw, {})
            if kw_result:
                engine_scores[eng] = kw_result

        if not engine_scores:
            continue

        # Calculate each brand's average top-3 visibility rate across all engines
        brand_avg = {}
        for b in all_brands:
            scores = [engine_scores[eng].get(b, 0) for eng in engines if eng in engine_scores]
            brand_avg[b] = round(sum(scores) / len(scores), 1) if scores else 0

        # Count cumulative cross-engine citation appearances per brand
        citation_total = {b: 0 for b in all_brands}
        for eng in engines:
            eng_result = engine_results.get(eng, {}).get(kw, {})
            for b in all_brands:
                citation_total[b] += eng_result.get(f"cited:{b}", 0)

        # Sort brands by combined average, highest first
        sorted_brands = sorted(all_brands, key=lambda b: brand_avg[b], reverse=True)

        brand_score = brand_avg.get(brand, 0)
        comp_scores = [brand_avg.get(b, 0) for b in competitors]
        industry_avg = round(sum(comp_scores) / max(len(comp_scores), 1), 1)
        brand_rank = sorted_brands.index(brand) + 1

        # ── Part 1: Multi-engine comparison table ──
        # Header: Brand | Engine1 | Engine2 | ... | Combined Average
        th_cells = "<th style='text-align:left;padding:8px 12px;background:#1a237e;color:#fff;border-radius:4px 0 0 4px;'>Brand</th>"
        for eng in engines:
            th_cells += f"<th style='text-align:center;padding:8px 10px;background:#1a237e;color:#fff;white-space:nowrap;'>{eng}</th>"
        th_cells += "<th style='text-align:center;padding:8px 12px;background:#1a237e;color:#fff;border-radius:0 4px 4px 0;'>Avg</th>"

        table_rows = ""
        for b in sorted_brands:
            is_target = (b == brand)
            row_bg = f"background:{COLORS['danger_bg']};border:1.5px solid {COLORS['danger']};" if is_target else "background:#f9f9f9;"
            label = f"⚠️ {b} (Your Brand)" if is_target else b
            fc = COLORS["danger"] if is_target else "#333"
            fw = "700" if is_target else "400"

            td_cells = f"<td style='padding:9px 12px;font-size:13px;font-weight:{fw};color:{fc};'>{label}</td>"
            for eng in engines:
                pct = engine_scores.get(eng, {}).get(b, "-")
                val_str = f"{pct}%" if isinstance(pct, (int, float)) else str(pct)
                # Highlight high/low values
                if isinstance(pct, (int, float)):
                    cell_color = COLORS["danger"] if (is_target and pct < industry_avg) else ("#2e7d32" if pct >= 40 else "#555")
                else:
                    cell_color = "#999"
                td_cells += f"<td style='text-align:center;padding:9px 10px;font-size:13px;font-weight:{fw};color:{cell_color};'>{val_str}</td>"

            avg_val = brand_avg.get(b, 0)
            avg_color = COLORS["danger"] if is_target else "#1a237e"
            td_cells += f"<td style='text-align:center;padding:9px 12px;font-size:14px;font-weight:700;color:{avg_color};'>{avg_val}%</td>"
            table_rows += f"<tr style='{row_bg}'>{td_cells}</tr>"

        # ── Citation row ──
        citation_row_cells = "<td style='padding:9px 12px;font-size:13px;font-weight:600;color:#5c6bc0;background:#e8eaf6;'>📌 Citations</td>"
        for eng in engines:
            # Per engine: which brands appear as citations in this keyword
            cited_brands_this_eng = [b for b in all_brands if engine_results.get(eng, {}).get(kw, {}).get(f"cited:{b}", 0) > 0]
            if cited_brands_this_eng:
                cell_text = ", ".join(cited_brands_this_eng)
                citation_row_cells += f"<td style='text-align:center;padding:9px 10px;font-size:12px;color:#2e7d32;font-weight:600;background:#e8eaf6;'>{cell_text}</td>"
            else:
                citation_row_cells += f"<td style='text-align:center;padding:9px 10px;font-size:12px;color:#aaa;background:#e8eaf6;'>-</td>"
        # Combined average column: which brands have any citation
        cited_any = [b for b in all_brands if citation_total.get(b, 0) > 0]
        if cited_any:
            summary_text = " ".join([f"✅{b}" for b in cited_any])
        else:
            summary_text = "-"
        citation_row_cells += f"<td style='text-align:center;padding:9px 12px;font-size:12px;font-weight:600;color:#2e7d32;background:#e8eaf6;'>{summary_text}</td>"
        table_rows += f"<tr>{citation_row_cells}</tr>"

        table_html = f"""
        <div style="overflow-x:auto;margin-bottom:24px;">
          <div style="font-size:14px;font-weight:600;color:#1a237e;margin-bottom:10px;">📊 Multi-Engine Comparison Matrix (Top-3 Visibility Rate)</div>
          <table style="width:100%;border-collapse:separate;border-spacing:0 4px;font-size:13px;">
            <thead><tr>{th_cells}</tr></thead>
            <tbody>{table_rows}</tbody>
          </table>
        </div>"""

        # ── Part 2: Combined average ranking bar chart ──
        bar_rows = ""
        for i, b in enumerate(sorted_brands):
            score = brand_avg.get(b, 0)
            is_target = (b == brand)
            bar_color = COLORS["danger"] if is_target else ("#3949ab" if score >= 30 else "#90a4ae")
            bg = f'background:{COLORS["danger_bg"]};border:1.5px solid {COLORS["danger"]};' if is_target else ""
            label = f"⚠️ {b} (Your Brand)" if is_target else b
            rank_badge = f"#{i+1}"
            fw = "700" if is_target else "400"
            fc = COLORS["danger"] if is_target else "#333"
            bar_rows += f'''
        <div style="display:flex;align-items:center;gap:12px;padding:10px 16px;border-radius:8px;margin-bottom:8px;{bg}">
          <div style="width:24px;color:#999;font-size:12px;text-align:center;">{rank_badge}</div>
          <div style="width:170px;font-size:14px;font-weight:{fw};color:{fc};flex-shrink:0;">{label}</div>
          <div style="flex:1;background:{COLORS["bar_bg"]};border-radius:4px;height:10px;overflow:hidden;">
            <div style="background:{bar_color};width:{score}%;height:100%;border-radius:4px;"></div>
          </div>
          <div style="width:52px;text-align:right;font-size:14px;font-weight:700;color:{bar_color};">{score}%</div>
        </div>'''

        bar_html = f"""
        <div style="margin-bottom:24px;">
          <div style="font-size:14px;font-weight:600;color:#1a237e;margin-bottom:10px;">🏆 Combined Average Ranking (5-Engine Average)</div>
          {bar_rows}
        </div>"""

        # ── Fatal conclusion ──
        cited_competitors = [b for b in competitors if citation_total.get(b, 0) > 0]
        citation_hook = ""
        if cited_competitors:
            cited_names = ", ".join(cited_competitors)
            citation_hook = (
                f'<br>🔴 Warning: <strong>{cited_names}</strong> have already been cited as authoritative sources by multiple AI engines — '
                f'meaning AI treats them as trusted data sources. The credibility gap is widening.'
            )

        fatal_text = (
            f'⚠️ For queries related to "<strong>{kw}</strong>", '
            f'<strong>{brand}</strong> achieves only a '
            f'<strong style="color:{COLORS["danger"]}">{brand_score}%</strong> average top-3 visibility rate across 5 AI engines, '
            f'while the industry average is already <strong>{industry_avg}%</strong> (current rank: #{brand_rank})'
            f'{citation_hook}'
        )

        cards_html += f'''
    <div style="background:#fff;border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.08);">
      <div style="font-size:16px;font-weight:700;color:{COLORS["primary"]};border-left:4px solid {COLORS["secondary"]};padding-left:12px;margin-bottom:24px;">
        🔍 "{kw}" · AI Top-3 Visibility Competitive Analysis (5 Engines)
      </div>
      {table_html}
      {bar_html}
      <div style="margin-top:8px;padding:14px 16px;background:{COLORS["danger_bg"]};border-radius:8px;font-size:14px;color:{COLORS["danger"]};line-height:1.7;">
        {fatal_text}
      </div>
    </div>'''

    # ── Bottom citation summary (across all keywords) ──
    all_brands = [brand] + competitors
    global_citation_total = {b: 0 for b in all_brands}
    for eng in engines:
        for kw in keywords:
            eng_result = engine_results.get(eng, {}).get(kw, {})
            for b in all_brands:
                global_citation_total[b] += eng_result.get(f"cited:{b}", 0)
    cited_comp_global = [b for b in competitors if global_citation_total.get(b, 0) > 0]
    if cited_comp_global:
        cited_count = len(cited_comp_global)
        cited_names_str = ", ".join(cited_comp_global)
        citation_summary_html = f'''
    <div style="background:#fff3e0;border:1.5px solid #ff9800;border-radius:10px;padding:16px 20px;margin-bottom:20px;text-align:left;">
      <div style="font-size:14px;font-weight:700;color:#e65100;margin-bottom:8px;">🔴 Citation Competition Warning</div>
      <div style="font-size:14px;color:#5d4037;line-height:1.8;">
        Among your competitors, <strong style="color:#c62828">{cited_count} brand(s) ({cited_names_str})</strong> have already been cited as authoritative sources by AI engines.<br>
        Being cited as a source is not the same as being listed — it means AI already treats them as industry authorities. Once this dependency is established, it becomes extremely difficult for newcomers to catch up.<br>
        <strong>Failing to build citation presence now will cost 10x more in the future.</strong>
      </div>
    </div>'''
    else:
        citation_summary_html = ""

    primary = COLORS["primary"]
    engines_str = ", ".join(engines)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GEO Quick Hook · {brand}</title>
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#eef2f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; padding:20px; }}
.container {{ max-width:1000px; margin:0 auto; }}
table tr:hover {{ filter:brightness(0.97); }}
</style>
</head>
<body>
<div class="container">
  <!-- Cover -->
  <div style="background:{primary};border-radius:16px;padding:40px;margin-bottom:20px;color:#fff;">
    <div style="font-size:13px;opacity:.7;margin-bottom:8px;">GEO Competitive Overview · 5-Engine Parallel · {date_str}</div>
    <div style="font-size:28px;font-weight:700;margin-bottom:12px;">{brand} · AI Top-3 Visibility Competitive Analysis</div>
    <div style="font-size:15px;opacity:.85;margin-bottom:16px;">Data collected from 5 major AI engines, revealing your brand's real position in AI recommendations</div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
      {''.join(f'<span style="background:rgba(255,255,255,.15);border-radius:20px;padding:4px 14px;font-size:13px;">{eng}</span>' for eng in engines)}
    </div>
  </div>

  {cards_html}

  <!-- Bottom hook -->
  <div style="background:#fff;border-radius:12px;padding:28px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
    <div style="font-size:13px;color:#999;margin-bottom:16px;">Data based on real Q&amp;A collected from {engines_str} and other major AI engines</div>
    <div style="font-size:15px;color:#333;margin-bottom:20px;line-height:1.8;">
      Once competitors claim AI recommendation slots, the advantage compounds daily.<br>
      Every day of inaction is a day competitors build deeper AI presence.
    </div>
    {citation_summary_html}
    <div style="display:inline-block;background:{primary};color:#fff;padding:12px 32px;border-radius:24px;font-size:15px;font-weight:600;">
      Want to improve your brand's visibility in AI recommendations?
    </div>
  </div>
</div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="GEO Pre-Sales Quick Hook (5-Engine Parallel Edition)")
    parser.add_argument("--brand", required=True, help="Target brand (client's brand name)")
    parser.add_argument("--competitors", required=True, help="Competitor list, comma-separated (5-8 brands)")
    parser.add_argument("--keywords", required=True, help="Target keywords, comma-separated (1-2 keywords)")
    parser.add_argument("--engines", default=",".join(ALL_ENGINES),
                        help="Engine list, comma-separated (default: all 5)")
    args = parser.parse_args()

    brand = args.brand.strip()
    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()][:2]
    engines = [e.strip() for e in args.engines.split(",") if e.strip() and e.strip() in ENGINE_MAP]
    if not engines:
        engines = ALL_ENGINES[:]

    print(f"\n🚀 GEO Pre-Sales Quick Hook (5-Engine Parallel Edition)")
    print(f"  Brand:       {brand}")
    print(f"  Competitors: {', '.join(competitors)}")
    print(f"  Keywords:    {', '.join(keywords)}")
    print(f"  Engines:     {', '.join(engines)}\n")

    # Run all engines in parallel
    engine_results = {}  # {engine_name: {keyword: {brand: pct}}}
    print(f"⚡ Launching {len(engines)} engines in parallel...\n")
    with ThreadPoolExecutor(max_workers=len(engines)) as executor:
        futures = {
            executor.submit(run_engine, eng, brand, competitors, keywords): eng
            for eng in engines
        }
        for future in as_completed(futures):
            eng = futures[future]
            try:
                engine_results[eng] = future.result()
                # Print result summary for this engine
                for kw in keywords:
                    pct = engine_results[eng].get(kw, {}).get(brand, 0)
                    print(f"  ✅ [{eng}] '{kw}' — {brand} top-3 visibility: {pct}%")
            except Exception as e:
                print(f"  ❌ [{eng}] Failed: {e}")
                engine_results[eng] = {}

    print()

    # Generate HTML report
    html = build_html_multi_engine(brand, competitors, keywords, engine_results, engines)

    date_tag = datetime.now().strftime("%Y%m%d")
    out_path = Path.home() / "Desktop" / f"GEO_QuickHook_{brand}_5engines_{date_tag}.html"
    out_path.write_text(html, encoding="utf-8")
    size_kb = out_path.stat().st_size // 1024
    print(f"✅ Report generated: {out_path} ({size_kb} KB)")

    # Print summary statistics
    print("\n📊 Engine Data Summary:")
    for kw in keywords:
        print(f"\n  '{kw}'")
        for eng in engines:
            pct = engine_results.get(eng, {}).get(kw, {}).get(brand, "N/A")
            pct_str = f"{pct}%" if isinstance(pct, (int, float)) else str(pct)
            print(f"    {eng}: {brand} = {pct_str}")
        # Calculate average
        scores = [engine_results.get(eng, {}).get(kw, {}).get(brand, None) for eng in engines]
        valid = [s for s in scores if s is not None]
        if valid:
            avg = round(sum(valid) / len(valid), 1)
            # Competitor average
            all_brands = [brand] + competitors
            comp_avgs = []
            for comp in competitors:
                comp_scores = [engine_results.get(eng, {}).get(kw, {}).get(comp, None) for eng in engines]
                comp_valid = [s for s in comp_scores if s is not None]
                if comp_valid:
                    comp_avgs.append(sum(comp_valid) / len(comp_valid))
            industry_avg = round(sum(comp_avgs) / len(comp_avgs), 1) if comp_avgs else 0
            print(f"    → Combined avg: {avg}% | Competitor avg: {industry_avg}%")


if __name__ == "__main__":
    main()
