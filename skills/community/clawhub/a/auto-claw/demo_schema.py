#!/usr/bin/env python3
"""
Auto-Claw Schema.org Generator 演示
为 WordPress 页面生成结构化数据
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.schema import SchemaGenerator, SchemaData
from src.seo import SEOAnalyzer

SITE_URL = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw Schema.org Generator                 ║
║       结构化数据自动生成                              ║
╚══════════════════════════════════════════════════════════╝"""

def print_schema(schema: SchemaData, depth: int = 2):
    """打印单个 Schema"""
    indent = "  " * depth
    print(f"{indent}📋 [{schema.page_type.upper()}] {schema.page_url}")
    
    if schema.issues:
        for issue in schema.issues:
            print(f"{indent}   ⚠️  {issue}")
    
    # 显示核心字段
    jld = schema.json_ld
    if jld.get("@type"):
        print(f"{indent}   @type: {jld.get('@type')}")
    if jld.get("headline") or jld.get("name"):
        print(f"{indent}   name: {(jld.get('headline') or jld.get('name'))[:60]}")
    if jld.get("description"):
        print(f"{indent}   desc: {jld.get('description')[:60]}...")
    if jld.get("datePublished"):
        print(f"{indent}   date: {jld.get('datePublished')}")
    
    # 显示注入代码片段
    if schema.injection_code:
        preview = schema.injection_code[:100].replace("\n", " ")
        print(f"{indent}   code: {preview}...")
    print()

def main():
    print(BANNER)
    
    gen = SchemaGenerator(
        site_name="Auto-Claw Demo Site",
        site_url=SITE_URL,
    )
    
    # ===== 第1步：手动生成示例 Schema =====
    print("=" * 60)
    print("  第1步：手动生成各类 Schema")
    print("=" * 60)
    
    # Article Schema
    print("\n  📰 Article Schema:")
    article = gen.generate_article(
        url=f"{SITE_URL}/sample-post",
        title="How to Optimize Your WordPress Site for SEO",
        description="A comprehensive guide to improving your WordPress SEO...",
        author="Auto-Claw Team",
        published_date="2026-03-24",
        image_url=f"{SITE_URL}/wp-content/uploads/seo-guide.jpg"
    )
    print_schema(article)
    
    # FAQ Schema
    print("  ❓ FAQ Schema:")
    faqs = [
        {"question": "What is WordPress SEO?", "answer": "WordPress SEO is the process..."},
        {"question": "How long does SEO take?", "answer": "SEO typically takes 3-6 months..."},
        {"question": "Do I need plugins for SEO?", "answer": "While WordPress has basic SEO..."},
    ]
    faq_schema = gen.generate_faq(
        url=f"{SITE_URL}/faq",
        title="SEO FAQ",
        faqs=faqs
    )
    print_schema(faq_schema)
    
    # Product Schema
    print("  🛒 Product Schema:")
    product = gen.generate_product(
        url=f"{SITE_URL}/product/widget-pro",
        name="Widget Pro - Premium Edition",
        description="The best widget for your needs...",
        sku="WGT-PRO-001",
        brand="AutoTools",
        price="29.99",
        currency="USD",
        availability="InStock",
        rating="4.7",
        review_count="128"
    )
    print_schema(product)
    
    # Breadcrumb Schema
    print("  🔖 Breadcrumb Schema:")
    breadcrumb = gen.generate_breadcrumb(
        url=f"{SITE_URL}/blog/seo-guide",
        items=[
            {"name": "Home", "url": "/"},
            {"name": "Blog", "url": "/blog"},
            {"name": "SEO Guide", "url": "/blog/seo-guide"}
        ]
    )
    print_schema(breadcrumb)
    
    # WebSite Schema
    print("  🌐 WebSite Schema:")
    website = gen.generate_website(search_url=f"{SITE_URL}/?s={{search_term_string}}")
    print_schema(website)
    
    # ===== 第2步：从真实站点扫描并生成 =====
    print("=" * 60)
    print("  第2步：扫描真实站点，生成 Schema")
    print("=" * 60)
    
    analyzer = SEOAnalyzer(SITE_URL, wp_web_root=WEB_ROOT)
    
    # 获取前3个页面
    urls_data = analyzer.get_all_urls(limit=3)
    
    all_schema_results = {}
    
    for page_info in urls_data[:3]:
        url = page_info["url"]
        title = page_info.get("title", "")
        
        print(f"\n  📄 页面: {url}")
        print(f"     Title: {title[:50] if title else '(空)'}")
        
        # 获取页面内容
        import requests
        try:
            resp = requests.get(url, timeout=10, verify=False)
            html = resp.text
            
            # 提取 H1
            h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
            h1s = [h.strip() for h in h1s]
            
            # 提取图片
            imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
            
            # 为页面生成 Schema
            schemas = gen.generate_for_wordpress_page(
                url=url,
                title=title or (h1s[0] if h1s else "Untitled"),
                page_content=html,
                h1s=h1s,
                images=imgs
            )
            
            all_schema_results[url] = schemas
            
            for s in schemas:
                print_schema(s)
            
            # 验证
            valid = gen.validate_schema(schemas[0]) if schemas else False
            print(f"     ✅ 验证: {'通过' if valid else '有警告'}")
            
        except Exception as e:
            print(f"     ❌ 错误: {e}")
    
    # ===== 第3步：导出注入代码 =====
    print("\n" + "=" * 60)
    print("  第3步：导出可注入 HTML 的代码")
    print("=" * 60)
    
    for url, schemas in all_schema_results.items():
        injection = gen.export_injection_code(schemas)
        if injection:
            print(f"\n  📄 {url}")
            print("  " + "-" * 50)
            print(f"  {injection[:200]}...")
    
    # ===== 第4步：统计 =====
    print("\n" + "=" * 60)
    print("  第4步：Schema 生成统计")
    print("=" * 60)
    
    type_counts = {}
    valid_count = 0
    for s in gen.generated:
        t = s.page_type
        type_counts[t] = type_counts.get(t, 0) + 1
        if gen.validate_schema(s):
            valid_count += 1
    
    print(f"\n  总生成: {len(gen.generated)} 个 Schema")
    for t, c in type_counts.items():
        print(f"    • {t}: {c} 个")
    print(f"  验证通过: {valid_count}/{len(gen.generated)}")
    
    # ===== 完成 =====
    print("\n" + "=" * 60)
    print("  ✅ Schema.org 生成完成")
    print("=" * 60)
    print(f"""
  产出：
    • {len(gen.generated)} 个 Schema 生成
    • {valid_count} 个通过验证
    • 支持类型: Article / Product / FAQ / Breadcrumb / WebSite / Organization
    
  技术实现：
    ✅ Schema类型自动检测
    ✅ 多Schema组合注入
    ✅ FAQ自动提取
    ✅ 面包屑自动生成
    ✅ Google结构化数据验证
    
  可扩展：
    → WooCommerce产品Schema
    → 本地商家LocalBusiness
    → 事件Event Schema
    → 视频Video Schema
""")

if __name__ == "__main__":
    import re
    main()
