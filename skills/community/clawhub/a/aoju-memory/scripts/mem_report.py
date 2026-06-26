#!/usr/bin/env python3
"""
mem_report.py — 生成精美的 HTML 记忆报告
使用方式: python3 mem_report.py [--days 30] [--output report.html]
"""
import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_FILE = MEMORY_DIR / "learnings" / "patterns.md"


def get_file_stats(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "size": 0, "lines": 0, "modified": None}
    stat = path.stat()
    content = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "exists": True,
        "size": stat.st_size,
        "lines": len(content.split("\n")),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def count_recent_daily_logs(days: int = 30) -> int:
    if not MEMORY_DIR.exists():
        return 0
    today = datetime.now()
    count = 0
    for d in range(days):
        date = today - timedelta(days=d)
        if (MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md").exists():
            count += 1
    return count


def count_learnings() -> int:
    if not LEARNINGS_DIR.exists():
        return 0
    return len(list(LEARNINGS_DIR.glob("*.md")))


def count_patterns() -> int:
    if not PATTERNS_FILE.exists():
        return 0
    content = PATTERNS_FILE.read_text(encoding="utf-8", errors="ignore")
    return content.count("## Pattern")


def get_recent_learnings(days: int = 30) -> list[dict]:
    learnings = []
    if not LEARNINGS_DIR.exists():
        return learnings
    cutoff = datetime.now() - timedelta(days=days)
    for f in sorted(LEARNINGS_DIR.glob("*.md"), reverse=True):
        try:
            date_str = f.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                break
            content = f.read_text(encoding="utf-8", errors="ignore")
            learnings.append({"date": date_str, "content": content})
        except Exception:
            continue
    return learnings


def get_memory_summary() -> str:
    """Extract key sections from MEMORY.md."""
    if not MEMORY_FILE.exists():
        return ""
    content = MEMORY_FILE.read_text(encoding="utf-8", errors="ignore")
    # Extract first 500 chars as summary
    lines = content.split("\n")
    summary_lines = []
    for line in lines:
        if line.startswith("## "):
            if summary_lines:
                break
        summary_lines.append(line)
        if len(summary_lines) > 20:
            break
    return "\n".join(summary_lines)


def health_score(stats: dict, daily_count: int, learnings_count: int, patterns_count: int) -> tuple[int, str]:
    score = 0
    reasons = []
    if stats['exists'] and stats['lines'] > 50:
        score += 30
        reasons.append("MEMORY.md 完善")
    elif stats['exists']:
        score += 15
        reasons.append("MEMORY.md 较薄")
    if daily_count >= 5:
        score += 25
        reasons.append(f"日志覆盖良好 ({daily_count}天)")
    elif daily_count > 0:
        score += 10
        reasons.append(f"有日志记录 ({daily_count}天)")
    if learnings_count >= 5:
        score += 25
        reasons.append(f"学习积累丰富 ({learnings_count}条)")
    elif learnings_count > 0:
        score += 10
        reasons.append(f"有学习记录 ({learnings_count}条)")
    if patterns_count > 0:
        score += 20
        reasons.append(f"已识别模式 ({patterns_count}个)")
    
    if score >= 80:
        label = "优秀"
    elif score >= 60:
        label = "良好"
    elif score >= 40:
        label = "一般"
    else:
        label = "需加强"
    
    return score, label, " | ".join(reasons)


def generate_html_report(stats: dict, daily_count: int, learnings: list, patterns_count: int, days: int) -> str:
    score, label, reasons = health_score(stats, daily_count, len(learnings), patterns_count)
    
    # Score color
    if score >= 80:
        score_color = "#22c55e"
        score_bg = "#dcfce7"
    elif score >= 60:
        score_color = "#3b82f6"
        score_bg = "#dbeafe"
    elif score >= 40:
        score_color = "#f59e0b"
        score_bg = "#fef3c7"
    else:
        score_color = "#ef4444"
        score_bg = "#fee2e2"
    
    learnings_html = ""
    for lr in learnings[:10]:
        content = lr["content"]
        incident = extract_section(content, "### Incident", "### Lesson")
        lesson = extract_section(content, "### Lesson", "### Context")
        confidence = extract_section(content, "### Confidence", "---")
        tags_raw = extract_section(content, "### Tags", "### Confidence")
        tags = [t.strip() for t in tags_raw.replace("#", "").split() if t.strip()]
        
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags[:4]) if tags else ""
        conf_icon = "🔴" if "high" in confidence.lower() else ("🟡" if "medium" in confidence.lower() else "⚪")
        
        learnings_html += f"""
        <div class="learning-card">
            <div class="learning-header">
                <span class="date">{lr['date']}</span>
                <span class="confidence">{conf_icon} {confidence.strip()}</span>
            </div>
            <div class="incident">💬 {incident[:100]}{'...' if len(incident) > 100 else ''}</div>
            <div class="lesson">📝 {lesson[:120]}{'...' if len(lesson) > 120 else ''}</div>
            {tag_html}
        </div>"""

    memory_summary = get_memory_summary()
    summary_lines = [f"<p>{l}</p>" if l.strip() and not l.startswith("#") else f"<h2>{l}</h2>" if l.startswith("## ") else f"<h3>{l}</h3>" if l.startswith("### ") else l for l in memory_summary.split("\n")]
    summary_html = "\n".join(summary_lines)

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐺 记忆系统报告 — {datetime.now().strftime('%Y-%m-%d')}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%); min-height: 100vh; color: #e2e8f0; padding: 2rem; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  
  .header {{ text-align: center; margin-bottom: 2rem; }}
  .header h1 {{ font-size: 2rem; color: #fff; margin-bottom: 0.5rem; }}
  .header p {{ color: #94a3b8; font-size: 0.9rem; }}
  
  .score-section {{ background: {score_bg}; border-radius: 20px; padding: 2rem; text-align: center; margin-bottom: 2rem; }}
  .score-number {{ font-size: 4rem; font-weight: 800; color: {score_color}; line-height: 1; }}
  .score-label {{ font-size: 1.2rem; color: {score_color}; font-weight: 600; margin-top: 0.5rem; }}
  .score-reasons {{ color: #64748b; font-size: 0.85rem; margin-top: 0.75rem; }}
  
  .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .stat-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.25rem; text-align: center; }}
  .stat-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
  .stat-value {{ font-size: 2rem; font-weight: 700; color: #fff; }}
  .stat-label {{ color: #94a3b8; font-size: 0.8rem; margin-top: 0.25rem; }}
  .stat-status {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem; margin-top: 0.5rem; }}
  .stat-ok {{ background: #dcfce7; color: #166534; }}
  .stat-warn {{ background: #fef3c7; color: #92400e; }}
  .stat-bad {{ background: #fee2e2; color: #991b1b; }}
  
  .section {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; }}
  .section h2 {{ color: #fff; font-size: 1.1rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); }}
  
  .learnings-grid {{ display: grid; gap: 1rem; }}
  .learning-card {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; }}
  .learning-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
  .date {{ color: #94a3b8; font-size: 0.8rem; }}
  .confidence {{ color: #94a3b8; font-size: 0.75rem; }}
  .incident {{ color: #e2e8f0; font-size: 0.9rem; margin-bottom: 0.5rem; line-height: 1.5; }}
  .lesson {{ color: #a5b4fc; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.5rem; }}
  .tag {{ display: inline-block; background: rgba(99, 102, 241, 0.2); color: #a5b4fc; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.7rem; margin-right: 0.3rem; }}
  
  .memory-summary {{ color: #cbd5e1; font-size: 0.9rem; line-height: 1.8; }}
  .memory-summary h2 {{ color: #fff; font-size: 1rem; margin: 1rem 0 0.5rem; }}
  .memory-summary h3 {{ color: #e2e8f0; font-size: 0.95rem; margin: 0.8rem 0 0.4rem; }}
  .memory-summary p {{ margin-bottom: 0.5rem; }}
  
  .footer {{ text-align: center; color: #475569; font-size: 0.75rem; margin-top: 2rem; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🐺 记忆系统健康报告</h1>
    <p>{datetime.now().strftime('%Y年%m月%d日 %H:%M')} · 近{days}天数据</p>
  </div>
  
  <div class="score-section">
    <div class="score-number">{score}</div>
    <div class="score-label">健康度: {label}</div>
    <div class="score-reasons">{reasons}</div>
  </div>
  
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon">📄</div>
      <div class="stat-value">{stats['lines']}</div>
      <div class="stat-label">MEMORY.md 行数</div>
      <span class="stat-status {'stat-ok' if stats['exists'] else 'stat-bad'}">{'存在' if stats['exists'] else '缺失'}</span>
    </div>
    <div class="stat-card">
      <div class="stat-icon">📅</div>
      <div class="stat-value">{daily_count}</div>
      <div class="stat-label">日志覆盖天数</div>
      <span class="stat-status {'stat-ok' if daily_count >= 5 else 'stat-warn' if daily_count > 0 else 'stat-bad'}">{'良好' if daily_count >= 5 else '稀疏' if daily_count > 0 else '无'}</span>
    </div>
    <div class="stat-card">
      <div class="stat-icon">💡</div>
      <div class="stat-value">{len(learnings)}</div>
      <div class="stat-label">学习记录条数</div>
      <span class="stat-status {'stat-ok' if len(learnings) >= 5 else 'stat-warn' if len(learnings) > 0 else 'stat-bad'}">{'丰富' if len(learnings) >= 5 else '少量' if len(learnings) > 0 else '空'}</span>
    </div>
    <div class="stat-card">
      <div class="stat-icon">🔄</div>
      <div class="stat-value">{patterns_count}</div>
      <div class="stat-label">识别模式数</div>
      <span class="stat-status {'stat-ok' if patterns_count > 0 else 'stat-warn'}">{'已形成' if patterns_count > 0 else '暂无'}</span>
    </div>
  </div>
  
  <div class="section">
    <h2>💡 最新学习记录</h2>
    <div class="learnings-grid">
      {learnings_html if learnings_html else '<p style="color:#64748b">暂无学习记录 — 多给老二反馈，它会越来越懂你</p>'}
    </div>
  </div>
  
  <div class="section">
    <h2>🧠 长期记忆摘要</h2>
    <div class="memory-summary">
      {summary_html if summary_html else '<p>MEMORY.md 为空或不存在</p>'}
    </div>
  </div>
  
  <div class="footer">
    <p>aoju-memory · 记忆系统 v1.0 · Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  </div>
</div>
</body>
</html>"""


def extract_section(content: str, start_marker: str, end_marker: str) -> str:
    import re
    pattern = re.escape(start_marker) + r"\s*\n(.*?)(?=\n##|###|---|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def main():
    parser = argparse.ArgumentParser(description="生成精美的记忆系统 HTML 报告")
    parser.add_argument("--days", type=int, default=30, help="回顾最近 N 天 (默认30)")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径 (默认 ~/memory-report.html)")
    args = parser.parse_args()
    
    stats = get_file_stats(MEMORY_FILE)
    daily_count = count_recent_daily_logs(args.days)
    learnings = get_recent_learnings(args.days)
    patterns_count = count_patterns()
    
    html = generate_html_report(stats, daily_count, learnings, patterns_count, args.days)
    
    output_path = args.output or str(Path.home() / "memory-report.html")
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ 报告已生成: {output_path}")
    print(f"   用浏览器打开查看效果 🌐")


if __name__ == "__main__":
    main()
