#!/usr/bin/env python3
"""
Dynamic FAQ Generator — 综合演示
基于已有WordPress内容，自动提取FAQ并生成带Schema的FAQ页面
"""
import sys
sys.path.insert(0, "src")

from dynamic_faq import DynamicFAQGenerator, FAQConfig

def main():
    generator = DynamicFAQGenerator("https://example.com")

    # ===== 模拟内容1：产品页面 =====
    product_html = """
    <article>
        <h1>Auto-Claw WordPress AI Agent</h1>

        <h2>What is Auto-Claw?</h2>
        <p>Auto-Claw is an AI-powered WordPress management agent that runs your site 24/7 without breaks.
        It automates SEO optimization, content creation, security monitoring, and performance tuning.</p>

        <h2>How do I install Auto-Claw?</h2>
        <p>Installation takes less than 5 minutes. Simply upload the plugin, activate it, and connect your WordPress site.
        No technical knowledge required. Our AI will start analyzing your site immediately.</p>
        <p>For SSH-based installations, use our CLI tool: <code>npx auto-claw connect --url=https://yoursite.com</code></p>

        <h2>Does Auto-Claw work with shared hosting?</h2>
        <p>Yes! Auto-Claw works with any WordPress hosting including shared, VPS, dedicated, and managed WordPress hosting.
        For best performance, we recommend PHP 8.1+ and at least 512MB RAM.</p>

        <h3>What about WordPress.com hosting?</h3>
        <p>Auto-Claw requires self-hosted WordPress (.org) as it needs filesystem access for plugin installation
        and mu-plugin deployment. WordPress.com Business plan can be used.</p>

        <h2>How much does Auto-Claw cost?</h2>
        <p>Plans start at $49/month for 1 site, $149/month for 3 sites, and enterprise pricing for unlimited sites.
        All plans include unlimited AI operations, 24/7 monitoring, and automatic updates.</p>

        <h2>Is my data secure?</h2>
        <p>Absolutely. Auto-Claw uses read-only API access by default. Your credentials are stored in HashiCorp Vault,
        never in AI context. All operations are audit-logged and reversible.</p>

        <h2>Can I try it before buying?</h2>
        <p>Yes! We offer a 14-day free trial with full access to all features. No credit card required.</p>
    </article>
    """

    # ===== 模拟内容2：博客文章 =====
    blog_html = """
    <article>
        <h1>How to 10x Your WordPress SEO with AI</h1>

        <h2>Why is WordPress SEO important?</h2>
        <p>Search engine optimization is crucial for driving organic traffic to your WordPress site.
        With proper SEO, you can attract visitors without paying for ads.</p>

        <h2>How can AI improve my WordPress SEO?</h2>
        <p>AI can analyze your content in seconds, identify optimization opportunities, and even
        generate meta descriptions and schema markup automatically. Auto-Claw does all of this 24/7.</p>
        <p>Key areas where AI helps: keyword research, content optimization, technical SEO fixes,
        schema markup, and competitor analysis.</p>

        <h3>What is Schema markup and why do I need it?</h3>
        <p>Schema.org markup helps search engines understand your content better, potentially
        earning you rich snippets in search results. Auto-Claw adds it automatically.</p>

        <h2>How long does SEO take to show results?</h2>
        <p>SEO is a long-term strategy. You typically see measurable results in 3-6 months of consistent effort.
        However, Auto-Claw's automated approach accelerates this by making weekly improvements automatically.</p>

        <strong>Can I use Auto-Claw alongside my existing SEO plugin?</strong>
        <p>Yes! Auto-Claw works alongside Yoast SEO, Rank Math, or All in One SEO.
        It complements rather than replaces your existing tools.</p>
    </article>
    """

    print("=" * 60)
    print("Dynamic FAQ Generator 演示")
    print("=" * 60)

    # 提取FAQ
    print("\n📄 从产品页面提取FAQ...")
    faqs1 = generator.extract_questions_from_html(product_html, "https://example.com/product/auto-claw")
    print(f"   提取了 {len(faqs1)} 条FAQ")

    print("\n📄 从博客文章提取FAQ...")
    faqs2 = generator.extract_questions_from_html(blog_html, "https://example.com/blog/wordpress-seo")
    print(f"   提取了 {len(faqs2)} 条FAQ")

    # 合并后去重
    print(f"\n📊 FAQ统计：共 {len(generator.faq_items)} 条")
    for i, faq in enumerate(generator.faq_items, 1):
        score_bar = "▓" * int(faq.relevance_score * 10) + "░" * (10 - int(faq.relevance_score * 10))
        print(f"  {i:2d}. [{score_bar}] {faq.question[:55]}...")

    # 生成FAQ页面
    print("\n" + "=" * 60)
    print("🛠️ 生成FAQ页面...")
    page = generator.generate_faq_page(
        title="Auto-Claw 常见问题解答",
        slug="faq",
        categories=["功能", "安装", "定价", "安全"],
        config=FAQConfig(min_relevance_score=0.5, max_faqs_per_page=20)
    )

    print(f"\n📄 页面标题: {page.title}")
    print(f"   包含FAQ: {len(page.faqs)} 条")
    print(f"   分类: {', '.join(page.categories)}")

    # 生成HTML
    html = generator.generate_html(page, include_schema=True)
    print(f"\n📄 生成HTML长度: {len(html)} 字符")

    # 检查Schema
    has_schema = "FAQPage" in html
    print(f"   Schema.org FAQ markup: {'✅ 已包含' if has_schema else '❌ 未包含'}")

    # 输出摘要
    print("\n" + "=" * 60)
    print(generator.summary())
    print("=" * 60)

    # 保存HTML（可选）
    output_path = "demo_faq_output.html"
    with open(output_path, "w") as f:
        f.write(html)
    print(f"\n💾 FAQ页面已保存: {output_path}")
    print(f"   打开浏览器查看: file://$(pwd)/{output_path}")


if __name__ == "__main__":
    main()
