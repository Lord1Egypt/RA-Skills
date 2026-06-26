#!/bin/bash
# Auto-Claw Quick Status Check
# Usage: bash status.sh

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🦶 Auto-Claw Status — $(date +%Y-%m-%d\ %H:%M\ UTC)       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

cd /root/.openclaw/workspace/auto-company/projects/auto-claw

# Check if WordPress is accessible
echo "📊 Site Health:"
if curl -s --max-time 5 http://linghangyuan1234.dpdns.org > /dev/null 2>&1; then
    echo "   ✅ Site accessible"
    python3 cli.py wp status --web-root /www/wwwroot/linghangyuan1234.dpdns.org 2>/dev/null | grep -E "版本|文章" | sed 's/^/   /'
else
    echo "   ❌ Site not accessible"
fi
echo ""

# Cron status
echo "⏰ Automation:"
crontab -l 2>/dev/null | grep "audit-daily\|full-audit" > /dev/null && echo "   ✅ Daily cron (8:00 UTC)" || echo "   ❌ Daily cron not set"
crontab -l 2>/dev/null | grep -i "week\|monday" > /dev/null && echo "   ✅ Weekly cron (Monday 9:00 UTC)" || echo "   ❌ Weekly cron not set"
echo ""

# Latest audit - run fresh if needed
echo "📋 Site Scores (live):"
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from seo import SEOAnalyzer
    from performance_diag import PerformanceDiagnostic
    from content_audit import ContentAuditor
    from cache_optimizer import CacheOptimizer
    
    url = 'http://linghangyuan1234.dpdns.org'
    web_root = '/www/wwwroot/linghangyuan1234.dpdns.org'
    
    # SEO
    analyzer = SEOAnalyzer()
    report = analyzer.scan(url)
    print(f'   SEO: {report.overall_score}/100 | {report.total_issues} issues')
    
    # Performance
    diag = PerformanceDiagnostic()
    result = diag.diagnose(url, web_root)
    print(f'   Performance: {result.score}/100')
    
    # Content
    auditor = ContentAuditor()
    result = auditor.audit(url, web_root)
    print(f'   Content: {result.quality_score}/100 | Readability: {result.readability_score}/100')
    
    # Cache
    optimizer = CacheOptimizer()
    result = optimizer.analyze(web_root)
    print(f'   Cache: {result.enabled_count}/{result.total_count} enabled')
except Exception as e:
    print(f'   ⚠️  Could not fetch live scores: {e}')
" 2>/dev/null
echo ""

# GTM Status
echo "🚀 GTM Status:"
echo "   ⏳ HN Launch post — pending your 'launch' confirmation"
echo "   ⏳ landing.html — needs public URL deployment"
echo "   ⏳ ClawhHub token — login at https://clawhub.ai"
echo ""

# What's next
echo "📁 Quick Commands:"
echo "   python3 cli.py full-audit     # Full site audit"
echo "   python3 demo_complete.py      # All 19 capabilities demo"
echo "   open dashboard.html           # Visual dashboard"
echo ""

echo "💡 GTM Next Steps:"
echo "   1. Reply 'launch' to submit HN post"
echo "   2. Deploy landing.html to get a public URL"
echo "   3. Get ClawhHub token to publish skill"
echo ""
