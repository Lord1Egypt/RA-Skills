#!/usr/bin/env python3
"""
Auto-Claw Content Quality Auditor 演示
"""
import sys, os, requests
sys.path.insert(0, os.path.dirname(__file__))

from src.seo import SEOAnalyzer
from src.content_audit import ContentAuditor, ContentAuditResult

SITE_URL = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw Content Quality Auditor             ║
║       可读性 · 结构深度 · E-A-T 审计                 ║
╚══════════════════════════════════════════════════════════╝"""

def print_result(r: ContentAuditResult):
    print(f"\n  📄 {r.url}")
    print(f"     标题: {r.title[:50] if r.title else '(空)'}")
    
    # 评分
    q_icon = "🟢" if r.quality_score >= 80 else "🟡" if r.quality_score >= 60 else "🔴"
    print(f"     综合评分: {q_icon} {r.quality_score}/100")
    print(f"     字数: {r.word_count} | 阅读时间: {r.reading_time_minutes:.1f}分钟")
    
    # 可读性
    rk_icon = "🟢" if r.flesch_kincaid_grade <= 8 else "🟡" if r.flesch_kincaid_grade <= 10 else "🔴"
    print(f"     可读性: {rk_icon} 年级{r.flesch_kincaid_grade}级 | 易读性{r.flesch_reading_ease:.0f}/100")
    
    # 结构
    struct = f"  H1:{r.h1_count} H2:{r.h2_count} H3:{r.h3_count} 图:{r.image_count}"
    struct += f"  内链:{r.internal_link_count} 外链:{r.external_link_count}"
    print(f"     结构:{struct}")
    
    # E-A-T
    eat = []
    if r.has_author: eat.append("✅ 作者")
    else: eat.append("❌ 作者")
    if r.has_published_date: eat.append("✅ 日期")
    else: eat.append("❌ 日期")
    if r.has_schema: eat.append("✅ Schema")
    else: eat.append("❌ Schema")
    print(f"     E-A-T: {' | '.join(eat)}")
    
    # 问题
    if r.issues:
        errors = [i for i in r.issues if i.severity == "ERROR"]
        warns = [i for i in r.issues if i.severity == "WARNING"]
        print(f"     ⚠️ 错误:{len(errors)} 警告:{len(warns)}")
        for i in r.issues[:2]:
            print(f"       • [{i.severity}] {i.message[:60]}")
    
    # 建议
    for rec in r.recommendations[:2]:
        print(f"     {rec}")

def main():
    print(BANNER)
    
    # 扫描页面
    analyzer = SEOAnalyzer(SITE_URL, wp_web_root=WEB_ROOT)
    urls_data = analyzer.get_all_urls(limit=5)
    
    # 获取HTML
    html_content = {}
    for page_info in urls_data[:4]:
        try:
            resp = requests.get(page_info["url"], timeout=10, verify=False)
            html_content[page_info["url"]] = resp.text
        except:
            html_content[page_info["url"]] = ""
    
    # 审计
    auditor = ContentAuditor()
    results = []
    
    print("\n" + "="*60)
    print("  正在审计页面内容质量...")
    print("="*60)
    
    for page_info in urls_data[:4]:
        url = page_info["url"]
        html = html_content.get(url, "")
        title = page_info.get("title", "")
        
        result = auditor.audit_page(url, html, title)
        results.append(result)
        
        print_result(result)
    
    # 汇总
    print("\n" + "="*60)
    print("  📊 汇总统计")
    print("="*60)
    
    avg_quality = sum(r.quality_score for r in results) / len(results)
    avg_words = sum(r.word_count for r in results) / len(results)
    avg_readability = sum(r.flesch_reading_ease for r in results) / len(results)
    total_issues = sum(len(r.issues) for r in results)
    
    print(f"\n  总审计页面: {len(results)}")
    print(f"  平均质量分: {avg_quality:.0f}/100 {'🟢' if avg_quality >= 70 else '🔴'}")
    print(f"  平均字数: {avg_words:.0f} {'✅' if avg_words >= 600 else '🔴'}")
    print(f"  平均易读性: {avg_readability:.0f}/100")
    print(f"  总问题数: {total_issues}")
    
    # 问题类型分布
    issue_types = {}
    for r in results:
        for i in r.issues:
            issue_types[i.category] = issue_types.get(i.category, 0) + 1
    
    print(f"\n  问题类型分布:")
    for cat, count in sorted(issue_types.items(), key=lambda x: -x[1]):
        print(f"    • {cat}: {count}")
    
    print("\n" + "="*60)
    print("  ✅ 内容审计完成")
    print("="*60)
    print(f"""
  评估维度：
    📖 可读性 — Flesch-Kincaid 年级水平
    📝 内容深度 — 字数、结构、引用
    🏛️  E-A-T  — 作者、日期、Schema
    🔗 链接健康 — 内外链比例
    🎯 综合评分 — 0-100 分

  能力 #3 完成: Content Quality Auditor ✅
""")

if __name__ == "__main__":
    main()
