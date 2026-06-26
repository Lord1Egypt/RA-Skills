---
name: build-smart-lists
description: "Create foundational segmented lists for marketing and sales operations. Includes a master sendable list, ICP-based lists, persona lists, engagement lists, and behavioral lists. All active (dynamic) lists."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: segmentation-scoring
---

# Build Smart Lists for Segmentation

Create 10 core active (dynamic) lists that serve as the foundation for all marketing campaigns, sales prioritization, and database health monitoring. These lists update automatically as contact properties change.

## Why This Matters

Without predefined lists, every email campaign requires building filters from scratch, there is no standardized definition of "who can we actually email", and there is no persona-based segmentation. The marketing team cannot quickly answer basic questions like "How many senior decision-makers can we email right now?" or "How many engaged contacts do we have?"

## Prerequisites

- Super Admin or Marketing Hub Admin permissions
- ICP Tier property created and workflows processed (create-icp-tiers skill)
- Lead scoring model created (build-lead-scoring skill) is recommended but not required
- Lifecycle Stage property populated for customers and partners (fix-lifecycle-stages skill)

## Interview: Gather Requirements

Before executing, collect the following information from the user:

**Q1: What defines "engaged" for your business? (e.g., activity in last 60-120 days)**
- Examples: Email open or click in last 90 days, website visit in last 60 days, form submission in last 30 days
- Default: Any email open, email click, or website session in the last 60-120 days (90 days is a common starting point; shorter cycles suit high-velocity sales, longer cycles suit enterprise)

**Q2: What job titles represent your target personas?**
- Examples: CEO, COO, CFO, CTO, CRO, VP of Operations, VP of Marketing, Director of Operations, Director of Marketing, Head of Procurement, Engineering Manager
- Default: C-suite and VP/Director-level leaders across business functions

## Plan

1. Define the 10 core lists and their filter logic
2. Create each list as an active (dynamic) list
3. Verify list sizes make sense relative to the database
4. Optionally create a dashboard to monitor list sizes

## The 10 Core Lists

| # | List Name | Purpose | Key Filters |
|---|-----------|---------|-------------|
| 1 | Marketable - Active | Master sendable list (who CAN receive email) | Marketing contact + not unsubscribed + not bounced + has email |
| 2 | ICP Tier 1 Contacts | Highest priority prospects | Associated company ICP Tier = Tier 1 + is Marketable |
| 3 | ICP Tier 2 Contacts | Secondary priority prospects | Associated company ICP Tier = Tier 2 + is Marketable |
| 4 | Engaged (Active Window) | Warm contacts showing signs of life | Email open/click in 60-120 days (default: 90) OR website sessions > 0 |
| 5 | Customers | Customer marketing and exclusion | Lifecycle stage = Customer |
| 6 | Partners | Partner communications and exclusion | Lifecycle stage = Partner |
| 7 | Re-engagement Needed | Sunset candidates | 5+ emails delivered + no open in 120-270 days (default: 180) + is Marketable |
| 8 | Senior Decision Makers | Top persona list | Job title contains target titles |
| 9 | Industry Leaders | Contacts at companies in target verticals | Associated company industry is any of target industries |
| 10 | Content Engaged | Form submissions and content downloads | Form submissions > 0 OR conversion contains content keywords |

## Execute

### List 1: Marketable - Active (Master Sendable List)

**This is the most important list.** It defines the single source of truth for "who can receive marketing email." All campaign sends should reference this list.

1. Go to **Contacts > Lists > Create list**
2. Select **Contact-based > Active list**
3. Name: `Marketable - Active`
4. Add filters (all AND logic):
   - Marketing contact status > is any of > Marketing contact
   - AND Unsubscribed from all email > is not equal to > True
   - AND Hard bounce reason > is unknown
   - AND Email > is known
   - AND Email quarantined > is not equal to > True
5. Save the list

### List 2: ICP Tier 1 Contacts

1. Create active list: `ICP Tier 1 Contacts`
2. Filters:
   - Associated company property > ICP Tier > is any of > Tier 1 - Primary ICP
   - AND List membership > is member of > Marketable - Active
3. Save

**Using List membership as a filter** is a powerful pattern. It means this list automatically inherits all deliverability and consent logic from List 1. If you add a new disqualification condition to List 1 in the future, it propagates here automatically.

### List 3: ICP Tier 2 Contacts

1. Create active list: `ICP Tier 2 Contacts`
2. Filters:
   - Associated company property > ICP Tier > is any of > Tier 2 - Secondary ICP
   - AND List membership > is member of > Marketable - Active
3. Save

### List 4: Engaged (Active Window)

Configure the engagement window based on your sales cycle: 60-120 days is typical (use 60-90 for high-velocity sales, 90-120 for enterprise). Default: 90 days.

1. Create active list: `Engaged Last [X] Days`
2. Filters (OR logic between groups):
   - Group 1: Last marketing email open date > is less than > [X] days ago
   - OR Group 2: Last marketing email click date > is less than > [X] days ago
   - OR Group 3: Number of Sessions > is greater than > 0
3. Save

### List 5: Customers

1. Create active list: `Customers`
2. Filters:
   - Lifecycle stage > is any of > Customer
3. Save

**Purpose:** Use for customer marketing (upsell, cross-sell, retention) and to EXCLUDE customers from acquisition campaigns.

### List 6: Partners

1. Create active list: `Partners`
2. Filters:
   - Lifecycle stage > is any of > Partner
3. Save

**Purpose:** Partner communications and co-marketing. Always exclude from prospect campaigns.

### List 7: Re-engagement Needed

Configure the re-engagement window based on your sales cycle: 120-270 days is typical (use shorter windows for high-velocity sales, longer for enterprise). Default: 180 days.

1. Create active list: `Re-engagement Needed`
2. Filters (all AND logic):
   - Marketing emails delivered > is greater than > 5
   - AND Last marketing email open date > is more than > [Y] days ago (default: 180)
   - AND List membership > is member of > Marketable - Active
3. Save

**Purpose:** Ongoing identification of contacts who should receive a re-engagement campaign before being suppressed or downgraded to non-marketing contacts. Feeds the engagement-based suppression workflow.

### List 8: Senior Decision Makers

1. Create active list: `Senior Decision Makers`
2. Filters:
   - Job title > contains any of > [your target titles]
   - Example titles: CEO, COO, CFO, CTO, CRO, VP of Operations, VP of Marketing, VP of Sales, Director of Operations, Director of Marketing, Head of Procurement

Customize the title keywords based on your buyer personas.

3. Save

### List 9: Industry Leaders

1. Create active list: `Industry Leaders`
2. Filters:
   - Associated company property > Industry > is any of > [your target industries]
   - Example: Manufacturing, Professional Services, Logistics, Retail, Education, Media & Entertainment
3. Save

### List 10: Content Engaged

1. Create active list: `Content Engaged`
2. Filters (OR logic between groups):
   - Group 1: Number of Form Submissions > is greater than > 0
   - OR Group 2: First conversion > contains any of > [content keywords like "Download", "Guide", "Checklist", "E-Book", "Whitepaper"]
   - OR Group 3: Recent conversion > contains any of > [same content keywords]
3. Save

**Note:** The conversion-based filters depend on your form naming conventions. Review your actual form names (Marketing > Forms) and adjust the keywords to match.

## After State

### Verify List Sizes

After all lists are created and processed:

| List | Expected Range | Red Flag If... |
|------|---------------|----------------|
| Marketable - Active | 30-80% of total contacts | Below 10% (too many excluded) or above 90% (filters too loose) |
| ICP Tier 1 Contacts | 2-10% of marketable | 0 (ICP Tier not populated) |
| ICP Tier 2 Contacts | 2-10% of marketable | 0 (ICP Tier not populated) |
| Engaged (Active Window) | 5-30% of total contacts | Below 2% (possible engagement tracking issue) |
| Customers | Known customer count | Off by more than 20% from expected |
| Partners | Known partner count | Off by more than 20% from expected |
| Re-engagement Needed | 10-40% of marketable | Above 60% (possible date threshold issue) |
| Senior Decision Makers | 5-25% of total contacts | 0 (job title data missing) |
| Industry Leaders | 10-50% of total contacts | 0 (industry data missing) |
| Content Engaged | 1-10% of total contacts | 0 (no form submissions or wrong keywords) |

### Verification Checklist

1. **All lists show as Active** (not Static) in the list view
2. **All lists have completed processing** (no "Processing" status)
3. **Marketable - Active sanity check:** Open the list, click 5 random contacts. Each should have a valid email, not be unsubscribed, not be bounced.
4. **ICP list check:** Open ICP Tier 1 list, click 5 contacts. Each should have an associated company with ICP Tier = Tier 1.
5. **Persona list check:** Open Senior Decision Makers, verify job titles match expected patterns. Watch for false positives (e.g., "Marketing Intern" matching on "Marketing").
6. **Re-engagement check:** Open Re-engagement Needed, verify contacts have 5+ emails delivered and no open beyond your configured re-engagement window.

## Key Technical Learnings

- **List 1 (Marketable - Active) is the foundation.** Every email campaign should either send directly to this list (with additional filters) or use it as an inclusion filter. Never send to a list that does not incorporate deliverability and consent checks.
- **List membership as a filter is a powerful pattern.** Lists 2, 3, and 7 use "is member of Marketable - Active" as a filter. Changes to List 1's criteria automatically propagate to all dependent lists.
- **"Contains any of" for job titles is broad by design.** It matches the keyword anywhere in the title string, so "CTO" matches "CTO", "Former CTO", "Assistant to the CTO". Review lists periodically and add exclusion terms (e.g., AND Job title does not contain "Former", "Assistant", "Intern") if false positives become a problem.
- **Content and event lists depend on form naming conventions.** The keyword-based filters only work if forms follow a naming convention that includes the keywords. After creating the lists, check if counts seem too low and adjust keywords to match actual form names.
- **Active lists have a processing delay.** HubSpot processes active lists periodically (every few minutes for small lists, potentially longer for complex ones). Wait for processing to complete before judging counts.
- **Each list should be active (dynamic), not static.** Static lists are snapshots that never update. Active lists update automatically as contact properties change, which is essential for ongoing segmentation.
- **Plan for growth.** These 10 lists cover core use cases. As marketing operations mature, add more targeted lists: "MQL Ready" (score threshold), "Competitor Employees" (for exclusion), "Recent Form Submitters (Last 30 Days)" (for fast follow-up), or service/product-specific interest lists.
- **Build a dashboard.** Create a dashboard with one KPI tile per list showing the current count. This gives at-a-glance visibility into segment health and makes it easy to spot sudden changes (e.g., Marketable list drops 50% = something broke).
