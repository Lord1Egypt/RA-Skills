# Campaign Structure Guide

## The Four-Campaign Architecture

Every mature ASA account should have these four campaign types running simultaneously. They serve different intents and should never be combined — mixing them makes it impossible to optimize bids and budgets per intent.

---

## Campaign 1: Brand Campaign

**Goal**: Protect your own brand searches. Users searching your app name are already aware of you — they're the highest-intent, lowest-CPA traffic available.

**Keywords**:
- Exact app name
- Common misspellings
- Brand variations and abbreviations
- Developer name if searchable

**Match type**: Exact match only. Broad match here means competitors can show for your brand.

**Bid strategy**: High bids — you should own top position for your own brand terms at all costs. CPA here is almost always your lowest.

**Budget allocation**: 10–15% of total budget

**Key insight**: If you're not running a brand campaign, competitors are bidding on your name and taking users who already want your app. This is the first campaign to set up.

---

## Campaign 2: Generic Keyword Campaign

**Goal**: Capture users searching for a solution in your category — they know what they need but haven't chosen an app yet.

**Keyword examples by category**:
- Fitness: workout planner, HIIT timer, calorie counter
- Productivity: task manager, habit tracker, note app
- Finance: budget tracker, expense tracker, savings app
- Creative: photo editor, video editor, AI art generator

**Match type**: Exact + broad phrase match. Start exact, add phrase once you have performance data.

**Bid strategy**: Moderate. These keywords have real competition — bid at suggested range initially, then adjust based on CR.

**Budget allocation**: 35–45% of total budget — this is your primary growth driver.

**Segmentation tip**: Split high-intent "solution" keywords (e.g., "budget tracker") from feature keywords (e.g., "track daily expenses"). They often have different conversion rates and warrant separate ad groups.

---

## Campaign 3: Competitor Campaign

**Goal**: Appear when users search for competing apps — they're already in buying mode, just evaluating options.

**Keyword examples**:
- Direct competitor names (e.g., "Todoist", "MyFitnessPal", "Calm")
- Competitor + category combinations (e.g., "Notion alternative")

**Match type**: Exact match. You only want to show for users specifically searching a competitor, not broad brand-adjacent terms.

**Bid strategy**: Start 20-30% below your generic campaign bids. Conversion rates are lower because users were searching for someone else — test before scaling.

**Budget allocation**: 15–25% of total budget

**Risk assessment**: Competitor campaigns are legal in ASA (Apple permits bidding on competitor brand names). However:
- Conversion rates are typically 20-40% lower than generic campaigns
- Some competitors have strong brand loyalty — test carefully before scaling
- Never run without a strong differentiating product page

**When to skip**: If you're a new app with no distinctive advantage over the competitor, competitor campaigns will drain budget without converting. Build your ASO first.

---

## Campaign 4: Discovery Campaign

**Goal**: Find keywords you don't know about yet. Your creative instincts about what users search for are often wrong — this campaign lets Apple's algorithm find the actual search terms that convert.

**Setup**:
- Use broad match keywords (your best guesses at intent)
- Enable Apple Search Match (automated keyword matching)
- Set a separate, capped daily budget

**Match type**: Broad match + Search Match enabled

**Bid strategy**: Lower bids than generic campaign — you're paying for data, not just installs. Start at 50-70% of your generic campaign CPT bid.

**Budget allocation**: 20–30% of total budget

**The discovery-to-exact pipeline** (critical workflow):
1. Run discovery for 2-4 weeks
2. Export search terms report from ASA dashboard
3. Filter for search terms with CR > 30% and ≥ 10 installs
4. Move those exact terms into your Generic campaign as exact match keywords
5. Add non-converting search terms as negatives in all campaigns
6. Repeat monthly

**What you'll find**: Users often search in ways that surprise you. "Best habit app for anxiety" might convert better than "habit tracker". You can only find this through discovery.

---

## Campaign Setup Checklist

Before launching any campaign:
- [ ] Ad group created with correct match type
- [ ] Daily budget set (not just total campaign budget)
- [ ] Negative keywords added (at minimum: free, crack, hack, cheat, wallpaper, ringtone, unrelated categories)
- [ ] Custom product pages assigned if available
- [ ] Attribution tracking confirmed (SKAdNetwork or MMP)
- [ ] CPA goal or CPT bid set (not both — pick one approach per campaign)

---

## Budget Allocation Summary

| Campaign | Allocation | Priority |
|----------|-----------|---------|
| Brand | 10-15% | Set and forget, maintain top position |
| Generic | 35-45% | Primary optimization target |
| Competitor | 15-25% | Test at low scale before expanding |
| Discovery | 20-30% | Run always, mine for new keywords |

**Rebalance rule**: If Generic CPA is hitting targets, shift budget from Discovery and Competitor into Generic. If Generic CPA rises, use Discovery to find fresher keywords.
