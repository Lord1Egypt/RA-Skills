#!/usr/bin/env python3
"""
Auto-Claw SEO 扫描演示
对 WordPress 站点进行完整 SEO 分析
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.seo import SEOAnalyzer, SEOReport

SITE_URL = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw SEO Analyzer — 完整 SEO 扫描演示       ║
╚══════════════════════════════════════════════════════════╝"""

def print_page_result(page):
    """打印单页扫描结果"""
    score_emoji = "🟢" if page.score >= 80 else "🟡" if page.score >= 60 else "🔴"
    print(f"\n  {score_emoji} {page.url}")
    print(f"     得分: {page.score}/100")
    if page.title:
        print(f"     Title: {page.title[:60]}")
    if page.meta_description:
        print(f"     Meta: {page.meta_description[:60]}...")
    if page.issues:
        for issue in page.issues[:3]:
            print(f"     ⚠️  {issue}")
    print(f"     字数: {page.word_count} | 图片无alt: {page.images_without_alt}")

def main():
    print(BANNER)
    
    # 创建 SEO 分析器
    analyzer = SEOAnalyzer(
        site_url=SITE_URL,
        wp_web_root=WEB_ROOT,
    )
    
    # 运行完整扫描
    print("\n" + "="*60)
    print("  开始 SEO 扫描")
    print("="*60)
    
    report = analyzer.run_full_scan(max_pages=20)
    
    # ===== 打印详细结果 =====
    print("\n" + "="*60)
    print("  📊 扫描结果汇总")
    print("="*60)
    print(f"\n  🌐 站点: {report.site_url}")
    print(f"  📄 扫描页面: {report.scanned_pages} 个")
    print(f"  ⚠️  总问题: {report.total_issues} 个")
    print(f"  🔒 平均得分: {report.avg_score:.0f}/100")
    
    # 得分等级
    if report.avg_score >= 80:
        grade = "🟢 优秀"
    elif report.avg_score >= 60:
        grade = "🟡 良好"
    else:
        grade = "🔴 需改进"
    print(f"  评级: {grade}")
    
    # ===== 逐页结果 =====
    print("\n" + "="*60)
    print("  📋 逐页详细结果")
    print("="*60)
    
    for page in report.pages:
        print_page_result(page)
    
    # ===== 优化建议 =====
    if report.recommendations:
        print("\n" + "="*60)
        print("  💡 优化建议")
        print("="*60)
        for rec in report.recommendations:
            print(f"\n  {rec}")
    
    # ===== SEO 问题排行榜 =====
    print("\n" + "="*60)
    print("  🔍 问题类型统计")
    print("="*60)
    
    issue_counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for page in report.pages:
        for issue in page.issues:
            for sev in issue_counts:
                if sev in issue:
                    issue_counts[sev] += 1
    
    print(f"\n  🔴 错误: {issue_counts['ERROR']} 个")
    print(f"  🟡 警告: {issue_counts['WARNING']} 个")
    print(f"  🔵 提示: {issue_counts['INFO']} 个")
    
    # ===== JSON 导出 =====
    json_report = analyzer.export_json(report)
    json_path = f"/root/.openclaw/workspace/auto-company/projects/auto-claw/logs/seo_report_{SITE_URL.replace('http://','').replace('.', '_')}.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w") as f:
        f.write(json_report)
    print(f"\n  📄 JSON 报告已保存: {json_path}")
    
    print("\n" + "="*60)
    print("  ✅ SEO 扫描完成")
    print("="*60)

if __name__ == "__main__":
    main()
