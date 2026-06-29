"""
抖音创作者中心 - 可视化报告生成模块
基于回复结果数据生成交互式 HTML 分析报告。
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import OUTPUT_DIR, ensure_dirs


def parse_comments_for_analysis(comments):
    """从评论数据中提取统计信息"""
    total = len(comments)
    if total == 0:
        return {}
    
    # 关键词频率（简单分词）
    all_words = []
    for c in comments:
        content = c.get("content", "")
        for word in content:
            if '\u4e00' <= word <= '\u9fff':  # 中文字符
                all_words.append(word)
    
    # 大致的词频（按字符）
    char_freq = Counter(all_words).most_common(30)
    
    # 简单情感分析
    positive_words = {"好", "棒", "赞", "喜欢", "爱", "支持", "感谢", "厉害", "美", "帅", "太", "优秀", "精彩", "加油", "不错", "good", "nice"}
    negative_words = {"差", "烂", "不好", "失望", "垃圾", "讨厌", "恶心", "举报", "投诉", "无语", "烦"}
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for c in comments:
        content = c.get("content", "")
        pos_score = sum(1 for w in positive_words if w in content)
        neg_score = sum(1 for w in negative_words if w in content)
        
        if pos_score > neg_score:
            positive_count += 1
        elif neg_score > pos_score:
            negative_count += 1
        else:
            neutral_count += 1
    
    # 作者活跃度
    author_freq = Counter()
    for c in comments:
        author = c.get("author_name", "unknown")
        if author:
            author_freq[author] += 1
    
    return {
        "total": total,
        "sentiment": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
        },
        "top_keywords": [{"word": w, "count": n} for w, n in char_freq if len(w) >= 2],
        "top_authors": [
            {"name": a, "count": n}
            for a, n in author_freq.most_common(10)
        ],
    }


def generate_html_report(comments, reply_results=None, output_path=None):
    """生成交互式 HTML 分析报告"""
    
    analysis = parse_comments_for_analysis(comments)
    total = analysis.get("total", 0)
    sentiment = analysis.get("sentiment", {})
    top_keywords = analysis.get("top_keywords", [])
    top_authors = analysis.get("top_authors", [])
    
    # 回复统计
    reply_stats = {}
    if reply_results:
        reply_stats = {
            "total": reply_results.get("total", 0),
            "success": reply_results.get("success", 0),
            "skipped": reply_results.get("skipped", 0),
            "failed": reply_results.get("failed", 0),
            "strategy": reply_results.get("strategy", "N/A"),
        }
    
    # 情感占比
    pos = sentiment.get("positive", 0)
    neg = sentiment.get("negative", 0)
    neu = sentiment.get("neutral", 0)
    sent_total = pos + neg + neu or 1
    
    pos_pct = round(pos / sent_total * 100, 1)
    neg_pct = round(neg / sent_total * 100, 1)
    neu_pct = round(neu / sent_total * 100, 1)
    
    # 构建报告 HTML
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>抖音评论管理报告</title>
    <style>
        :root {{
            --bg: #ffffff;
            --card-bg: #f8f9fa;
            --text: #1a1a2e;
            --text-secondary: #666;
            --primary: #ff0040;
            --primary-light: #ffe5ec;
            --success: #00c853;
            --success-light: #e8f5e9;
            --warning: #ff9800;
            --warning-light: #fff3e0;
            --danger: #ff1744;
            --danger-light: #ffebee;
            --border: #e0e0e0;
            --shadow: 0 2px 12px rgba(0,0,0,0.08);
            --radius: 12px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #f0f2f5;
            color: var(--text);
            line-height: 1.6;
            padding: 24px;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #ff0040, #ff6b81);
            color: white;
            padding: 32px;
            border-radius: var(--radius);
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(255,0,64,0.3);
        }}
        .header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 4px; }}
        .header .subtitle {{ opacity: 0.85; font-size: 14px; }}
        .header .time {{ opacity: 0.7; font-size: 12px; margin-top: 8px; }}
        
        /* Summary Cards */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .summary-card {{
            background: var(--card-bg);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            gap: 16px;
            transition: transform 0.2s;
        }}
        .summary-card:hover {{ transform: translateY(-2px); }}
        .summary-card .icon {{
            width: 48px; height: 48px;
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px;
        }}
        .summary-card .info .value {{ font-size: 28px; font-weight: 700; }}
        .summary-card .info .label {{ font-size: 13px; color: var(--text-secondary); }}
        
        /* Section */
        .section {{
            background: white;
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}
        .section h2 {{
            font-size: 18px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--primary-light);
            display: flex; align-items: center;
            gap: 8px;
        }}
        
        /* Sentiment Bar */
        .sentiment-bar {{
            display: flex;
            height: 36px;
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        .sentiment-bar .pos {{ background: var(--success); }}
        .sentiment-bar .neu {{ background: #90a4ae; }}
        .sentiment-bar .neg {{ background: var(--danger); }}
        .sentiment-legend {{
            display: flex; gap: 24px; justify-content: center;
            font-size: 14px;
        }}
        .sentiment-legend span {{
            display: flex; align-items: center; gap: 6px;
        }}
        .sentiment-legend .dot {{
            width: 10px; height: 10px; border-radius: 50%; display: inline-block;
        }}
        
        /* Keyword Tags */
        .keyword-cloud {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .keyword-tag {{
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            background: var(--primary-light);
            color: var(--primary);
            font-weight: 500;
            transition: transform 0.2s;
        }}
        .keyword-tag:hover {{ transform: scale(1.05); }}
        .keyword-tag .count {{
            font-size: 11px;
            opacity: 0.7;
            margin-left: 4px;
        }}
        
        /* Authors Table */
        .author-list {{
            display: flex; flex-direction: column; gap: 8px;
        }}
        .author-item {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 10px 16px;
            background: var(--card-bg);
            border-radius: 8px;
        }}
        .author-item .rank {{
            width: 28px; height: 28px;
            border-radius: 50%;
            background: var(--primary-light);
            color: var(--primary);
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 600;
        }}
        .author-item .name {{ flex: 1; margin-left: 12px; font-weight: 500; }}
        .author-item .comment-count {{
            font-size: 13px; color: var(--text-secondary);
        }}
        
        /* Reply Stats */
        .reply-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            text-align: center;
        }}
        .reply-stat {{
            padding: 16px;
            background: var(--card-bg);
            border-radius: 8px;
        }}
        .reply-stat .num {{ font-size: 32px; font-weight: 700; }}
        .reply-stat .lbl {{ font-size: 13px; color: var(--text-secondary); margin-top: 4px; }}
        .reply-stat.success .num {{ color: var(--success); }}
        .reply-stat.failed .num {{ color: var(--danger); }}
        .reply-stat.skipped .num {{ color: var(--warning); }}
        
        /* Comment List */
        .comment-list {{ max-height: 500px; overflow-y: auto; }}
        .comment-item {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            display: flex; gap: 12px; align-items: flex-start;
        }}
        .comment-item:last-child {{ border-bottom: none; }}
        .comment-item .avatar {{
            width: 36px; height: 36px;
            border-radius: 50%;
            background: var(--primary-light);
            color: var(--primary);
            display: flex; align-items: center; justify-content: center;
            font-weight: 600; font-size: 14px;
            flex-shrink: 0;
        }}
        .comment-item .body {{ flex: 1; }}
        .comment-item .author-name {{ font-weight: 600; font-size: 14px; }}
        .comment-item .text {{ font-size: 14px; color: var(--text); margin-top: 4px; }}
        .comment-item .meta {{ font-size: 12px; color: var(--text-secondary); margin-top: 4px; }}
        
        /* Footer */
        .footer {{
            text-align: center; padding: 24px;
            color: var(--text-secondary); font-size: 13px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 12px; }}
            .header {{ padding: 20px; }}
            .header h1 {{ font-size: 22px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎬 抖音评论管理报告</h1>
            <div class="subtitle">批量回复执行结果 & 评论数据分析</div>
            <div class="time">生成时间: {report_time}</div>
        </div>

        <!-- Overview Cards -->
        <div class="summary-grid">
            <div class="summary-card">
                <div class="icon" style="background:#fff3e0;color:#ff9800;">💬</div>
                <div class="info">
                    <div class="value">{total}</div>
                    <div class="label">评论总数</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="icon" style="background:#e8f5e9;color:#00c853;">✅</div>
                <div class="info">
                    <div class="value">{reply_stats.get('success', 0)}</div>
                    <div class="label">成功回复</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="icon" style="background:#ffe5ec;color:#ff0040;">📊</div>
                <div class="info">
                    <div class="value">{reply_stats.get('strategy', 'N/A')}</div>
                    <div class="label">回复策略</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="icon" style="background:#e3f2fd;color:#2196f3;">🎯</div>
                <div class="info">
                    <div class="value">{pos_pct}%</div>
                    <div class="label">正面评论占比</div>
                </div>
            </div>
        </div>

        <!-- Sentiment Analysis -->
        <div class="section">
            <h2>📈 评论情感分析</h2>
            <div class="sentiment-bar">
                <div class="pos" style="width:{pos_pct}%"></div>
                <div class="neu" style="width:{neu_pct}%"></div>
                <div class="neg" style="width:{neg_pct}%"></div>
            </div>
            <div class="sentiment-legend">
                <span><span class="dot" style="background:var(--success)"></span> 正面 {pos} 条 ({pos_pct}%)</span>
                <span><span class="dot" style="background:#90a4ae"></span> 中性 {neu} 条 ({neu_pct}%)</span>
                <span><span class="dot" style="background:var(--danger)"></span> 负面 {neg} 条 ({neg_pct}%)</span>
            </div>
        </div>

        <!-- Reply Execution -->
        <div class="section">
            <h2>🚀 批量回复执行结果</h2>
            <div class="reply-stats">
                <div class="reply-stat success">
                    <div class="num">{reply_stats.get('success', 0)}</div>
                    <div class="lbl">✅ 成功</div>
                </div>
                <div class="reply-stat skipped">
                    <div class="num">{reply_stats.get('skipped', 0)}</div>
                    <div class="lbl">⏭️ 跳过</div>
                </div>
                <div class="reply-stat failed">
                    <div class="num">{reply_stats.get('failed', 0)}</div>
                    <div class="lbl">❌ 失败</div>
                </div>
            </div>
        </div>

        <!-- Top Keywords -->
        <div class="section">
            <h2>🔑 高频关键词</h2>
            <div class="keyword-cloud">
                {"".join(f'<span class="keyword-tag">{kw["word"]}<span class="count">({kw["count"]})</span></span>' for kw in top_keywords[:20])}
            </div>
        </div>

        <!-- Top Active Fans -->
        <div class="section">
            <h2>🏆 互动最活跃粉丝 TOP 10</h2>
            <div class="author-list">
                {"".join(f'<div class="author-item"><span class="rank">{i+1}</span><span class="name">{a["name"]}</span><span class="comment-count">{a["count"]} 条评论</span></div>' for i, a in enumerate(top_authors))}
            </div>
        </div>

        <!-- Latest Comments -->
        <div class="section">
            <h2>📝 最新评论列表（前 50 条）</h2>
            <div class="comment-list">
                {"".join(f'<div class="comment-item"><div class="avatar">{c.get("author_name", "?")[0] if c.get("author_name") else "?"}</div><div class="body"><div class="author-name">{c.get("author_name", "匿名用户")}</div><div class="text">{c.get("content", "")[:200]}</div><div class="meta">👍 {c.get("like_count", 0)} · {c.get("create_time", "")[:10]}</div></div></div>' for c in comments[:50])}
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>由「抖音评论管理助手」自动生成 · Powered by WorkBuddy Skill</p>
            <p style="margin-top: 4px;font-size:12px;">douyin-comment-manager v1.0.0</p>
        </div>
    </div>
</body>
</html>"""
    
    if output_path:
        output_file = Path(output_path)
    else:
        output_file = OUTPUT_DIR / "report.html"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"[SAVED] 报告已生成 → {output_file}")
    return str(output_file)


def main():
    parser = argparse.ArgumentParser(description="抖音评论管理 - 可视化报告生成")
    parser.add_argument("--input", type=str, help="评论 JSON 文件（未回复评论或回复结果）")
    parser.add_argument("--reply-results", type=str, help="回复结果 JSON 文件")
    parser.add_argument("--output", type=str, help="报告 HTML 输出路径")
    parser.add_argument("--date-range", nargs=2, help="日期范围 START END")
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    # 加载数据
    comments = []
    reply_results = None
    
    if args.input:
        input_path = Path(args.input)
        if input_path.exists():
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    comments = data
                elif isinstance(data, dict) and "results" in data:
                    # 是回复结果
                    reply_results = data
                    comments = [r for r in data.get("results", [])]
    
    if args.reply_results:
        rr_path = Path(args.reply_results)
        if rr_path.exists():
            with open(rr_path, "r", encoding="utf-8") as f:
                reply_results = json.load(f)
    
    if not comments:
        print("[ERROR] 没有评论数据。请使用 --input 指定评论 JSON 文件。")
        print("  示例: python scripts/report.py --input output/unreplied_comments.json")
        sys.exit(1)
    
    output_path = generate_html_report(comments, reply_results, args.output)


if __name__ == "__main__":
    main()
