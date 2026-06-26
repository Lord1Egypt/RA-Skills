#!/usr/bin/env python3
"""
AI 早报质量验证脚本
验证生成的早报是否符合标准：
1. 每条新闻 200-300 字详细总结
2. 每条新闻附带原文链接
3. 约 10 条资讯
4. 只包含中文内容

Usage: python3 validate_report.py [date]
"""

import re
import sys
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "output"

def validate_report(date: str = None) -> bool:
    """验证早报质量"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    report_file = OUTPUT_DIR / f"AI-Daily-{date}.md"
    
    if not report_file.exists():
        print(f"❌ 早报文件不存在：{report_file}")
        return False
    
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    warnings = []
    
    # 1. 检查新闻数量
    articles = re.findall(r'^\d+\. 【.+?】(.+?)\s*⭐', content, re.MULTILINE)
    article_count = len(articles)
    
    if article_count < 8:
        issues.append(f"新闻数量不足：{article_count} 条（标准：8-10 条）")
    elif article_count > 12:
        warnings.append(f"新闻数量过多：{article_count} 条（建议：8-10 条）")
    else:
        print(f"✅ 新闻数量：{article_count} 条")
    
    # 2. 检查每条新闻的总结长度
    summary_matches = re.findall(r'\*\*📝 核心内容\*\*：(.+?)\n\n\[阅读原文\]', content, re.DOTALL)
    
    valid_count = 0
    short_summaries = []
    long_summaries = []
    
    for i, summary in enumerate(summary_matches, 1):
        summary = summary.strip()
        length = len(summary)
        
        if length < 200:
            short_summaries.append((i, length))
        elif length > 300:
            long_summaries.append((i, length))
        else:
            valid_count += 1
    
    if short_summaries:
        issues.append(f"{len(short_summaries)} 条新闻总结不足 200 字：{short_summaries}")
    else:
        print(f"✅ 所有总结长度 >= 200 字")
    
    if long_summaries:
        warnings.append(f"{len(long_summaries)} 条新闻总结超过 300 字：{long_summaries}")
    
    valid_ratio = valid_count / len(summary_matches) * 100 if summary_matches else 0
    print(f"✅ 符合 200-300 字标准的总结：{valid_count}/{len(summary_matches)} ({valid_ratio:.0f}%)")
    
    # 3. 检查原文链接
    url_matches = re.findall(r'\[阅读原文\]\((https?://[^\)]+)\)', content)
    url_count = len(url_matches)
    
    if url_count < article_count:
        issues.append(f"缺少原文链接：{url_count}/{article_count}")
    else:
        print(f"✅ 原文链接：{url_count}/{article_count}")
    
    # 4. 检查中文内容
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
    if not has_chinese:
        issues.append("未检测到中文字符")
    else:
        print(f"✅ 包含中文内容")
    
    # 5. 检查是否有 KOL 观点或论文（可选）
    kol_section = re.search(r'## 💬 KOL 观点.*?\*今日暂无 KOL 观点\*', content, re.DOTALL)
    paper_section = re.search(r'## 📚 推荐论文.*?\*今日暂无推荐论文\*', content, re.DOTALL)
    
    if kol_section and paper_section:
        warnings.append("今日无 KOL 观点和推荐论文（可能是正常的）")
    
    # 输出结果
    print("\n" + "="*60)
    print("验证结果：")
    print("="*60)
    
    if issues:
        print("\n❌ 严重问题：")
        for issue in issues:
            print(f"  - {issue}")
    
    if warnings:
        print("\n⚠️ 警告：")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not issues and not warnings:
        print("\n✅ 所有检查通过！早报符合标准。")
        return True
    elif not issues:
        print("\n✅ 主要检查通过，有少量警告。")
        return True
    else:
        print("\n❌ 早报不符合标准，需要修复。")
        return False

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else None
    success = validate_report(date)
    sys.exit(0 if success else 1)
