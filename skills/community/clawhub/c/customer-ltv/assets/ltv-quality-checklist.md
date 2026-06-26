# LTV Quality Assurance Checklist

Use this comprehensive 40+ item checklist before launching any LTV-based segmentation campaigns. Organized by category (REQUIRED and RECOMMENDED), each checkpoint ensures calculation accuracy, segment validity, strategy differentiation, and delivery compliance.

---

## REQUIRED: Data Quality & LTV Calculation (10 items)

**These must pass before proceeding to segmentation or campaign launch.**

- [ ] **LTV Calculation Method Documented** — Define whether using historical AOV × frequency × lifespan, cohort-based predictive, or hybrid approach. Document assumptions (discount handling, refund treatment, lookback period). Version your methodology.

- [ ] **Minimum 12 Months of Data** — All customers in LTV base have at least 12 months of post-purchase history OR are explicitly excluded as "New" segment. Do not segment customers <6 months post-acquisition.

- [ ] **Cohort Normalization Applied** — If using historical LTV, confirm cohort-based analysis separates acquisition seasons. Q4 cohorts should not inflate LTV baseline; normalize or segment seasonally.

- [ ] **Refunds & Returns Handled Consistently** — All refunds subtracted from order value (not excluded entirely). Partial refunds calculated as net revenue. Documented and auditable in calculation sheet.

- [ ] **AOV Calculation Verified** — AOV = total revenue ÷ total orders (not average order count). Confirm no duplicate counting or excluded transactions that skew upward.

- [ ] **Discount Handling Standardized** — Discounts applied to orders are included in net revenue (not excluded). Promotional orders treated same as full-price. No bias toward higher LTV from selective exclusion.

- [ ] **No Extreme Outliers Without Review** — Customers with >100 orders/year or LTV >10x median flagged and reviewed for fraud, bulk purchases, or B2B transactions. Document inclusion/exclusion decision.

- [ ] **Percentile Thresholds Validated** — Top 20% of customers drive 60%+ of revenue. If not, recalibrate thresholds or investigate data quality. Document final breakpoints (% LTV = $[amount]).

- [ ] **Churn Rate Documented** — Calculate annual churn by cohort. Use this to validate lifespan assumptions (lifespan = 1 ÷ annual churn rate). If churn is 25%/year, lifespan = 4 years.

- [ ] **Data Recalculation Schedule Set** — LTV segments refreshed monthly. Calendar reminders scheduled for [DATE each month]. Recalculation SOP documented and assigned to [Owner].

---

## REQUIRED: Segment Definition (8 items)

**Segment definitions must be crystal-clear and reproducible.**

- [ ] **All 5–6 Segments Defined with Clear Thresholds** — Champions: LTV $[X]+, VIP: $[Y]–$[X], High-Value: $[Z]–$[Y], Mid-Tier: $[A]–$[Z], Low-Value: <$[A]. Percentile equivalents documented (top 1%, top 10%, top 20%, mid 60%, bottom 20%).

- [ ] **Segment Size Verified** — Count of customers per segment documented. Total = 100% of active base. No customers assigned to multiple segments.

- [ ] **Recency Overlay Defined** — RFM scoring methodology documented. Churn risk scores calculated for all customers. Action triggers defined per segment + RFM combination.

- [ ] **Lapsed Cohorts Isolated** — "Lapsed High-Value" (180+ days inactive, was top 20%) and "Lapsed Low-Value" (180+ days inactive, was bottom 20%) defined separately with distinct playbooks.

- [ ] **New Customer Segment Handled** — Customers <6 months post-acquisition either excluded from segmentation or placed in separate "New" segment. Do not mix with mature segments.

- [ ] **Segment Definitions Reproducible** — Anyone with access to source data can reproduce segments using SQL/spreadsheet methodology documented. No manual overrides or exceptions.

- [ ] **Segment Logic Documented in Writing** — 1-page summary per segment: definition, size, avg LTV, repeat rate, characteristics. Shared with all stakeholders.

- [ ] **Segment Assignment Audit Completed** — Spot-check 20+ random customers per segment. Verify LTV calculation, segment assignment logic, and recency status match expectations.

---

## REQUIRED: Platform Setup & Data Mapping (7 items)

**Segments must exist in your marketing platform and be correctly configured.**

- [ ] **Segments Created in ESP** — All segments (Champions, VIP, High-Value, Mid-Tier, Low-Value, Lapsed High-Value, Lapsed Low-Value) created in Klaviyo/Iterable/other ESP. Segment size matches calculation file.

- [ ] **Shopify Tags Applied** — If using Shopify, customer tags applied ("champion", "vip", "high_value", "mid_tier", "low_value") and verified in Shopify admin. CSV upload or app automation confirmed working.

- [ ] **RFM Scores Added to Platform** — RFM/churn risk scores imported as custom attributes into ESP. Scores refresh daily or weekly depending on transaction volume.

- [ ] **Suppression Lists Configured** — "Suppressed—Low-Value" list created and actively excluded from all broadcasts, SMS, push. Updated weekly with new low-value customers hitting 90+ day inactivity.

- [ ] **Automation Workflows Mapped** — For each segment, document which Klaviyo/Iterable flows run and when. Example: "High-Value—Reactivation Flow triggers when customer hits 90 days inactive."

- [ ] **Ad Platform Audiences Synced** — Facebook Custom Audiences created for Champions, VIP, High-Value from email list export. Test synchronization: audience size matches ESP segment within ±5%.

- [ ] **Segment Refresh Schedule Automated** — Monthly LTV recalculation triggers automatic segment update in ESP. Manual cleanup schedule set if automation unavailable. [Owner] assigned.

---

## REQUIRED: Strategy Differentiation (6 items)

**Each segment must have distinctly different tactics and offers.**

- [ ] **Email Copy Differentiated by Segment** — Champions receive "exclusive," "insider" messaging; Mid-Tier receives promotional/value messaging. Tone, subject line, CTA differ meaningfully. Audit 3 emails per segment for differentiation.

- [ ] **Offer Depth Differentiated** — Champions: 0% off (exclusive access instead); VIP: 15–20% off; High-Value: 20–25% off; Mid-Tier: 30–40% off; Low-Value: suppressed. Documented and enforced in offer planning.

- [ ] **Email Cadence Differentiated** — Champions: 2–3x/week + SMS; VIP: 2–3x/week + SMS 2x/week; High-Value: 2x/week; Mid-Tier: 1–2x/week; Low-Value: suppressed. No segment receives identical frequency.

- [ ] **Upsell Sequences Built for Each Segment** — Champions: VIP experiences + co-creation; VIP: subscription conversion + exclusive access; High-Value: frequency acceleration + bundles; Mid-Tier: second-purchase + cross-sell; Low-Value: none.

- [ ] **Reactivation Rules Segment-Specific** — Champions: 45-day trigger, high-touch; VIP: 60-day, email + SMS; High-Value: 90-day, email; Mid-Tier: 120-day, email; Low-Value: suppressed or 180-day single email only.

- [ ] **Product/Category Recommendations Personalized** — Not "recommend bestsellers to all." Instead: Champions see premium tier + limited editions; VIP see exclusive collections; High-Value see category expansion; Mid-Tier see bundles + bestsellers; Low-Value: none.

---

## REQUIRED: Suppression & Compliance (5 items)

**Suppression logic and compliance must be airtight to protect sender reputation and legal standing.**

- [ ] **Hard Bounce Protocol Enforced** — All hard bounces (invalid email, domain does not exist) removed within 24 hours. Soft bounces monitored; removed after 2 soft bounces or 30 days of continued soft bouncing.

- [ ] **Spam Complaint Suppression Automatic** — Any customer marking email as spam/abuse immediately moved to global suppression list. Escalation to compliance team if complaint rate >0.3% from single campaign.

- [ ] **Unsubscribe Honor Documented** — All unsubscribes honored within 24 hours. Preference center allows segment-specific unsubscribe (e.g., "unsubscribe from SMS only"). Manual audits bi-weekly to confirm compliance.

- [ ] **Low-Value Suppression Rules Live** — Low-Value customers automatically suppressed from SMS, push, and paid social after 90+ days inactivity. Suppression list updated weekly. Audit confirms <5% of email volume to Low-Value segment.

- [ ] **Do-Not-Mail & DNC Compliance** — Global Do-Not-Mail list, CAN-SPAM registry, and GDPR/CCPA suppression lists checked and excluded before every send. Quarterly audit of compliance status.

---

## REQUIRED: Campaign Launch Readiness (4 items)

**Before sending first campaign, confirm all systems are go.**

- [ ] **Test Send Complete** — Send test emails to internal team (5+ people) across devices (desktop, mobile, webmail). Verify: open tracking fires, click tracking fires, unsubscribe link works, preference center loads, reply-to works.

- [ ] **Control Group Defined & Isolated** — Hold 20% of each segment as control (do not send any marketing). Isolate in ESP so accidental sends do not occur. Document control group IDs.

- [ ] **Success Metrics Dashboard Live** — Dashboard created measuring: RPE per segment, open rate, click rate, unsubscribe rate, conversion rate, segment migration. Refresh daily during campaign.

- [ ] **Stakeholder Sign-Off Recorded** — Email approval from [CMO/VP Marketing], [Compliance], [Finance], [Analytics]. Forwarded to Slack #campaign-approvals or recorded in project tracker. Launch not approved without all sign-offs.

---

## RECOMMENDED: Advanced Validation (6 items)

**These strengthen your approach; not strictly required but highly recommended.**

- [ ] **Cohort Retention Curve Analyzed** — Plot retention % by cohort month for 12+ months. Confirm each cohort shows expected decay curve (not erratic). Flag any cohort with anomalous retention (may indicate data issue or external factor).

- [ ] **Seasonality Impact Documented** — Q4 cohort LTV vs. Q1 cohort LTV calculated; seasonal multiplier documented. Note: Q4 typically 1.5–2x higher; Q1 typically lowest. Adjusted strategy if needed.

- [ ] **Product Category Mix Analyzed by Segment** — High-Value customers weighted toward [CATEGORY], Low-Value toward [CATEGORY]. Document top 3 product categories per segment; use in personalization strategy.

- [ ] **Purchase Frequency Distribution Reviewed** — Not just average frequency; understand distribution. % of segment making 1 purchase, 2 purchases, 3+. Champions should have tight distribution (>50% with 3+ purchases); Low-Value should be >60% with 1 purchase.

- [ ] **Repeat Rate Trending Over Time** — For each cohort, is repeat rate accelerating (healthy) or decelerating (concerning)? Track: Jan 2024 cohort at 30d: 5%, 60d: 12%, 90d: 18% (accelerating = good). If stuck at 10% and stalling = churn risk.

- [ ] **LTV Accuracy Benchmarked Against Industry** — Your LTV compared to category benchmarks (luxury fashion avg $700–900; vitamins $500–900, etc.). Within 20% of benchmark = validated. >30% above or below = investigate.

---

## RECOMMENDED: Email Content Quality (5 items)

**Strong email execution multiplies LTV campaign effectiveness.**

- [ ] **Subject Lines A/B Tested** — For each major send, test 2 subject line variants. Document winners. Champions should have high personalization (name, past purchase reference); Low-Value should focus on offer/urgency.

- [ ] **Preview Text Optimized** — Preview (snippet visible in inbox) called out for first 40 characters. "We miss you—20% off inside" beats "This email has the following…"

- [ ] **CTA Button Consistency** — Primary CTA appears above fold and as button (not just link). Color consistent across all segment emails. Mobile CTA >44px height for easy tap.

- [ ] **Mobile Rendering Tested** — All emails tested on iOS (iPhone 12), Android, Gmail web, Outlook. No broken layouts, cutoff text, or misaligned images. Rendering test tool used (Litmus, Email on Acid, or similar).

- [ ] **Personalization Tokens Verified** — [FIRST_NAME], [LAST_NAME], [LTV_SEGMENT], [LAST_PRODUCT_PURCHASED], etc. tested with sample data. Fallback text provided if tokens undefined (never send "[FIRST_NAME]" blank).

---

## RECOMMENDED: Offer & Incentive Validation (5 items)

**Confirm offers are profitable and well-targeted.**

- [ ] **Offer Economics Validated** — For each segment's standard offer (e.g., VIP 15% off), confirm margin preservation. Example: VIP avg AOV $250, margin 45%, 15% off = cost of $37.50. Post-discount margin = 33%. Acceptable if expect 20%+ lift in conversion.

- [ ] **Offer Sequence Built (Not Ad-Hoc Discounts)** — Reactivation offers escalate: 1st email 25% off, 2nd email 30% off, 3rd email 35% off (or premium benefit swap). No random "40% off surprise" mid-sequence.

- [ ] **Promo Codes Segment-Specific** — Each segment uses unique code (CHAMP_25, VIP_20, HV_25, etc.). Enables tracking of code redemption rate per segment.

- [ ] **Offer Expiration Clear** — Every promotional email specifies "Offer expires [DATE] at 11:59pm [TZ]." No ambiguity. Countdown timers tested to ensure accuracy.

- [ ] **Fulfillment Capability Confirmed** — Offer inventory checked before send. No over-promising (e.g., "limited to 50 units" but only 35 in stock). Supply chain and ops team sign-off on promotional volume.

---

## RECOMMENDED: Targeting & Audience Accuracy (5 items)

**Correct audience targeting prevents wasted spend and brand damage.**

- [ ] **Segment Overlap Audit** — Confirm no customer appears in multiple segments simultaneously. Run query: `SELECT customer_id, COUNT(*) FROM segments GROUP BY customer_id HAVING COUNT(*) > 1`. Should return 0 rows.

- [ ] **Segment Population Stability** — 90-day trend of segment sizes: Champions [X] → [Y] → [Z]. Expect <5% month-to-month variance (excluding seasonal). Flag any segment shrinking >10% or growing >20%.

- [ ] **Engagement Baseline Validated** — For each segment, baseline metrics documented (current open rate, click rate, conversion rate BEFORE campaign). Enables measurement of lift post-campaign.

- [ ] **New vs. Repeat Customer Logic Clear** — If including new customers (0–6 months), separate "New Customer" segment with different playbooks. Do not confuse with Low-Value (which may be lapsed repeat customers).

- [ ] **Ad Platform Audience Sync Verified** — Facebook Custom Audience created from email segment upload. Audience size matches email segment within ±5%. Re-sync scheduled for weekly updates.

---

## RECOMMENDED: Data Governance & Audit Trail (4 items)

**Documentation and auditability protect against errors and enable post-mortems.**

- [ ] **LTV Calculation Spreadsheet/SQL Versioned** — Master LTV calculation file stored with version control. Example: "LTV_Calc_v1.1_Mar2026.xlsx" with change log in separate tab. Previous versions retained for 12 months.

- [ ] **Segment Assignment Logic Documented** — One-page reference: "Champions = top 1% LTV by percentile (>$[X]) AND acquired before [DATE] AND not new." Shared with team and updated monthly.

- [ ] **Data Lineage Tracked** — Document flow: Raw transaction data (Shopify) → Cleaned export (SQL) → LTV calc (Excel/Tableau) → Segment assignment (SQL) → ESP import (Klaviyo API). Know where data comes from and where it goes.

- [ ] **Monthly Audit Log Maintained** — Record of each month's recalculation: date run, who ran it, segment sizes, total revenue, any anomalies noted. Archive for compliance and future reference.

---

## RECOMMENDED: Performance Monitoring (5 items)

**Track campaign performance and iterate toward better results.**

- [ ] **RPE (Revenue Per Email) Tracked by Segment** — Calculate: (Email Revenue ÷ Email Volume) per segment. Champions should have 3–10x higher RPE than Low-Value. Trend month-over-month to identify improvements or issues.

- [ ] **Segment Migration Monitored** — Monthly: what % of High-Value moved to VIP? What % of VIP moved to Champions? What % of Mid-Tier moved to High-Value? Healthy business should see 2–5% upward migration per month.

- [ ] **Churn by Segment Tracked** — Annualized churn rate per segment (% not purchasing in 365 days). Champions <5%, VIP <8%, High-Value <15%, Mid-Tier <25%, Low-Value >40%. Flag if any segment churn spikes.

- [ ] **Cohort Retention Curve Monitored** — For each new monthly cohort, track retention at 30d, 60d, 90d, 180d, 365d. Compare to previous cohort; flag if below trend (may indicate product/market fit issue or acquisition quality decline).

- [ ] **Win-Back Campaign ROI Measured** — For each reactivation campaign, track: cost (emails + SMS + phone), revenue attributed, ROI. Champions win-back should break even or better; Mid-Tier may lose money (acceptable if protecting larger base).

---

## RECOMMENDED: Team & Stakeholder Alignment (3 items)

**Organizational alignment prevents strategy drift and ensures accountability.**

- [ ] **Segment Strategy Documented & Shared** — 5–10 page playbook (or PowerPoint) explaining each segment's goals, tactics, and expected outcomes. Shared with marketing, product, customer success, finance teams.

- [ ] **Cross-Functional Kickoff Meeting Held** — Marketing, product, finance, customer success leadership align on segment strategy, offer economics, and success metrics. Record decisions and action items.

- [ ] **Monthly Review Cadence Scheduled** — Calendar block: [Date] each month for 30-min segment performance review. Participants: [Marketing Manager], [Analytics], [Product], [Finance]. Review: RPE trend, segment migration, churn, flags.

---

## FINAL CHECKPOINT: Launch Readiness

Before hitting send on first campaign:

- [ ] All REQUIRED checkpoints passed (20 items)
- [ ] At least 80% of RECOMMENDED checkpoints passed (23 items)
- [ ] Leadership sign-off recorded in writing
- [ ] Control group properly isolated in ESP
- [ ] Measurement dashboard live and monitoring
- [ ] Team trained on segment strategy
- [ ] Post-campaign review meeting scheduled (30 days post-launch)

**Launch Status:** ☐ APPROVED / ☐ HOLD (note reason below)

**Approved By:** [Name, Title, Date]
**Approved By:** [Name, Title, Date]

**Notes/Blockers:**
[Add any conditions, caveats, or items requiring follow-up]

---

## Post-Launch: 30-Day Review Checklist

After campaign runs for 30 days:

- [ ] RPE per segment measured and documented
- [ ] Unsubscribe rate per segment reviewed; no segment >0.6%
- [ ] Segment migration analyzed (any downward trends? Investigate)
- [ ] Win-back conversion rate measured for lapsed cohorts
- [ ] Email deliverability reviewed (bounce rate <2%, complaint rate <0.3%)
- [ ] Mobile rendering issues (if any) documented for next iteration
- [ ] Test results documented (what worked, what didn't)
- [ ] Optimization recommendations drafted for next quarter
- [ ] Stakeholder debrief meeting scheduled
- [ ] Playbook updated with learnings

**Review Date:** [DATE]
**Reviewer:** [Name]
**Overall Assessment:** ☐ SUCCESSFUL / ☐ NEEDS IMPROVEMENT / ☐ FAILED (pivot)

**Key Learnings:**
[1–3 bullet points of biggest insights or surprises]

**Next Actions:**
[Prioritized list of improvements for next campaign or optimization]
