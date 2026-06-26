# Client Relationship Manager — Advanced Patterns

_by The Agent Ledger | theagentledger.com_

---

## 1. The Weekly CRM Ritual

A structured weekly CRM review keeps your pipeline honest and your relationships warm. Run this every Monday morning (cron or manual):

```
CRM Weekly Review Protocol:

1. FOLLOW-UPS: Read follow-ups.md. List everything overdue + due this week. Flag any item overdue by 7+ days as "stalled."

2. PIPELINE HEALTH: Read pipeline.md. For each deal in Proposal Sent or Negotiating stage:
   - How many days since last interaction?
   - Is the next action date still in the future, or has it passed?
   - Flag deals with no movement in 14+ days as "at risk."

3. RELATIONSHIP WARMTH: Scan all client files for "Active" clients. Flag any with no interaction log entry in 30+ days.

4. CLOSED-WON REVIEW: Check for any Closed-Won clients from the last 90 days. Are there upsell or case study opportunities?

5. OUTPUT: Weekly CRM summary — 10 lines or less. Overdue items, at-risk deals, relationship alerts, one recommended priority action.
```

---

## 2. Multi-Service Tracking

If you offer multiple services, track them per-client with a services section:

```markdown
## Services

| Service | Status | Rate | Started | Renewed |
|---------|--------|------|---------|---------|
| Monthly Retainer | Active | $X/mo | 2025-09-01 | 2026-01-01 |
| Project: Website Redesign | Complete | $X | 2025-07-15 | — |
| Ad-Hoc Advisory | Occasional | $X/hr | 2025-08-01 | — |

**Total LTV:** $X
**Annualized value (current):** $X/yr
```

Then your pipeline.md value column reflects total annual value, not just the current engagement.

---

## 3. Relationship Score System

Rate relationship health on a simple 1-5 scale:

```markdown
**Relationship Score:** 4/5
**Score Rationale:** Strong rapport, pays on time, refers occasionally. Would take another project. Minor tension around scope on last engagement — resolved but worth watching.
**Last Scored:** YYYY-MM-DD
```

Review and update scores quarterly. Declining scores on active clients are early churn signals.

---

## 4. The Pre-Meeting Brief Template

When you say "prep me for [client]," your agent should produce this format:

```
MEETING BRIEF: [Client Name]
Date: [Today]
Meeting type: [Call / In-person / Video]

WHO YOU'RE TALKING TO
[Contact name], [title], [company]. [1 sentence on their background].

WHERE THINGS STAND
Stage: [Current stage]
Value: [Deal value or MRR]
Last contact: [Date] via [medium]

LAST INTERACTION SUMMARY
[2-3 sentences on what was discussed, what was agreed, what's outstanding]

WHAT THEY CARE ABOUT
[From background section — their key priorities, concerns, or constraints]

YOUR NEXT ACTION
[What you said you'd do / what you're asking for in this meeting]

WATCH FOR
[Any known friction points, sensitivities, or things to handle carefully]

SUGGESTED TALKING POINTS
1. [Open with this]
2. [Address this proactively]
3. [Ask about this]
```

---

## 5. Deal Post-Mortem (Closed-Lost)

When a deal is lost, log a brief post-mortem before archiving:

```markdown
## Post-Mortem (Closed-Lost)

**Lost Date:** YYYY-MM-DD
**Loss Reason:** [Price / Timing / Competitor / Scope mismatch / No decision / Other]
**Competitor (if known):** [Name or "Unknown"]
**Decision Maker:** [Did I reach the actual decision-maker? Yes/No]
**Biggest Obstacle:** [In one sentence]
**What I'd Do Differently:** [One actionable lesson]
**Reopen Potential:** [Yes — follow up in Q3 / No / Unknown]
**Next Touch (if any):** YYYY-MM-DD — [Brief touch to keep door open]
```

Run quarterly: review all Closed-Lost post-mortems and look for patterns. If the same loss reason appears 3+ times, that's a product, pricing, or targeting problem — not a sales problem.

---

## 6. The Referral Network Map

Track who sends you business and who you send business to — it's one of the highest-ROI activities for solopreneurs.

Create `crm/referral-network.md`:

```markdown
# Referral Network

## My Top Referral Sources

| Person | Company | Referrals Sent Me | My Referrals To Them | Last Touch |
|--------|---------|-------------------|----------------------|------------|
| [Name] | [Co] | 3 ($X total) | 1 | YYYY-MM-DD |

## Referral Leaderboard (Last 12 Months)
1. [Name] — 3 referrals, $X in business
2. [Name] — 1 referral, $X in business

## Pending Reciprocation
- [ ] [Name] sent me [Client]. I haven't sent them anything yet. Look for opportunities.

## Thank You Queue
- [ ] Send [Name] a note — they sent me [Client] last month.
```

Your agent can flag referral imbalances ("You've received 3 referrals from X but sent 0 back — worth watching.").

---

## 7. Churn Prevention Monitoring

For service businesses with recurring revenue, track churn risk signals:

```markdown
## Churn Risk Signals
- No interaction in 45+ days (for monthly clients)
- Scope creep that wasn't addressed
- Payment late 2+ times
- Sponsor/champion left the company
- Engagement declining (fewer requests, shorter responses)
- They asked about contract terms or cancellation policy
```

Add this check to your weekly CRM ritual or HEARTBEAT.md:

```
Churn Risk Check:
- Read all Active client files
- Flag any with: no interaction in 45+ days, late payment notes, or any churn risk signals noted
- Report as: 🔴 High risk / 🟡 Watch / 🟢 Healthy
```

---

## 8. Client Onboarding Checklist

When a deal closes, use a standard onboarding log entry:

```markdown
### YYYY-MM-DD — Onboarding Started
- [ ] Signed agreement received
- [ ] Invoice sent (deposit)
- [ ] Kickoff call scheduled
- [ ] Access/credentials collected
- [ ] Project file created (link to crm/projects/[slug])
- [ ] Added to project-tracker dashboard
- [ ] Welcome email/message sent
- [ ] First deliverable date confirmed
```

Ask your agent to generate this checklist entry whenever you mark a deal as "Closed-Won."

---

## 9. Annual Client Review

Once a year (January or your fiscal year-end), run an annual review across all clients:

```
Annual CRM Review:

1. REVENUE: Sum all Closed-Won values from the year. Break down by client, service type, and quarter.

2. TOP CLIENTS: Who were your top 5 clients by revenue? By referrals? By ease of working with them?

3. WORST CLIENTS: Who were the most difficult, lowest-margin, or most time-consuming? What would you do differently?

4. LOSS ANALYSIS: Review all Closed-Lost records. What patterns do you see?

5. RETENTION: What % of Active clients from last year renewed?

6. PIPELINE QUALITY: Review all current Leads and Prospects. Are they realistic? Cut anything you haven't touched in 90+ days.

7. RELATIONSHIP MAINTENANCE: Who haven't you talked to in 6+ months that you should reconnect with?

8. NEXT YEAR TARGETS: Based on this data, set revenue targets by client segment.
```

---

## 10. Integration with Solopreneur Dashboard

If you use the `solopreneur-assistant` skill, add CRM metrics to your weekly dashboard section:

```
## Business Dashboard — CRM Section

**Pipeline:**
- Total value: $X across X deals
- Active clients: X generating $X/mo MRR
- Deals in negotiation: X ($X combined)

**Relationships:**
- Follow-ups overdue: X
- Clients not touched in 30+ days: X
- Referrals received (MTD): X

**Health:**
- Win rate (last 90 days): X%
- Average deal size: $X
- Average sales cycle: X days
```

---

## Notes on Data Hygiene

The biggest failure mode in text-based CRM is staleness. A few rules to keep it useful:

1. **Log within 24 hours** — Interaction context fades fast. Ask your agent to help you log immediately after calls.
2. **Always set a next action** — A client record with no "Next Action Due" date is invisible to your follow-up process.
3. **Quarterly archive** — Move Closed-Won and Closed-Lost clients older than 12 months to `crm/archive/` to keep the active directory manageable.
4. **One source of truth** — Don't maintain the same client in a CRM tool AND these files. Pick one. Text files win if you want agent access.

---

_Part of the Agent Ledger Skills Collection — free, open, and built to work together._
_→ theagentledger.com for new skills, guides, and the premium blueprint guide._

**License:** CC-BY-NC-4.0
