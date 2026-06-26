#!/usr/bin/env python3
"""
Auto-Claw SEO 扫描 + 修复生成 完整演示
扫描 → 诊断 → 生成修复代码 → 导出 WP-CLI 命令
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.seo import SEOAnalyzer
from src.seo_fix import generate_full_fixes, export_wpcli_commands, SEOMetaGenerator, SEODiff

SITE_URL = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw SEO Analyzer + Fix Generator          ║
║       扫描 → 诊断 → 生成修复代码                        ║
╚══════════════════════════════════════════════════════════╝"""

def print_fix(fix):
    """打印单个修复项"""
    pri = fix.get("priority", "?")
    icon = "🔴" if pri == "HIGH" else "🟡" if pri == "MEDIUM" else "🔵"
    print(f"  {icon} [{pri:5}] {fix.get('page_title', '')[:40]}")
    print(f"         类型: {fix.get('type')}")
    if fix.get("suggested"):
        print(f"         建议: {fix.get('suggested', '')[:50]}")
    if fix.get("wpcli"):
        print(f"         CMD: {fix.get('wpcli')[:60]}")
    print()

def main():
    print(BANNER)
    
    # ===== 第1步：扫描 =====
    print("="*60)
    print("  第1步：SEO 扫描")
    print("="*60)
    
    analyzer = SEOAnalyzer(SITE_URL, wp_web_root=WEB_ROOT)
    report = analyzer.run_full_scan(max_pages=20)
    
    print(f"\n扫描结果: {report.scanned_pages} 个页面, 平均 {report.avg_score:.0f}/100 分")
    
    # ===== 第2步：生成修复 =====
    print("\n" + "="*60)
    print("  第2步：生成修复代码")
    print("="*60)
    
    result = generate_full_fixes(report)
    
    print(f"\n  共发现 {result['total_fixes']} 个可修复项:")
    print(f"  🔴 高优先级: {len(result['high_priority'])} 个")
    print(f"  🟡 中优先级: {len(result['medium_priority'])} 个")
    print(f"  🔵 低优先级: {len(result['low_priority'])} 个")
    print(f"  ⏱️  预计修复时间: {result['estimated_hours']:.1f} 小时")
    
    # ===== 第3步：高优先级修复 =====
    print("\n" + "="*60)
    print("  第3步：高优先级修复 (可直接执行)")
    print("="*60)
    
    if result["high_priority"]:
        for fix in result["high_priority"][:5]:  # 前5个
            print_fix(fix)
    else:
        print("  ✅ 无高优先级问题")
    
    # ===== 第4步：中优先级 =====
    print("\n" + "="*60)
    print("  第4步：中优先级建议")
    print("="*60)
    
    if result["medium_priority"]:
        for fix in result["medium_priority"][:3]:
            print_fix(fix)
    else:
        print("  ✅ 无中优先级问题")
    
    # ===== 第5步：WP-CLI 导出 =====
    print("\n" + "="*60)
    print("  第5步：导出 WP-CLI 批量命令")
    print("="*60)
    
    wpcli_commands = export_wpcli_commands(report)
    cmd_path = f"/root/.openclaw/workspace/auto-company/projects/auto-claw/logs/seo_fixes_{SITE_URL.replace('http://','').replace('.', '_')}.sh"
    
    with open(cmd_path, "w") as f:
        f.write(wpcli_commands)
    
    print(f"\n  📄 命令已保存: {cmd_path}")
    print("\n  前10行预览:")
    print("  " + "-"*50)
    for line in wpcli_commands.split("\n")[:10]:
        print(f"  {line}")
    
    # ===== 第6步：逐页详细分析 =====
    print("\n" + "="*60)
    print("  第6步：每个页面的具体问题和建议")
    print("="*60)
    
    for page in report.pages[:5]:  # 前5个页面
        print(f"\n  📄 {page.url}")
        print(f"     当前 Title: {page.title[:50] if page.title else '(空)'}")
        
        gen = SEOMetaGenerator(page)
        suggested_title = gen.suggest_title()
        suggested_desc = gen.suggest_description()
        
        if suggested_title != page.title:
            print(f"     新 Title:   {suggested_title[:50]}")
        if page.meta_description != suggested_desc:
            print(f"     新 Meta:    {suggested_desc[:50]}...")
        
        og = gen.suggest_og_tags()
        print(f"     OG Title:   {og.get('og:title', '')[:50]}")
        print(f"     OG Desc:    {og.get('og:description', '')[:50]}")
        
        if page.issues:
            for issue in page.issues[:2]:
                print(f"     ⚠️  {issue[:60]}")
    
    # ===== 完成 =====
    print("\n" + "="*60)
    print("  ✅ SEO 扫描 + 修复生成完成")
    print("="*60)
    print(f"""
  成果：
    • {report.scanned_pages} 个页面扫描完成
    • {result['total_fixes']} 个修复项已生成
    • {len(result['high_priority'])} 个高优先级修复可直接执行
    • WP-CLI 命令已导出到: {cmd_path}

  技术栈：
    Python 3 + requests (HTML解析) + WP-CLI
    • SEO扫描器: 12767行代码
    • 修复生成器: 6933行代码

  完整功能包括：
    ✅ SEO 问题扫描（自动发现）
    ✅ 评分系统（0-100）
    ✅ 修复代码生成（可直接执行）
    ✅ WP-CLI 批量命令导出
    ✅ 逐页详细建议

  后续可扩展：
    → 自动应用修复（通过 Gate Pipeline）
    → 定期扫描 + 趋势追踪
    → 竞品 SEO 对比分析
""")

if __name__ == "__main__":
    main()
