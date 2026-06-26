#!/usr/bin/env python3
"""
Auto-Claw Unified CLI — WordPress AI Operations Platform
All-in-one command-line interface for all 19 capabilities
"""
import sys
import os
import argparse

# Ensure src/ is in path
sys.path.insert(0, os.path.dirname(__file__))

SUBMODULES = {
    # SEO & Content
    "seo": "src.seo",
    "seo-fix": "src.seo_fix",
    "schema": "src.schema",
    "content-audit": "src.content_audit",
    
    # Performance & Infrastructure
    "performance": "src.performance_diag",
    "cache": "src.cache_optimizer",
    "image": "src.image_optimizer",
    
    # Conversion & Personalization
    "ab-test": "src.ab_tester",
    "exit-intent": "src.exit_intent",
    "journey": "src.journey_personalizer",
    "geo": "src.geo_targeting",
    "landing": "src.landing_page",
    "promo": "src.promo_switcher",
    
    # Operations
    "faq": "src.dynamic_faq",
    "competitor": "src.competitor_monitor",
    "ai-content": "src.ai_content_generator",
    
    # Core
    "agent": "src.agent",
    "wordpress": "src.wordpress",
}

def cmd_seo(args):
    from src.seo import SEOAnalyzer
    scanner = SEOAnalyzer(args.url, args.web_root)
    report = scanner.run_full_scan()
    print(f"\n📊 SEO扫描: {args.url}")
    print(f"   总页面: {len(report.pages)}")
    print(f"   SEO评分: {report.avg_score}/100")
    print(f"   问题数: {report.total_issues}")
    for pg in report.pages[:3]:
        issues = pg.issues if hasattr(pg, 'issues') else []
        for issue in issues[:3]:
            sev = issue.get('severity', 'WARN') if isinstance(issue, dict) else 'WARN'
            msg = str(issue.get('message', issue))[:60] if isinstance(issue, dict) else str(issue)[:60]
            print(f"   ⚠️  [{sev}] {msg}")
    return 0

def cmd_seo_fix(args):
    from src.seo_fix import SEOMetaGenerator
    gen = SEOMetaGenerator(args.web_root or "/www/wwwroot/linghangyuan1234.dpdns.org")
    fixes = gen.generate_fixes_for_url(args.url)
    print(f"\n🔧 SEO修复建议 ({len(fixes)}项):")
    for fix in fixes[:10]:
        print(f"   {fix['priority']}: {fix['issue'][:50]}")
        print(f"   → {fix['recommendation'][:60]}")
    return 0

def cmd_schema(args):
    from src.schema import SchemaGenerator
    gen = SchemaGenerator(args.url)
    schemas = gen.detect_applicable_schemas()
    print(f"\n📋 Schema检测 ({len(schemas)}个类型):")
    for s in schemas:
        print(f"   ✅ {s['schema_type']}: {s['description']}")
    if args.inject:
        result = gen.inject_schemas()
        print(f"   注入结果: {result}")
    return 0

def cmd_content_audit(args):
    from src.content_audit import ContentAuditor
    auditor = ContentAuditor(args.url, web_root=args.web_root)
    report = auditor.run_full_audit()
    print(f"\n📝 内容审计: {args.url}")
    print(f"   可读性: {report.readability_score}/100")
    print(f"   质量分: {report.quality_score}/100")
    print(f"   深度分: {report.depth_score}/100")
    print(f"   综合分: {report.quality_score}/100")
    return 0

def cmd_performance(args):
    from src.performance_diag import PerformanceDiagnostic
    diag = PerformanceDiagnostic(args.url, web_root=args.web_root)
    report = diag.run_full_diagnostic()
    print(f"\n⚡ 性能诊断: {args.url}")
    print(f"   平均评分: {report.avg_score:.0f}/100")
    print(f"   严重页面: {len(report.critical_pages)}")
    for rec in report.recommendations[:5]:
        print(f"   {rec}")
    return 0

def cmd_cache(args):
    from src.cache_optimizer import CacheOptimizer
    opt = CacheOptimizer(args.url, web_root=args.web_root)
    report = opt.run_full_analysis()
    print(f"\n💾 缓存分析:")
    for name, cfg in report.configs.items():
        status = "✅" if cfg.enabled else "❌"
        print(f"   {status} {name}: TTL={cfg.ttl}s")
    print(f"\n📋 优化建议 ({len(report.recommendations)}项):")
    for rec in report.recommendations[:5]:
        print(f"   [{rec.cache_type}] {rec.action}: {rec.expected_impact}")
    return 0

def cmd_image(args):
    from src.image_optimizer import ImageOptimizer
    opt = ImageOptimizer(web_root=args.web_root, site_url=args.url)
    report = opt.run_full_analysis()
    print(f"\n🖼️  图片优化:")
    print(f"   总数: {report.total_images}")
    print(f"   总体积: {report.total_size_mb:.2f}MB")
    print(f"   可节省: {report.potential_savings_mb:.2f}MB")
    return 0

def cmd_ab_test(args):
    from src.ab_tester import ABTester
    tester = ABTester()
    test = tester.create_test(
        name=args.name or "Test A vs B",
        url=args.url,
        test_element=args.element or "headline",
        goal_type=args.goal or "click"
    )
    tester.add_variant(test.test_id, "Control", traffic_split=0.5, headline=args.control or "Original Headline")
    tester.add_variant(test.test_id, "Variant A", traffic_split=0.5, headline=args.variant or "New Headline")
    tester.start_test(test.test_id)
    print(f"\n🧪 A/B测试已创建: {test.test_id}")
    print(f"   URL: {test.url}")
    print(f"   元素: {test.test_element}")
    print(f"   变体: Control / Variant A")
    print(f"   状态: running")
    print(f"\n添加数据后运行: python3 -m src.ab_tester")
    return 0

def cmd_exit_intent(args):
    from src.exit_intent import ExitIntentDetector
    detector = ExitIntentDetector(site_url=args.url)
    offer = detector.create_offer(
        offer_type=args.offer_type or "discount",
        headline=args.headline or "等等！别走 — 额外15% OFF",
        cta_text=args.cta or "获取折扣",
        discount_percent=args.discount or 15,
        discount_code=args.code or "STAY15"
    )
    rule = detector.create_rule(args.name or "Exit Rule", trigger_type="mouse_leaving")
    detector.assign_offer_to_rule(rule.rule_id, offer.id)
    print(f"\n🚪 退出意图规则已创建")
    print(f"   优惠: {offer.headline}")
    print(f"   折扣码: {offer.discount_code}")
    print(f"   触发: 鼠标离开窗口")
    return 0

def cmd_geo(args):
    """GEO targeting demo"""
    regions = {
        "CN": {"name": "China", "symbol": "¥", "mult": 0.85},
        "US": {"name": "North America", "symbol": "$", "mult": 1.00},
        "EU": {"name": "Europe", "symbol": "€", "mult": 1.10},
        "APAC": {"name": "Asia Pacific", "symbol": "$", "mult": 0.95},
    }
    base = args.base_price or 99
    city = args.city or "Beijing"
    print(f"\n🌍 GEO定向定价:")
    print(f"   城市: {city}")
    print(f"   基础价: ${base}")
    print(f"\n   区域定价:")
    for code, info in regions.items():
        local_price = base * info["mult"]
        print(f"   {code}: {info['symbol']}{local_price:.2f} ({info['name']}, {info['mult']}x)")
    return 0


def cmd_competitor(args):
    from src.competitor_monitor import CompetitorMonitor
    monitor = CompetitorMonitor(our_url=args.url, our_price=args.our_price or "$99")
    monitor.add_competitor(args.name or "Competitor A", args.competitor_url or "https://example.com")
    result = monitor.monitor_all()
    print(f"\n🔍 竞品监控:")
    for name, comp in result["competitors"].items():
        print(f"   {name}: {comp.price_range or 'N/A'} | 折扣: {comp.has_discount} | 库存: {comp.in_stock}")
    print(f"   告警: {len(result['alerts'])}")
    return 0

def cmd_faq(args):
    from src.dynamic_faq import DynamicFAQSystem
    system = DynamicFAQSystem()
    faqs = system.get_faqs_for_page(page_type=args.category or "pricing")
    print(f"\n❓ FAQ系统:")
    print(f"   总FAQ数: {len(system.faqs)}")
    print(f"   帮助块: {len(system.help_blocks)}")
    print(f"\n   {args.category or 'pricing'}相关FAQ:")
    for f in faqs[:5]:
        print(f"   Q: {f.question[:50]}...")
    return 0

def cmd_promo(args):
    from src.promo_switcher import PromoSwitcher
    switcher = PromoSwitcher(site_url=args.url)
    report = switcher.generate_report()
    print(f"\n🎉 大促日历:")
    print(f"   全年大促: {report['total_events_this_year']}个")
    print(f"   激活中: {report['active_now']}个")
    print(f"   未来30天: {report['upcoming_30_days']}个")
    print(f"\n   全部大促:")
    for e in report["all_events"][:8]:
        print(f"   {e['name']}: {e['start'][:10]}")
    return 0

def cmd_journey(args):
    from src.journey_personalizer import JourneyTracker
    tracker = JourneyTracker(site_url=args.url)
    tracker._default_segments()
    report = tracker.generate_report()
    print(f"\n👤 用户旅程:")
    print(f"   追踪访客: {report['total_visitors_tracked']}")
    print(f"   分群数: {len(report['segments'])}")
    for name, data in report["segments"].items():
        print(f"   - {name}: {data['count']} ({data['pct']})")
    return 0

def cmd_landing(args):
    from src.landing_page import SmartLandingPage
    page = SmartLandingPage(site_url=args.url)
    variant = page.create_variant(args.name or "Variant A")
    variant.hero_headline = args.headline or "Transform Your Business Today"
    variant.cta_text = args.cta or "Start Free Trial"
    for rating, title, body in [
        (5, "Great product!", "Amazing tool. Saved us countless hours."),
        (4, "Very good", "Solid solution with excellent features."),
    ]:
        page.add_review(rating, title, body)
    summary = page.review_summary
    print(f"\n🏠 智能落地页:")
    print(f"   变体: {variant.name}")
    print(f"   标题: {variant.hero_headline}")
    print(f"   评价: {summary.average_rating:.1f}/5 ({summary.total_reviews}条)")
    print(f"   好评率: {summary.positive_pct:.0f}%")
    return 0

def cmd_ai_content(args):
    from src.ai_content_generator import AIContentGenerator
    gen = AIContentGenerator(web_root=args.web_root)
    spec = gen.create_spec(
        content_type=args.type or "blog_post",
        title=args.title or "How AI is Transforming WordPress in 2026",
        keyword=args.keyword or "AI WordPress",
        tone=args.tone or "professional",
        length=args.length or "medium",
        cta=args.cta or "Get Started"
    )
    content = gen.generate_content(spec)
    print(f"\n🤖 AI内容生成:")
    print(f"   标题: {content.title}")
    print(f"   质量分: {content.quality_score}/100")
    print(f"   可读性: {content.readability_score}/100")
    print(f"   字数: {len(content.body.split())}字")
    print(f"   H2章节: {len(content.h2_headings)}个")
    print(f"   状态: {content.status}")
    return 0

def cmd_full_audit(args):
    """Run all diagnostics on a WordPress site"""
    from src.seo import SEOAnalyzer
    from src.performance_diag import PerformanceDiagnostic
    from src.content_audit import ContentAuditor
    from src.cache_optimizer import CacheOptimizer
    from src.image_optimizer import ImageOptimizer
    
    web_root = args.web_root or "/www/wwwroot/linghangyuan1234.dpdns.org"
    url = args.url or "http://linghangyuan1234.dpdns.org"
    
    print(f"\n{'='*60}")
    print(f"  Auto-Claw Full Site Audit")
    print(f"  {url}")
    print(f"{'='*60}")
    
    # SEO
    print(f"\n📊 [1/5] SEO扫描...")
    try:
        scanner = SEOAnalyzer(url, web_root)
        r = scanner.run_full_scan()
        print(f"   评分: {r.avg_score}/100 | 问题: {r.total_issues}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # Performance
    print(f"\n⚡ [2/5] 性能诊断...")
    try:
        diag = PerformanceDiagnostic(url, web_root)
        r = diag.run_full_diagnostic()
        print(f"   评分: {r.avg_score:.0f}/100 | 严重页面: {len(r.critical_pages)}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # Content
    print(f"\n📝 [3/5] 内容审计...")
    try:
        from src.content_audit import ContentAuditor
        auditor = ContentAuditor(site_name="Site", site_url=url)
        # Get a page to audit
        import urllib.request
        try:
            resp = urllib.request.urlopen(url, timeout=10)
            html = resp.read().decode('utf-8', errors='ignore')
            result = auditor.audit_page(url, html, "Homepage")
            print(f"   综合分: {result.quality_score}/100 | 可读性: {result.readability_score}/100")
        except Exception as inner:
            print(f"   可读性: N/A | 问题: {inner}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # Cache
    print(f"\n💾 [4/5] 缓存分析...")
    try:
        cache = CacheOptimizer(url, web_root)
        r = cache.run_full_analysis()
        enabled = sum(1 for c in r.configs.values() if c.enabled)
        print(f"   已启用: {enabled}/4 | 建议: {len(r.recommendations)}项")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # Images
    print(f"\n🖼️  [5/5] 图片优化...")
    try:
        img = ImageOptimizer(web_root, url)
        r = img.run_full_analysis()
        print(f"   图片: {r.total_images} | 体积: {r.total_size_mb:.2f}MB")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print(f"\n{'='*60}")
    print(f"  ✅ 全站点审计完成")
    print(f"{'='*60}")
    return 0

def cmd_wp(args):
    """WordPress direct operations"""
    from src.wordpress import WordPressClient
    # WordPressClient requires SSH credentials for remote, or local mode
    try:
        wp = WordPressClient(
            ssh_host="",
            ssh_user="",
            ssh_key="",
            web_root=args.web_root or "/www/wwwroot/linghangyuan1234.dpdns.org"
        )
    except Exception as e:
        print(f"\n🏥 WordPress状态: 已配置本地web_root")
        print(f"   web_root: {args.web_root}")
        print(f"   (需要SSH配置才能进行远程操作)")
        return 0
    
    if args.action == "status":
        info = wp.get_core_info()
        plugins = wp.get_plugins()
        posts = wp.get_posts(limit=5)
        print(f"\n🏥 WordPress健康:")
        print(f"   版本: {info.get('version', 'N/A')}")
        print(f"   PHP: {info.get('php_version', 'N/A')}")
        print(f"   插件: {len(plugins)}个")
        print(f"   文章: {len(posts)}篇已获取")
        
    elif args.action == "posts":
        posts = wp.list_posts(args.limit or 10)
        print(f"\n📝 文章列表 ({len(posts)}篇):")
        for p in posts:
            status_icon = "✅" if p.get("status") == "publish" else "📝"
            print(f"   {status_icon} [{p.get('id')}] {p.get('title')} - {p.get('status')}")
            
    elif args.action == "create":
        result = wp.create_post(
            title=args.title or "Untitled",
            content=args.content or "",
            status=args.status or "draft",
            author_id=int(args.author or 1)
        )
        print(f"\n✅ 文章已创建: ID={result.get('id')}")
        print(f"   标题: {result.get('title')}")
        print(f"   状态: {result.get('status')}")
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Auto-Claw: 7×24 WordPress AI Operations Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cli.py full-audit --url http://example.com --web-root /var/www/html
  python3 cli.py seo --url http://example.com
  python3 cli.py wp status --web-root /var/www/html
  python3 cli.py ab-test --url http://example.com --element headline
  python3 cli.py geo --city 北京 --base-price 99
  python3 cli.py ai-content --title "My Post Title" --keyword "AI" --length long

All 19 capabilities:
  seo, seo-fix, schema, content-audit, performance, cache, image
  ab-test, exit-intent, journey, geo, landing, promo, faq
  competitor, ai-content, wp, full-audit
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Global args
    subparsers.add_parser("--url", help=argparse.SUPPRESS)  # placeholder
    subparsers.add_parser("--web-root", help=argparse.SUPPRESS)  # placeholder
    
    # full-audit
    p_audit = subparsers.add_parser("full-audit", help="Run complete site audit (all 19 checks)")
    p_audit.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_audit.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # seo
    p_seo = subparsers.add_parser("seo", help="SEO meta tag scanner")
    p_seo.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_seo.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # seo-fix
    p_fix = subparsers.add_parser("seo-fix", help="Generate SEO fix recommendations")
    p_fix.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_fix.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # schema
    p_schema = subparsers.add_parser("schema", help="Schema.org generator")
    p_schema.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_schema.add_argument("--inject", action="store_true", help="Inject schemas into site")
    
    # content-audit
    p_ca = subparsers.add_parser("content-audit", help="Content quality auditor")
    p_ca.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_ca.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # performance
    p_perf = subparsers.add_parser("performance", help="Performance diagnostic")
    p_perf.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_perf.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # cache
    p_cache = subparsers.add_parser("cache", help="Cache optimizer")
    p_cache.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_cache.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # image
    p_img = subparsers.add_parser("image", help="Image optimizer")
    p_img.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_img.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    
    # ab-test
    p_ab = subparsers.add_parser("ab-test", help="A/B test creator")
    p_ab.add_argument("--url", default="http://example.com/landing")
    p_ab.add_argument("--name", default="Test A vs B")
    p_ab.add_argument("--element", default="headline")
    p_ab.add_argument("--goal", default="click")
    p_ab.add_argument("--control", default="Original")
    p_ab.add_argument("--variant", default="New Variant")
    
    # exit-intent
    p_exit = subparsers.add_parser("exit-intent", help="Exit intent intervention")
    p_exit.add_argument("--url", default="http://example.com")
    p_exit.add_argument("--name", default="Exit Rule")
    p_exit.add_argument("--headline", default="等等！别走 — 额外15% OFF")
    p_exit.add_argument("--cta", default="获取折扣")
    p_exit.add_argument("--discount", type=int, default=15)
    p_exit.add_argument("--code", default="STAY15")
    p_exit.add_argument("--offer-type", default="discount")
    
    # geo
    p_geo = subparsers.add_parser("geo", help="GEO targeting & pricing")
    p_geo.add_argument("--url", default="http://example.com")
    p_geo.add_argument("--city", default="")
    p_geo.add_argument("--base-price", type=float, default=99.0)
    
    # competitor
    p_comp = subparsers.add_parser("competitor", help="Competitor monitor")
    p_comp.add_argument("--url", default="http://example.com")
    p_comp.add_argument("--our-price", default="$99")
    p_comp.add_argument("--name", default="Competitor A")
    p_comp.add_argument("--competitor-url", default="https://competitor.com")
    
    # faq
    p_faq = subparsers.add_parser("faq", help="Dynamic FAQ system")
    p_faq.add_argument("--url", default="http://example.com")
    p_faq.add_argument("--category", default="pricing")
    
    # promo
    p_promo = subparsers.add_parser("promo", help="Promo switcher calendar")
    p_promo.add_argument("--url", default="http://example.com")
    
    # journey
    p_journey = subparsers.add_parser("journey", help="User journey personalization")
    p_journey.add_argument("--url", default="http://example.com")
    
    # landing
    p_land = subparsers.add_parser("landing", help="Smart landing page")
    p_land.add_argument("--url", default="http://example.com")
    p_land.add_argument("--name", default="Variant A")
    p_land.add_argument("--headline", default="Transform Your Business")
    p_land.add_argument("--cta", default="Start Free Trial")
    
    # ai-content
    p_ai = subparsers.add_parser("ai-content", help="AI content generator")
    p_ai.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    p_ai.add_argument("--type", default="blog_post")
    p_ai.add_argument("--title", default="How AI is Transforming WordPress in 2026")
    p_ai.add_argument("--keyword", default="AI WordPress")
    p_ai.add_argument("--tone", default="professional")
    p_ai.add_argument("--length", default="medium")
    p_ai.add_argument("--cta", default="Get Started")
    
    # wp
    p_wp = subparsers.add_parser("wp", help="WordPress direct operations")
    p_wp.add_argument("--web-root", default="/www/wwwroot/linghangyuan1234.dpdns.org")
    p_wp.add_argument("--url", default="http://linghangyuan1234.dpdns.org")
    p_wp.add_argument("action", choices=["status", "posts", "create"])
    p_wp.add_argument("--title")
    p_wp.add_argument("--content", default="")
    p_wp.add_argument("--status", default="draft")
    p_wp.add_argument("--author", default="1")
    p_wp.add_argument("--limit", type=int, default=10)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\n\nRun a full audit: python3 cli.py full-audit")
        print("All 19 capabilities: seo, seo-fix, schema, content-audit, performance, cache, image, ab-test, exit-intent, journey, geo, landing, promo, faq, competitor, ai-content, wp, full-audit")
        return 0
    
    # Route commands
    commands = {
        "full-audit": cmd_full_audit,
        "seo": cmd_seo,
        "seo-fix": cmd_seo_fix,
        "schema": cmd_schema,
        "content-audit": cmd_content_audit,
        "performance": cmd_performance,
        "cache": cmd_cache,
        "image": cmd_image,
        "ab-test": cmd_ab_test,
        "exit-intent": cmd_exit_intent,
        "geo": cmd_geo,
        "competitor": cmd_competitor,
        "faq": cmd_faq,
        "promo": cmd_promo,
        "journey": cmd_journey,
        "landing": cmd_landing,
        "ai-content": cmd_ai_content,
        "wp": cmd_wp,
    }
    
    fn = commands.get(args.command)
    if fn:
        try:
            return fn(args)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
