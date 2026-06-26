# Skill #63: Agency Client Reporting & Retention Kit Generator

## Overview
Generates professional client-facing reports, QBR narratives, health scorecards, and renewal/upsell proposals. Designed for digital agencies, consultants, and managed service providers who need to prove ROI, retain clients, and grow accounts.

## Use Cases
- Monthly performance reports for retainer clients
- Quarterly business reviews (QBR) for high-value accounts
- Client health scoring and churn risk identification
- Renewal conversations and upsell proposals

## Prompts

### Prompt 1: Monthly Performance Report
**Input:** Client name, services provided, KPIs this month vs last month, wins/highlights, challenges/misses, next month priorities, budget spent

**Output:**
- Executive summary (3-4 sentences, results-first)
- KPI dashboard table (metric, target, actual, MoM change, status ✅/⚠️/❌)
- Wins section (3-5 bullet points with specific numbers)
- Challenges & learnings (honest, action-oriented — no excuses)
- Recommendations (2-3 specific action items with rationale)
- Next month priorities (numbered list with owner and due date)
- Footer: hours used, hours remaining, next check-in date

**Format:** ~600-800 words, table + narrative hybrid. Suitable for email attachment or Google Doc.

---

### Prompt 2: Quarterly Business Review (QBR) Narrative
**Input:** Client name, Q goals, Q results, revenue/leads/traffic summary, key campaigns/projects, competitive context, Q+1 strategy

**Output:**
- QBR agenda (5 sections with time allocations)
- Quarter in review: narrative summary (2 paragraphs)
- Results vs goals: scorecard table (goal, result, delta, grade A-F)
- What drove performance: 3 key drivers explained
- What we'd do differently: honest retrospective (builds trust)
- Q+1 strategy brief: 3 strategic priorities with expected outcomes
- Success metrics for next quarter
- Talking points for the agency to present verbally (bulleted, not scripted)

**Format:** ~800-1,000 words, structured for a 45-60 min meeting.

---

### Prompt 3: Client Health Scorecard
**Input:** Client name, months retained, NPS score (if known), product/service usage indicators, communication responsiveness, budget trend (growing/flat/shrinking), referrals given, escalations/complaints, strategic alignment

**Output:**
- Health score: 0-100 with grade (Green 80-100, Yellow 50-79, Red 0-49)
- Scoring breakdown: 8 dimensions, each 0-10 with rationale
  - Payment reliability (10)
  - Usage/engagement depth (10)
  - Communication responsiveness (10)
  - Budget trajectory (10)
  - Strategic alignment (10)
  - Relationship depth (10)
  - Referral behavior (10)
  - Escalation history (10) [inverted — 0 escalations = 10 pts]
- Risk flags: specific churn signals with urgency level
- Recommended action: immediate steps based on score
- Internal note (not client-facing): retention play recommendation

**Format:** ~400-500 words + scorecard table. For internal agency use.

---

### Prompt 4: Renewal & Upsell Proposal
**Input:** Client name, current contract (scope, term, price), performance summary, proposed renewal terms, upsell service(s), client goals for next year

**Output:**
- Renewal cover letter (1 page, warm and results-focused)
- ROI summary: what they got vs what they paid (value delivered section)
- Proposed renewal: 3 options (maintain current / expand tier / premium tier) with pricing
- Upsell rationale: why adding [service] now makes sense with evidence
- Testimonial placeholder: prompt to request a quote from their team
- Next steps section: 3 clear actions with owner and deadline
- Urgency element: why renewing 30 days early benefits the client

**Format:** ~700-900 words, letter format. Suitable for PDF or email.

---

## Example Output
See `examples/` directory for a complete worked example: CloudPath Digital Agency × ReportLab (month 8, $4,500/month retainer, 67% MoM lead increase, QBR + renewal to $6,500/month + SEO add-on).

## Pricing Strategy
- **Free tier:** Prompt 1 (monthly report only)
- **Paid tier:** $29 one-time for all 4 prompts
- **DFY tier:** $79/month — Max runs all 4 prompts for your client roster

## Target Users
- Digital marketing agencies (50K+ in US)
- SEO/PPC/social media consultants
- Fractional CMOs and marketing advisors
- Managed IT service providers (MSPs)
- Web design agencies with ongoing retainers

## Competitive Edge
- **vs. Agency Analytics ($399/month):** No live data pull, but full narrative output — complementary, not competing
- **vs. Google Data Studio:** No data connection needed — works from numbers the user provides
- **vs. human copywriters:** $29 vs $150-300/hr for a 4-page report
- **vs. ChatGPT raw:** Enforces specific formats (QBR agenda, health scorecard rubric, 3-option renewal pricing)

## Revenue Projection
- Month 3: ~$1,156/month (40 free downloads, 10 paid × $29, 4 DFY × $79)
- Month 6: ~$2,312/month (80 paid, 8 DFY)
- DFY retainer potential: 10 agencies × $79 = $790/month recurring
