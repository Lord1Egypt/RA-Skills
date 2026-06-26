# Example agent interactions

These are realistic conversations between a marketer and the AI Marketing + ActiveCampaign skill, shown the way they'd appear in a Telegram chat with the OpenClaw bot.

The agent's responses use real data from the underlying scripts — open rates, list sizes, automation step counts, etc. Numbers are illustrative; actual output will reflect your account.

---

## Example 1 — Morning briefing

> **🧑 You** &nbsp; *9:02 AM*
> /briefing

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *9:02 AM*
> 📨 Pulling your morning briefing — running `find_slipping_deals`, `find_hot_leads`, `baseline_drift`, `automation_audit`. About 30 seconds…

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *9:02 AM*
> ☕ **Tuesday, April 28 — Daily Briefing**
>
> **Deals needing attention (3)**
> • **Acme Enterprise** — $50,000 · 12 days overdue · stage: Negotiation · last activity 18 days ago. Call today or escalate.
> • **Globex Pro** — $25,000 · 5 days overdue · proposal sent, no response.
> • **Initech Renewal** — $12,000 · close date today, no recent activity.
>
> **Hot leads (top 3)**
> • Jane Smith (jane@acme.com) — score 92 · opened proposal 3× yesterday
> • Bob Lee (bob@globex.com) — score 85 · new deal created, high engagement
> • Priya Singh (priya@initech.com) — score 78 · trial signup + 4 page views
>
> **Campaign performance — last 3 sends**
> • April Newsletter · 2,400 sent · 31.2% open ✅ +3.2pp vs. baseline
> • Trial Nurture #5 · 340 sent · 19.8% open ⚠️ -8.2pp vs. baseline
> • Feature Launch · 1,800 sent · 28.1% open ✅ on baseline
>
> ⚠️ *Trial Nurture #5 underperformed. Want me to run a postmortem?*
>
> **Today's actions**
> 1️⃣  Call Acme — 12 days overdue ($50k)
> 2️⃣  Follow up Globex — 5 days past close ($25k)
> 3️⃣  Investigate Trial Nurture #5 (subject + audience cut)
> 4️⃣  Reach out to Jane Smith — score 92, high intent

> **🧑 You** &nbsp; *9:04 AM*
> yes run the postmortem on the trial nurture

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *9:04 AM*
> Running `campaign_postmortem.py 247`…
>
> **Trial Nurture #5 — Postmortem**
> • Subject: "{firstName}, here's what's next" · sent Tue 8 AM UTC · 340 recipients
> • Open rate **19.8%** vs. account baseline 28.0% (-8.2pp ⚠️)
> • Click rate 1.2% vs. baseline 4.0% (-2.8pp)
> • Click-to-open ratio 6.1% (very low — content didn't compel action)
>
> **Likely cause:** Send time. Your account's best-open hour is **2 PM UTC** (3pp lift). 8 AM UTC is your worst window.
>
> **Recommendation:** Re-send to the no-opens cohort at 2 PM UTC tomorrow with a refreshed subject. Want me to draft the spec?

---

## Example 2 — List health audit

> **🧑 You** &nbsp; *2:47 PM*
> i think my list is dirty. can you audit it?

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *2:47 PM*
> 📨 On it. Running the list health workflow — `audit_list_health`, `dedupe_contacts`, `role_address_finder`, `free_vs_corporate_report`, `list_overlap`, `suppression_export`, `stale_contact_report`. About 2 minutes…

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *2:49 PM*
> 📋 **List Health Audit — Summary**
>
> **Headline metrics (vs. 90-day baseline)**
> • Active contacts: **12,438**
> • Bounce rate: 1.8% ⚠️ (+0.6pp vs. baseline 1.2%)
> • Unsub rate: 0.31% ✅ on baseline
> • Engaged-in-30-days: 38% ⚠️ (target: ≥45%)
>
> **🚩 5 things to clean up before your next send**
>
> 1. **47 role addresses** on Master Contact List
>    `info@*`, `support@*`, `sales@*` — never engage, hurt deliverability
>    Action: suppress all 47 (1-click via API)
>
> 2. **63 case-insensitive email duplicates**
>    e.g. `Alice@Acme.com` AND `alice@acme.com` — both counting as 1 contact toward your plan
>    Action: merge to lowercase canonical
>
> 3. **8 lists ≥95% subset of "Master Contact List"**
>    `Newsletter`, `Updates`, `Few Locust`, `Young Hornet`… — likely consolidation candidates
>    Action: pick 1 as canonical, archive the rest
>
> 4. **1,847 contacts with no engagement in 12+ months**
>    On 4 lists; last open was Apr 2024
>    Action: re-engagement attempt (recipe available) → sunset whoever doesn't reopen
>
> 5. **Bounce trend +0.6pp over 30 days**
>    Spike traces to import on Apr 18 (CSV: "leads_q1_2026.csv")
>    Action: re-validate that source; may need to suppress that batch
>
> **B2B vs. consumer mix**: 96.6% corporate (ActiveCampaign, Telenix, etc.) — your list is firmly B2B. Tune subject lines accordingly.

> **🧑 You** &nbsp; *2:51 PM*
> draft the suppression update for #1 and #2

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *2:51 PM*
> Will execute these writes (110 total operations). Confirm before I run any:
>
> **Plan:**
> • Set status=2 (unsubscribed) on 47 role addresses
> • Merge 63 duplicate pairs (keep lowercase canonical, suppress alternate-case)
>
> Say `yes` to execute, or `dry-run` to preview the API calls without writing.

---

## Example 3 — Subject line patterns

> **🧑 You** &nbsp; *11:32 AM*
> what subject line patterns are working for me

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *11:32 AM*
> Running `subject_line_report --days 90`…
>
> 🎯 **Subject Line Patterns — Last 90 Days**
> Analyzed 47 sends · baseline open rate **28.0%**
>
> | Pattern | n with | n w/o | Δ vs. baseline |
> |---|---|---|---|
> | Personalization (`%FIRSTNAME%`) | 12 | 35 | **+6.1pp** ✅ |
> | Question (ends in ?) | 8 | 39 | +3.4pp ✅ |
> | Emoji | 4 | 43 | +1.2pp |
> | Urgency words | 6 | 41 | -2.1pp ⚠️ |
> | All-caps | 1 | 46 | -11.0pp ❌ |
>
> **Length buckets** — sweet spot is 31-60 chars
> • ≤30 chars: 24.1% open
> • 31-60 chars: **31.4%** open ⭐
> • 60+ chars: 22.0% open
>
> **What this says about your audience**
> • Personalization tokens are your biggest free win — use on every campaign
> • Questions outperform statements (consultative tone fits B2B)
> • Don't shout (all-caps is killing your one trial send)
> • Keep subjects 31-60 chars for the sweet-spot length
>
> Want me to A/B-test a personalized variant against your next send for confirmation?

---

## Example 4 — Hot leads

> **🧑 You** &nbsp; *4:15 PM*
> who should i call today

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *4:15 PM*
> Running `find_hot_leads --top 5`…
>
> 🔥 **Hot Leads — Today**
>
> | Contact | Score | Signal | Action |
> |---|---|---|---|
> | **Jane Smith** (jane@acme.com) | **92** | Opened proposal 3× yesterday + visited pricing page | Call today — proposal is open |
> | **Bob Lee** (bob@globex.com) | 85 | New deal created Apr 27, score jumped +18 in 7 days | Confirm BANT, send proposal |
> | **Priya Singh** (priya@initech.com) | 78 | Trial signup + 4 page views, downloaded white paper | Welcome call, qualify use case |
> | **Marcus Chen** (marcus@megacorp.com) | 71 | Tagged "enterprise-target", opened 4 of 6 sends | Account executive intro |
> | **Lara Patel** (lara@umbrella.com) | 68 | Cross-sell candidate (existing customer with new role) | Renewal + expansion |
>
> 💡 *Jane Smith is the standout — proposal opens 3× in 24h is a "buying signal" pattern. Open rate among contacts with this pattern who closed in the last 90 days: 64%.*

---

## Example 5 — Tag hygiene

> **🧑 You** &nbsp; *Friday 10:18 AM*
> i feel like my tags are a mess. can you check

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *10:18 AM*
> Running `tag_audit`…
>
> 🏷️ **Tag Hygiene Report**
> 72 total tags · 187 tagged contacts
>
> **🪦 Dead tags (no automation/segment uses them) — 68**
> Top examples:
> • `Holiday 2018 Coupon Used` — 0 contacts (4 years stale)
> • `Training: Onboarding Scheduled` — 0 contacts
> • `landing-pages-integration-` — 0 contacts (literal trailing dash typo)
> • `September Promo - Engaged` — 0 contacts
> • …64 more
>
> Action: bulk delete the 68 dead tags
>
> **🤝 Consolidation candidates (95%+ co-occurrence)**
> • `Product Category Interest: Scented` + `Product Category Interest: Electric` — appear together on every contact
> • Merge into single tag `Product Category Interest`
>
> **📈 Over-applied (lost discriminating power)**
> • `shopify-customer` — applied to 99% of tagged contacts. Useless as a filter.
>
> **🚨 Likely typos (used <2 times each)**
> • `landing-pages-integration` AND `landing-pages-integration-` (with trailing dash)
> • `created-from-salesforce-lead` (used 1× — probably a one-off)
>
> Net cleanup: **72 → ~6 meaningful tags**. ~1 hour of work, much cleaner reporting.

---

## Example 6 — Quarterly review

> **🧑 You** &nbsp; *Friday 4:45 PM*
> /quarterly-review

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *4:45 PM*
> 📊 Running the full quarterly review — this will take ~5 minutes (24 scripts, ~3,500 API calls). I'll send the report when ready. ⏳

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *4:50 PM*
> 📈 **Q1 2026 Marketing Review**
>
> **Executive summary**
> • 47 campaigns sent to 312k recipient-events; open rate **26.4%** (-0.8pp vs. baseline)
> • List grew 8.4%; new-subscriber engagement is solid (62% opened ≥1 email)
> • 3 automations completed >10k contacts; 2 are orphaned
> • 14 zombie tags + 6 unused custom fields safe to delete
> • Pipeline closed **$487k won / $112k lost**; one source list has 0% win rate
>
> *Full 8-section report (~4 pages) attached.*
>
> **Top 3 actions for Q2:**
> 1. Investigate Trial Nurture stall (230 contacts stuck at Wait-7-days step)
> 2. Suppress 47 role addresses + 14 zombie tags before next campaign
> 3. A/B test personalized subject lines (data shows +6.1pp lift)

---

## Example 7 — Pre-send safety check

> **🧑 You** &nbsp; *Tuesday 1:48 PM*
> sending the launch announcement to "Active Customers" in 2 hours. anything i should know first?

> **🤖 AI Marketing + ActiveCampaign** &nbsp; *1:48 PM*
> Running pre-flight on list "Active Customers"…
>
> ✈️ **Pre-Send Check — Active Customers**
>
> **Audience**
> • 8,742 active subscribers · 0 currently in your in-flight automations (no overlap risk)
>
> **Quality flags** ⚠️
> • 23 hard-bounced contacts still on the list — should suppress before send
> • 8 role addresses (`info@*`, `support@*`)
> • 11 contacts marked as "fatigued" (received >8 sends in last 30 days)
>
> **Send timing**
> • Your account's best open window: **Tue/Wed/Thu 13:00-15:00 UTC**
> • You scheduled for: **Tue 16:00 UTC** — within +1h of optimal ✅
>
> **Forecast (vs. 90-day baseline)**
> • Estimated opens: 2,448 (28% of 8,742)
> • Estimated clicks: 350 (4%)
> • Estimated unsubs: 26 (0.3%)
> • Estimated bounces: 44 (0.5%)
>
> **🚦 Verdict: yellow — clean up the 23 bounces before sending.**
>
> Want me to suppress them now?

---

## Notes on these examples

The agent uses Telegram's standard markdown subset — bold, italics, lists, tables (as code blocks), and emoji. Long reports are sent as a single message with section headers; very long reports may be sent as a file attachment.

All agent responses are grounded in actual script output. The scripts read your real account data via the AC v3 API; the agent then summarizes and formats. No data is sent anywhere except your own AC account.
