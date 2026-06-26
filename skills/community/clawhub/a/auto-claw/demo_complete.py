#!/usr/bin/env python3
"""
Auto-Claw Complete Demo — All 19 Capabilities in One Script
Demonstrates full value on the real WordPress site
"""
import sys
import os
import time

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

SITE = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

def banner(text):
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}  {text}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def section(num, text):
    print(f"{YELLOW}▶ [{num}/19] {BOLD}{text}{RESET}")

def success(text):
    print(f"  {GREEN}✅ {text}{RESET}")

def info(text):
    print(f"  {BLUE}ℹ {text}{RESET}")

def warn(text):
    print(f"  {YELLOW}⚠ {text}{RESET}")

def error(text):
    print(f"  {RED}❌ {text}{RESET}")

def main():
    print(f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════════════════╗
║         Auto-Claw Complete Demo — All 19 Capabilities   ║
║         Real WordPress Site: {SITE:<27}║
╚══════════════════════════════════════════════════════════╝
{RESET}
""")

    # Add src to path
    sys.path.insert(0, os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    # ========== 1. SEO Meta Tag Scanner ==========
    banner("AI原生独立站 — SEO")
    try:
        from src.seo import SEOAnalyzer
        section(1, "SEO Meta标签扫描")
        scanner = SEOAnalyzer(SITE, WEB_ROOT)
        report = scanner.run_full_scan(max_pages=5)
        success(f"扫描 {len(report.pages)} 个页面")
        success(f"SEO评分: {report.avg_score:.0f}/100")
        success(f"发现 {report.total_issues} 个问题")
        for pg in report.pages[:3]:
            if hasattr(pg, 'issues') and pg.issues:
                for issue in pg.issues[:2]:
                    if isinstance(issue, dict):
                        warn(f"  [{issue.get('severity', 'WARN')}] {issue.get('message', str(issue))[:50]}")
    except Exception as e:
        error(f"SEO扫描失败: {e}")

    # ========== 2. SEO Fix Generator ==========
    section(2, "SEO优化建议生成")
    try:
        from src.seo_fix import SEOMetaGenerator
        if report.pages:
            page = report.pages[0]
            gen = SEOMetaGenerator(page)
            success(f"标题建议: {gen.suggest_title()[:50]}")
            success(f"描述建议: {gen.suggest_description()[:60]}")
            og = gen.suggest_og_tags()
            success(f"OG标签: og:title={og.get('og:title', 'N/A')[:30]}")
        else:
            info("无可用页面数据")
    except Exception as e:
        error(f"SEO修复生成失败: {e}")

    # ========== 3. Schema.org Generator ==========
    section(3, "Schema.org生成")
    try:
        from src.schema import SchemaGenerator
        gen = SchemaGenerator(site_name="Auto Claw Site", site_url=SITE)
        org = gen.generate_organization(name="Auto Claw", url=SITE)
        web = gen.generate_website()
        success(f"Organization Schema: {org.json_ld.get('@type', 'N/A')}")
        success(f"WebSite Schema: {web.json_ld.get('@type', 'N/A')}")
        success(f"JSON-LD有效: {'✅' if org.json_ld else '❌'}")
    except Exception as e:
        error(f"Schema生成失败: {e}")

    # ========== 4. Content Quality Auditor ==========
    section(4, "内容质量审计")
    try:
        import urllib.request
        resp = urllib.request.urlopen(SITE, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')

        from src.content_audit import ContentAuditor
        auditor = ContentAuditor(site_name="Test Site", site_url=SITE)
        result = auditor.audit_page(SITE, html, "Homepage")

        if hasattr(result, 'overall_score'):
            success(f"内容质量: {result.overall_score}/100")
        if hasattr(result, 'readability_score'):
            success(f"可读性: {result.readability_score}/100")
        success(f"字数: {result.word_count if hasattr(result, 'word_count') else 'N/A'}")
    except Exception as e:
        error(f"内容审计失败: {e}")

    # ========== 5. Performance Diagnostic ==========
    banner("AI原生独立站 — 性能")
    section(5, "性能诊断")
    try:
        from src.performance_diag import PerformanceDiagnostic
        diag = PerformanceDiagnostic(SITE, WEB_ROOT)
        report = diag.run_full_diagnostic()
        success(f"性能评分: {report.avg_score:.0f}/100")
        success(f"严重页面: {len(report.critical_pages)}")
        for rec in report.recommendations[:3]:
            info(f"  {rec[:60]}")
    except Exception as e:
        error(f"性能诊断失败: {e}")

    # ========== 6. Cache Optimizer ==========
    section(6, "缓存策略优化")
    try:
        from src.cache_optimizer import CacheOptimizer
        opt = CacheOptimizer(SITE, WEB_ROOT)
        report = opt.run_full_analysis()
        enabled = sum(1 for c in report.configs.values() if c.enabled)
        success(f"缓存已启用: {enabled}/4")
        success(f"优化建议: {len(report.recommendations)}项")
        for rec in report.recommendations[:3]:
            if hasattr(rec, 'expected_impact'):
                info(f"  {rec.cache_type}: {rec.expected_impact[:50]}")
    except Exception as e:
        error(f"缓存优化失败: {e}")

    # ========== 7. Image Optimizer ==========
    section(7, "图片自动优化")
    try:
        from src.image_optimizer import ImageOptimizer
        opt = ImageOptimizer(WEB_ROOT, SITE)
        report = opt.run_full_analysis()
        success(f"图片总数: {report.total_images}")
        success(f"总体积: {report.total_size_mb:.2f}MB")
        success(f"可节省: {report.potential_savings_mb:.2f}MB")
    except Exception as e:
        error(f"图片优化失败: {e}")

    # ========== 8. A/B Testing Engine ==========
    banner("转化率飞轮")
    section(8, "A/B测试引擎")
    try:
        from src.ab_tester import ABTester
        tester = ABTester()
        test = tester.create_test(
            name="Hero Headline Test",
            url=f"{SITE}/landing",
            test_element="headline",
            goal_type="click"
        )
        tester.add_variant(test.test_id, "Control", traffic_split=0.5,
                          headline="Original Headline That Converts at 3%")
        tester.add_variant(test.test_id, "Variant A", traffic_split=0.5,
                          headline="Urgency Headline: 50% Off Today Only!")
        tester.start_test(test.test_id)

        # Simulate data
        test.variants[0].visitors = 500
        test.variants[0].conversions = 15
        test.variants[1].visitors = 500
        test.variants[1].conversions = 23

        result = tester.analyze_test(test.test_id)
        success(f"A/B测试已创建: {test.test_id[:8]}")
        success(f"变体: Control vs Variant A")
        success(f"提升: {result.lift*100:.1f}% (置信度: {result.confidence:.1%})")
        success(f"建议: {result.recommendation[:50]}")
    except Exception as e:
        error(f"A/B测试失败: {e}")

    # ========== 9. Exit Intent Intervention ==========
    section(9, "退出意图干预")
    try:
        from src.exit_intent import ExitIntentDetector
        detector = ExitIntentDetector(site_url=SITE)
        offer = detector.create_offer(
            offer_type="discount",
            headline="等等！别走 — 额外15% OFF",
            cta_text="获取折扣",
            discount_percent=15,
            discount_code="STAY15"
        )
        rule = detector.create_rule("Cart Exit", trigger_type="mouse_leaving",
                                    page_types=["cart", "checkout"])
        detector.assign_offer_to_rule(rule.rule_id, offer.id)

        # Simulate data
        offer.shown_count = 1000
        offer.converted_count = 45

        report = detector.generate_report()
        success(f"挽留优惠已创建: {offer.headline}")
        success(f"挽回率: {report['recovery_rate']}")
        success(f"转化数: {report['converted']}")
    except Exception as e:
        error(f"退出意图失败: {e}")

    # ========== 10. User Journey Personalization ==========
    section(10, "用户旅程个性化")
    try:
        from src.journey_personalizer import JourneyTracker
        tracker = JourneyTracker(site_url=SITE)

        # Simulate visitor journey
        vid = "demo_visitor_001"
        tracker.track_event(vid, "page_view", page_url="/", scroll_depth=30)
        tracker.track_event(vid, "page_view", page_url="/products", scroll_depth=70)
        tracker.track_event(vid, "add_to_cart", page_url="/cart")

        summary = tracker.get_journey_summary(vid)
        success(f"用户分群: {summary['segment']}")
        success(f"页面浏览: {summary['page_views']}")
        success(f"滚动深度: {summary['max_scroll_depth']}%")

        headline = tracker.generate_personalized_headline(summary['segment'])
        info(f"个性化标题: {headline[:50]}")
    except Exception as e:
        error(f"用户旅程失败: {e}")

    # ========== 11. GEO Targeting ==========
    section(11, "GEO动态页面+定价")
    try:
        from src.geo_targeting import IPLookup, CurrencyConverter
        geo = IPLookup.lookup("北京")
        base = 99.0
        converted = CurrencyConverter.convert(base, "USD", geo.country_code)

        success(f"IP地理位置: {geo.city}, {geo.country_name}")
        success(f"基础价格: ${base}")
        success(f"本地价格: {CurrencyConverter.format(converted, geo.country_code)} ({geo.country_code})")

        regions = {"CN": 0.85, "US": 1.0, "EU": 1.1, "APAC": 0.95}
        for code, mult in regions.items():
            info(f"  {code}: ${base * mult:.2f} ({mult}x)")
    except Exception as e:
        error(f"GEO定向失败: {e}")

    # ========== 12. Smart Landing Page ==========
    section(12, "智能落地页")
    try:
        from src.landing_page import SmartLandingPage
        page = SmartLandingPage(site_url=SITE)
        variant = page.create_variant("Social Proof Heavy")
        variant.hero_headline = "AI驱动团队协作，让效率提升10倍"
        variant.cta_text = "免费试用14天"
        variant.review_count = 3

        # Add reviews
        for rating, title, body in [
            (5, "绝对值得！", "This product is amazing."),
            (4, "很好用", "Great tool, saved us hours."),
            (5, "物超所值", "Outstanding value for money."),
        ]:
            page.add_review(rating, title, body)

        summary = page.review_summary
        success(f"落地页变体: {variant.name}")
        success(f"评价分数: {summary.average_rating:.1f}/5 ({summary.total_reviews}条)")
        success(f"好评率: {summary.positive_pct:.0f}%")
    except Exception as e:
        error(f"落地页失败: {e}")

    # ========== 13. Review Summarizer (integrated with landing_page) ==========
    section(13, "用户评价摘要")
    try:
        from src.landing_page import ReviewSummarizer, Review
        summarizer = ReviewSummarizer()

        reviews = [
            Review(review_id="1", author="Sarah", rating=5, title="Great!",
                  body="This tool is amazing and easy to use. Support team is very responsive."),
            Review(review_id="2", author="John", rating=4, title="Very good",
                  body="Solid product overall. Does what it promises. Minor issues but acceptable."),
            Review(review_id="3", author="Mike", rating=5, title="Perfect",
                  body="Outstanding value. AI features are game-changing."),
        ]

        summary = summarizer.summarize(reviews)
        success(f"评价摘要: {summary.average_rating:.1f}/5")
        success(f"好评: {summary.positive_pct:.0f}% | 中评: {summary.neutral_pct:.0f}% | 差评: {summary.negative_pct:.0f}%")
        success(f"推荐率: {summary.recommendation_rate:.0f}%")
        success(f"优点: {', '.join(summary.top_pros[:3])}")
    except Exception as e:
        error(f"评价摘要失败: {e}")

    # ========== 14. Dynamic FAQ ==========
    section(14, "动态FAQ+实时帮助")
    try:
        from src.dynamic_faq import DynamicFAQSystem
        system = DynamicFAQSystem()
        faqs = system.get_faqs_for_page(page_type="pricing")
        success(f"FAQ总数: {len(system.faqs)}")
        success(f"定价相关FAQ: {len(faqs)}")
        for faq in faqs[:2]:
            info(f"  Q: {faq.question[:50]}")

        # Help block
        tip = system.add_help_block(
            name="新手引导",
            help_type="quick_tip",
            title="快速开始",
            content="上传产品列表，AI自动分析SEO问题。",
            position="bottom_right",
            trigger_delay=15
        )
        success(f"帮助组件: {tip.name} ({tip.help_type})")
    except Exception as e:
        error(f"动态FAQ失败: {e}")

    # ========== 15. AI Content Generator ==========
    section(15, "AI内容生成")
    try:
        from src.ai_content_generator import AIContentGenerator
        gen = AIContentGenerator(web_root=WEB_ROOT)
        spec = gen.create_spec(
            content_type="blog_post",
            title="How AI is Transforming WordPress in 2026",
            keyword="AI WordPress",
            tone="professional",
            length="medium",
            cta="Get Started"
        )
        content = gen.generate_content(spec)
        success(f"内容标题: {content.title}")
        success(f"质量评分: {content.quality_score}/100")
        success(f"可读性: {content.readability_score}/100")
        success(f"字数: {len(content.body.split())}字")
        success(f"H2章节: {len(content.h2_headings)}个")
    except Exception as e:
        error(f"AI内容生成失败: {e}")

    # ========== 16. Competitor Monitor ==========
    banner("全球运营中心")
    section(16, "竞品监控响应")
    try:
        from src.competitor_monitor import CompetitorMonitor
        monitor = CompetitorMonitor(our_url=SITE, our_price="$99")
        monitor.add_competitor("竞品A", "https://example.com")

        # Simulate data
        comp = monitor.competitors["竞品A"]
        comp.price_range = "$89"
        comp.has_discount = True
        comp.discount_text = "20% OFF"
        comp.in_stock = True

        results = monitor.monitor_all()
        alerts = results["alerts"]
        success(f"监控竞品: {len(results['competitors'])}个")
        success(f"告警: {len(alerts)}个")

        for alert in alerts:
            if hasattr(alert, 'severity'):
                warn(f"  [{alert.severity}] {alert.message}")
    except Exception as e:
        error(f"竞品监控失败: {e}")

    # ========== 17. Promo Switcher ==========
    section(17, "大促页面自动切换")
    try:
        from src.promo_switcher import PromoSwitcher
        switcher = PromoSwitcher(site_url=SITE)
        report = switcher.generate_report()
        success(f"全年大促: {report['total_events_this_year']}个")
        success(f"已结束: {report['past_events']}个")
        success(f"未来30天: {report['upcoming_30_days']}个")

        for ev in report["all_events"][:5]:
            info(f"  {ev['name']}: {ev['start'][:10]}")
    except Exception as e:
        error(f"大促切换失败: {e}")

    # ========== 18. WordPress CRUD ==========
    banner("核心架构")
    section(18, "WordPress CRUD+GATE")
    try:
        from src.wordpress import WordPressClient
        wp = WordPressClient(ssh_host="", ssh_user="", ssh_key="", web_root=WEB_ROOT)
        info(f"WordPress版本: {wp.get_core_info().get('version', 'N/A')}")
        info(f"文章数: {len(wp.get_posts(limit=10))}")
        info(f"插件数: {len(wp.get_plugins())}")
        success("WordPress CRUD 已就绪")
    except Exception as e:
        error(f"WordPress CRUD失败: {e}")

    # ========== 19. Vault + Gate + Audit ==========
    section(19, "Vault+Gate+Audit框架")
    try:
        from src.vault import VaultManager
        from src.pipeline import GatePipeline, RiskLevel
        from src.audit import AuditLogger
        audit = AuditLogger()
        from src.audit import AuditLogger

        vault = VaultManager()
        pipeline = GatePipeline(audit=audit)
        audit = AuditLogger()

        info(f"Vault模式: {vault.mode}")
        info(f"Gate风险级别: LOW/MEDIUM/HIGH")
        info(f"Audit日志: JSONL格式")

        # Test gate
        level = pipeline.assess_risk("create_post")
        info(f"Gate评估: {level.name}")

        success("安全框架已就绪")
    except Exception as e:
        error(f"安全框架失败: {e}")

    # ========== Summary ==========
    banner("演示完成")

    print(f"""
{GREEN}{BOLD}📊 Auto-Claw 19个能力演示完成！{RESET}

{BOLD}能力分类:{RESET}
  AI原生独立站 (5): SEO扫描/修复/Schema/内容审计/性能诊断
  转化率飞轮 (5): A/B测试/退出意图/用户旅程/GEO/落地页+评价
  全球运营中心 (3): 竞品监控/大促切换/缓存优化+图片+FAQ+AI内容
  核心架构 (3): WordPress CRUD / Vault / Gate / Audit

{BOLD}下一步:{RESET}
  1. ClawhHub发布 (需token)
  2. SSH远程WordPress
  3. Vault生产配置

{BOLD}命令:{RESET}
  cd /root/.openclaw/workspace/auto-company/projects/auto-claw
  python3 cli.py full-audit --url {SITE}
""")

if __name__ == "__main__":
    main()
