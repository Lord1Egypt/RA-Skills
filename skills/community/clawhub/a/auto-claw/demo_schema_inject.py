#!/usr/bin/env python3
"""
Demo: 结构化数据 + SEO + 内容质量 综合审计
测试站点: linghangyuan1234.dpdns.org
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + "/src")

import requests
from seo import SEOAnalyzer
from schema import SchemaGenerator
from content import ContentQualityAuditor
from wordpress import WordPressClient

TARGET = "http://linghangyuan1234.dpdns.org"

def fetch_html(url: str) -> str:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Auto-Claw-Perf/1.0"})
        r.encoding = r.apparent_encoding or 'utf-8'
        return r.text
    except:
        return ""


def demo():
    print("=" * 60)
    print("🧠 Auto-Claw: SEO + Schema + Content 综合审计")
    print("=" * 60)
    
    # 1. SEO 扫描
    print("\n[1/4] SEO 扫描中...")
    scanner = SEOAnalyzer(TARGET)
    report = scanner.run_full_scan(max_pages=8)
    print(f"  扫描页面: {report.scanned_pages}")
    print(f"  平均分: {report.avg_score:.1f}/100")
    print(f"  问题总数: {report.total_issues}")
    
    # 2. Schema 生成
    print("\n[2/4] JSON-LD Schema 生成中...")
    schema_gen = SchemaGenerator(
        site_name="灵航院 AI 工具",
        site_url=TARGET,
    )
    
    injected_schemas = []
    for page in report.pages:
        if page.url.endswith("/category/uncategorized"):
            continue
        schemas = schema_gen.generate_for_wordpress_page(
            url=page.url,
            title=page.title,
        )
        for s in schemas:
            print(f"  ✓ {s.page_type}: {s.page_url[:55]}")
            if s.json_ld:
                injected_schemas.append(s.json_ld)
    
    print(f"  总计生成 Schema: {len(injected_schemas)} 个")
    
    # 3. 内容质量审计
    print("\n[3/4] 内容质量审计中...")
    auditor = ContentQualityAuditor()
    for page in report.pages:
        if page.url.endswith("/category/uncategorized"):
            continue
        html = fetch_html(page.url)
        if html:
            q = auditor.audit_page(page.url, html, page.title)
            print(f"  📄 {q.title[:40]}")
            print(f"     质量: {q.quality_score:.1f} | 可读性: {q.readability_score:.0f} | SEO: {q.seo_score:.0f}")
            for s in q.suggestions[:2]:
                print(f"     → {s[:70]}")
    
    # 4. 生成注入代码
    print("\n[4/4] WordPress JSON-LD 注入方案...")
    wp_client = WordPressClient(
        ssh_host="localhost",
        ssh_user="",
        ssh_key="",
        web_root="/www/wwwroot/linghangyuan1234.dpdns.org",
    )
    
    if wp_client.test_connection():
        mu_code = wp_client.generate_schema_mu_plugin(injected_schemas[:5])
        # 保存
        out_path = "/root/.openclaw/workspace/auto-company/projects/auto-claw/logs/auto-claw-schema.php"
        with open(out_path, "w") as f:
            f.write(mu_code)
        print(f"  ✅ mu-plugin 已生成: {out_path} ({len(mu_code)} 字节)")
        print("  安装: 上传至 wp-content/mu-plugins/auto-claw-schema.php")
    else:
        print("  ⚠️  WP-CLI 未连接（本地测试）")
        # 仍保存本地版本
        out_path = "/root/.openclaw/workspace/auto-company/projects/auto-claw/logs/auto-claw-schema.php"
        import json
        mu_code = f'''<?php
/**
 * Auto-Claw JSON-LD Schema Injection (mu-plugin)
 * 放到: wp-content/mu-plugins/auto-claw-schema.php
 */
add_action('wp_head', function() {{
    $schemas = {json.dumps(injected_schemas[:5], ensure_ascii=False, indent=4)};
    foreach ($schemas as $s) {{
        echo '<script type="application/ld+json">' . wp_json_encode($s, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>' . "\\n";
    }}
}}, 1);
'''
        with open(out_path, "w") as f:
            f.write(mu_code)
        print(f"  ✅ 本地版本已生成: {out_path} ({len(mu_code)} 字节)")
    
    print("\n" + "=" * 60)
    print("📊 综合报告")
    print("=" * 60)
    print(auditor.summary())
    
    # 能力完成度更新
    completed = 5  # SEO扫描 + SEO修复 + Schema生成 + 内容审计 + 性能诊断
    total = 19
    pct = completed / total * 100
    
    print(f"\n🔋 Cycle 1 能力完成度: {completed}/{total} ({pct:.1f}%)")
    print()
    print("✅ #1  SEO Meta标签扫描 — 已实现")
    print("✅ #2  SEO 优化建议生成 — 已实现")
    print("✅ #3  结构化数据生成（JSON-LD）— 已实现 + 可注入")
    print("✅ #4  内容质量审计 — 已实现")
    print("✅ #15 代码级性能诊断 — 已实现 (perf.py)")
    print("❌ 剩余 14 个能力待实现")


if __name__ == "__main__":
    demo()
