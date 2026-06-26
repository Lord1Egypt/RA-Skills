# Tech Brand Full Example — ByteNest

## Input
```json
{
  "brand_name": "ByteNest",
  "brand_positioning": "AI workflow tooling for small teams",
  "brand_tone": "direct technical practical",
  "target_audience": ["operators", "founders", "PMs"],
  "use_cases": ["task automation", "team coordination", "decision support"],
  "channels": ["wechat", "x", "linkedin"],
  "content_goals": ["thought leadership", "product awareness", "inbound leads"],
  "brand_dos": ["technical clarity", "use cases with data", "honest limitations"],
  "brand_donts": ["hype language", "vague AI claims"],
  "competitor_scope": ["Notion public signals", "Linear public signals"],
  "kpis": ["impressions", "click_through", "signups", "retention"],
  "constraints": {"budget": "low", "region": "global", "compliance": "public+authorized-only"},
  "execution_action": "content_generate",
  "browser_action": "read_public_content",
  "data_access": "public",
  "need_login": false
}
```

## Expected Output

### brand_brief
- positioning: AI workflow tooling for small teams
- tone: direct technical practical
- audience: operators, founders, PMs
- goals: thought leadership, product awareness, inbound leads

### content_strategy
- content_pillars: product walkthrough / team case study / workflow comparison / integration guide
- style_rules: tone=direct technical practical, use cases with data, no hype
- channel_rules: x → thread format; linkedin → article/post; wechat → long-form

### content_assets
- topics: "ByteNest vs spreadsheets: a real comparison", "How one PM saved 3hrs/week"
- titles: "ByteNest: AI coordination without the buzzwords"

### competitor_report
- competitors: Notion, Linear (public signals only)
- themes: productivity, collaboration, developer-friendly
- gaps: ByteNest differentiator = AI-native task reasoning vs static lists

### authorization
- execution_action: content_generate → decision: allow
- No publish/payment triggered

### browser
- action: read_public_content (Notion/Linear public pages)
- compliant: true
- capability_plan: navigate → state → get_text/get_html
