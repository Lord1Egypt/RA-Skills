#!/usr/bin/env python3
"""Batch analyze multiple stocks and export results."""

import argparse, json, sys, os
from datetime import datetime

# Import from sibling modules
sys.path.insert(0, os.path.dirname(__file__))
from analyze import analyze
from score import score_stock

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/finance-radar/data")


def batch_analyze(tickers, output_format="table"):
    """Analyze multiple stocks at once."""
    results = []
    for ticker in tickers:
        try:
            data = analyze(ticker)
            price = data.get("price", 0)
            change = data.get("change_percent", 0)
            
            # Get score
            score_data = score_stock(ticker)
            rating = score_data.get("grade", "N/A")
            total = score_data.get("total", 0)
            
            results.append({
                "ticker": ticker,
                "name": data.get("name", ticker),
                "price": price,
                "change": change,
                "score": total,
                "rating": rating,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": str(e),
            })
    
    return {"count": len(results), "results": results}


def export_csv(data, filepath=None):
    """Export results to CSV."""
    if not filepath:
        filepath = os.path.join(OUTPUT_DIR, f"batch_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Ticker,Name,Price,Change%,Score,Rating\n")
        for r in data["results"]:
            if "error" not in r:
                f.write(f"{r['ticker']},{r['name']},{r['price']:.2f},{r['change']:.2f},{r['score']},{r['rating']}\n")
    
    return filepath


def format_output(data):
    lines = [f"📊 批量分析 ({data['count']} 只股票)", ""]
    lines.append(f"{'代码':<8} {'名称':<25} {'价格':>10} {'涨跌%':>8} {'评分':>6} {'评级':>4}")
    lines.append("-" * 65)
    
    for r in data["results"]:
        if "error" in r:
            lines.append(f"{r['ticker']:<8} ❌ 错误：{r['error'][:20]}")
        else:
            arrow = "🟢" if r["change"] >= 0 else "🔴"
            lines.append(f"{r['ticker']:<8} {r['name'][:25]:<25} {r['price']:>10.2f} {arrow}{r['change']:>7.2f} {r['score']:>6}/80 {r['rating']:>4}")
    
    lines.append("")
    lines.append(f"导出 CSV: python3 scripts/batch.py --tickers AAPL,GOOG --export")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tickers", required=True, help="Comma-separated tickers")
    p.add_argument("--export", action="store_true", help="Export to CSV")
    p.add_argument("--output", default=None, help="Output filepath")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    tickers = [t.strip().upper() for t in a.tickers.split(",")]
    data = batch_analyze(tickers)
    
    if a.export:
        path = export_csv(data, a.output)
        print(f"✅ 已导出：{path}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
