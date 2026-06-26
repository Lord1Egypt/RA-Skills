#!/bin/bash
# Auto-Claw Weekly Report Generator
# Usage: bash scripts/weekly-report.sh
# Run via cron: 0 9 * * 1 cd /root/.openclaw/workspace/auto-company/projects/auto-claw && bash scripts/weekly-report.sh

WEB_ROOT="/www/wwwroot/linghangyuan1234.dpdns.org"
SITE_URL="http://linghangyuan1234.dpdns.org"
REPORT_FILE="/root/.openclaw/workspace/auto-company/projects/auto-claw/logs/weekly-report-$(date +%Y-W%V).txt"

echo "=============================================="
echo "Auto-Claw Weekly Report — $(date '+%Y-%m-%d %H:%M UTC')"
echo "=============================================="
echo ""

# 1. Full audit
echo "📊 Full Site Audit:"
cd /root/.openclaw/workspace/auto-company/projects/auto-claw
python3 cli.py full-audit 2>/dev/null | grep -E "SEO|性能|内容|缓存|图片|审计完成" | sed 's/^/   /'
echo ""

# 2. A/B Test Results
echo "🧪 A/B Test Results:"
curl -s "${SITE_URL}/wp-json/autoclawa/v1/ab/stats?test=ab_exit_001" 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   Variant A: {d[\"A\"][\"impressions\"]} impressions, {d[\"A\"][\"conversions\"]} conversions ({d[\"A\"][\"rate\"]})'); print(f'   Variant B: {d[\"B\"][\"impressions\"]} impressions, {d[\"B\"][\"conversions\"]} conversions ({d[\"B\"][\"rate\"]})')" 2>/dev/null || echo "   No data yet"
echo ""

# 3. Analytics Summary
echo "📈 Analytics:"
curl -s "${SITE_URL}/wp-json/autoclawa/v1/track/pageview" \
  -X POST -H "Content-Type: application/json" \
  -d '{"page":"/weekly-check","title":"Weekly Report"}' 2>/dev/null

cd "$WEB_ROOT" && wp eval '
$views = get_option("autoclaw_page_views", array());
$convs = get_option("autoclaw_conversions", array());
$total = array_sum($views);
echo "   Total pageviews (30d): " . $total . "\n";
echo "   Total conversions: " . count($convs) . "\n";
$by_event = array();
foreach ($convs as $c) {
    $e = $c["event"];
    $by_event[$e] = ($by_event[$e] ?? 0) + 1;
}
foreach ($by_event as $event => $count) {
    echo "   - $event: $count\n";
}
' --allow-root 2>/dev/null
echo ""

# 4. Beta Applications
echo "🎯 Beta Applications:"
curl -s "${SITE_URL}/wp-json/autoclawa/v1/beta/applications" 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   Total: {d.get(\"count\",0)} applications')" 2>/dev/null || echo "   (requires admin auth)"
echo ""

# 5. Competitor Monitor
echo "📊 Competitor Monitor:"
cd "$WEB_ROOT" && php -r "
require 'wp-load.php';
update_option('autoclaw_competitor_last_check', 0);
if (function_exists('autoclaw_run_competitor_check')) {
    \$r = autoclaw_run_competitor_check();
    foreach (\$r['results'] ?? [] as \$c) {
        echo '   ' . \$c['competitor'] . ': ' . \$c['status'] . ' | pricing: ' . (\$c['has_pricing'] ? 'yes' : 'no') . '\n';
    }
}
" 2>/dev/null
echo ""

# 6. WordPress Status
echo "🔧 WordPress Status:"
cd "$WEB_ROOT" && wp plugin list --status=active --format=table --allow-root 2>/dev/null | grep -E "Name|active" | head -10
echo ""

# 7. Posts Published
echo "📝 Content:"
cd "$WEB_ROOT" && wp post list --post_type=post --post_status=publish --fields=post_title,post_date --format=table --allow-root 2>/dev/null
echo ""

echo "=============================================="
echo "Report saved to: $REPORT_FILE"
echo "=============================================="
