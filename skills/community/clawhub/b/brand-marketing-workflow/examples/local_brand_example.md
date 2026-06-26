# Local Brand Full Example — River Tea

## Input
```json
{
  "brand_name": "River Tea",
  "brand_positioning": "local tea brand with modern lifestyle appeal",
  "brand_tone": "warm grounded friendly",
  "target_audience": ["nearby residents", "young shoppers 20-35"],
  "use_cases": ["gifts", "daily tea", "social sharing"],
  "channels": ["xiaohongshu", "wechat", "local_community"],
  "content_goals": ["foot traffic", "social sharing", "brand affinity"],
  "brand_dos": ["authentic local story", "seasonal content", "community tie-ins"],
  "brand_donts": ["cold corporate tone", "over-edited imagery"],
  "competitor_scope": ["local cafe public signals", "HeyTea public signals"],
  "kpis": ["store_visits", "shares", "follower_growth", "repeat_purchase"],
  "constraints": {"budget": "low", "region": "CN-local", "compliance": "public+authorized-only"},
  "execution_action": "draft_prepare",
  "browser_action": "collect_public_signals",
  "data_access": "public",
  "need_login": false
}
```

## Expected Output

### brand_brief
- positioning: local tea brand with modern lifestyle appeal
- tone: warm grounded friendly
- audience: nearby residents, young shoppers 20-35
- goals: foot traffic, social sharing, brand affinity

### content_strategy
- content_pillars: origin story / seasonal specials / community moments / gift ideas
- style_rules: tone=warm grounded friendly, authentic local story, seasonal content
- channel_rules: xiaohongshu → visual/lifestyle posts; wechat → community articles

### content_assets
- topics: "How River Tea began", "This winter's new blend", "A gift for someone you love"
- titles: "River Tea: where tea meets daily life"

### competitor_report
- competitors: local cafe, HeyTea (public signals only)
- themes: lifestyle, seasonal, visual richness
- gaps: River Tea differentiator = authentic local roots + lifestyle positioning

### authorization
- execution_action: draft_prepare → decision: allow
- Publish confirmation required before going live

### browser
- action: collect_public_signals on xiaohongshu
- compliant: true
- capability_plan: navigate → state → extract likes/comments/saves/public metadata
