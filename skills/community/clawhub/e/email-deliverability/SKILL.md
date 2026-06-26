---
name: "Email Deliverability"
description: "Audit and improve email deliverability for ecommerce marketing by diagnosing spam folder issues, list hygiene problems, authentication gaps, and sending reputation issues."
version: "1.0"
category: "ecommerce-marketing"
tags: ["email", "deliverability", "spam", "authentication", "list-hygiene", "reputation"]
---

# Email Deliverability

Audit and improve email deliverability for ecommerce marketing. This skill provides a systematic framework for diagnosing why emails land in spam, identifying authentication gaps, cleaning subscriber lists, and repairing sending reputation to maximize inbox placement rates.

---

## Quick Reference

Use this table to rapidly assess the current state of any deliverability dimension.

| Decision Area | Strong | Acceptable | Weak |
|---|---|---|---|
| **Inbox Placement Rate** | >95% inbox placement across major providers | 85-95% placement with minor provider-specific issues | <85% placement or blacklisted at one or more major provider |
| **Authentication (SPF/DKIM/DMARC)** | All three configured with DMARC at p=reject and aligned | SPF + DKIM in place, DMARC at p=none or p=quarantine | Missing one or more protocol, no DMARC, or misaligned records |
| **Bounce Rate** | <1% hard bounces per campaign | 1-2% hard bounces, soft bounces under 5% | >2% hard bounces or >5% soft bounces per campaign |
| **Spam Complaint Rate** | <0.05% (below 1 per 2,000 emails) | 0.05-0.08% with downward trend | >0.08% or rising trend (Google threshold is 0.10%) |
| **List Hygiene** | Verified within 90 days, engaged segments defined, sunset policy active | Verified within 6 months, basic segmentation in place | No verification in 6+ months, no segmentation, no sunset policy |
| **Sending Infrastructure** | Dedicated IP with warm-up complete, consistent volume, subdomain isolation | Shared IP with reputable ESP, moderate volume consistency | Unknown IP reputation, erratic volume, no subdomain separation |
| **Content Quality** | Personalized, mobile-optimized, <0.1% spam trigger density, clear unsubscribe | Template-based with some personalization, visible unsubscribe | Heavy image-to-text ratio, spam trigger words, hidden unsubscribe |
| **Engagement Metrics** | >20% open rate, >2.5% CTR, <0.3% unsubscribe rate | 15-20% open rate, 1.5-2.5% CTR, 0.3-0.5% unsubscribe | <15% open rate, <1.5% CTR, >0.5% unsubscribe rate |

---

## Solves

This skill addresses the following ecommerce email marketing problems:

1. **Emails landing in spam or promotions tabs** -- Campaigns reach spam folders at Gmail, Outlook, or Yahoo despite legitimate content, reducing revenue from email marketing by 50-80%.

2. **Declining open and click-through rates** -- Engagement metrics drop over time as sender reputation degrades, list quality decays, or content triggers spam filters.

3. **Authentication failures and spoofing vulnerability** -- Missing or misconfigured SPF, DKIM, or DMARC records cause delivery failures and leave the domain open to phishing impersonation.

4. **High bounce rates damaging sender reputation** -- Accumulated invalid addresses, typo domains, and abandoned mailboxes generate hard bounces that erode IP and domain reputation with mailbox providers.

5. **Blacklisting and IP reputation damage** -- Sending IP or domain appears on one or more DNS-based blacklists (Spamhaus, Barracuda, SORBS), causing widespread delivery failures.

6. **Subscriber list decay and disengagement** -- Lists degrade at 25-30% per year through abandoned addresses, role accounts, and spam traps, dragging down overall deliverability.

7. **Inconsistent sending patterns triggering throttling** -- Irregular send volumes (e.g., nothing for weeks then a massive blast) cause mailbox providers to throttle or defer messages.

---

## Workflow

### Step 1: Baseline Deliverability Assessment

Establish the current state by gathering quantitative data across all relevant dimensions.

**Inputs needed:**
- Access to ESP dashboard (Klaviyo, Mailchimp, Omnisend, etc.)
- Domain and sending IP addresses
- Last 90 days of campaign performance data

**Actions:**
1. Pull inbox placement rates by provider (Gmail, Outlook, Yahoo, Apple Mail) using seed-list testing tools (GlockApps, Inbox Monster, or Everest).
2. Record aggregate open rate, click rate, bounce rate, unsubscribe rate, and spam complaint rate for last 90 days.
3. Check Google Postmaster Tools for domain and IP reputation status.
4. Run IP addresses against major blacklists: Spamhaus (SBL, XBL, PBL), Barracuda, SORBS, SpamCop, URIBL.
5. Document sending volume patterns over the last 90 days (daily/weekly volume graph).

**Output:** A baseline scorecard with numeric values for each Quick Reference dimension.

### Step 2: Authentication Audit

Verify that all email authentication protocols are correctly configured and aligned.

**Actions:**
1. Query DNS for SPF record on the sending domain. Validate syntax, check for >10 DNS lookups, confirm the ESP's include is present.
2. Verify DKIM signing by sending a test email and inspecting headers. Confirm key length is 1024-bit or higher (2048-bit preferred). Verify alignment with the From domain.
3. Check DMARC record. Assess policy level (none/quarantine/reject), alignment mode (relaxed/strict), and reporting configuration (rua/ruf).
4. If applicable, check BIMI record and VMC certificate status.
5. Verify return-path/envelope-from alignment for SPF.
6. Test with MXToolbox, dmarcian, or mail-tester.com to get a composite authentication score.

**Output:** Authentication status matrix. See `references/authentication-setup-guide.md` for remediation steps.

### Step 3: List Health Analysis

Assess the quality, composition, and engagement profile of the subscriber list.

**Actions:**
1. Export list with engagement data: last open date, last click date, total opens/clicks in 90 days, acquisition source, subscription date.
2. Segment the list into engagement tiers:
   - **Active**: Opened or clicked in last 30 days
   - **Lapsing**: Last engagement 31-90 days ago
   - **Inactive**: Last engagement 91-180 days ago
   - **Dead**: No engagement in 180+ days or never engaged
3. Identify risky address patterns: role accounts (info@, sales@, support@), disposable domains (guerrillamail, tempmail), known spam trap providers.
4. Run the list through a verification service (ZeroBounce, NeverBounce, BriteVerify) to flag invalid, catch-all, and risky addresses.
5. Calculate list decay rate and project forward 6 months.

**Output:** List health report with segment sizes, risk flags, and recommended removals. See `references/list-hygiene-guide.md`.

### Step 4: Content and Technical Scan

Evaluate email content for spam filter triggers and technical issues.

**Actions:**
1. Analyze the last 10 campaigns for spam trigger patterns:
   - Subject line: ALL CAPS, excessive punctuation, urgency words ("Act now!", "Limited time!")
   - Body: image-to-text ratio (target >60% text), spam trigger word density, URL shorteners, excessive links
   - HTML: broken tags, excessive inline CSS, missing alt text on images, non-standard fonts
2. Check email weight (target <100KB total) and image hosting (external CDN vs. embedded).
3. Verify unsubscribe mechanism: one-click List-Unsubscribe header, visible footer link, functional processing.
4. Test rendering across top 10 email clients using Litmus or Email on Acid.
5. Verify plain-text MIME part exists alongside HTML.
6. Check for proper use of preheader text.

**Output:** Content audit findings with specific fix recommendations per campaign template.

### Step 5: Sending Infrastructure Review

Evaluate the technical sending setup and its impact on deliverability.

**Actions:**
1. Determine IP type: dedicated vs. shared. If dedicated, assess warm-up status and age.
2. Review sending subdomain configuration (e.g., mail.store.com vs. store.com). Verify DNS records point correctly.
3. Analyze volume patterns: look for spikes >2x normal volume, gaps in sending, day-of-week distribution.
4. Check ESP configuration: throttling settings, retry logic, feedback loop enrollment with major providers.
5. Verify TLS encryption is enforced for transmission.
6. Review bounce handling: automatic suppression of hard bounces, soft bounce retry policy.

**Output:** Infrastructure assessment with configuration recommendations.

### Step 6: Remediation Plan

Prioritize and sequence fixes based on impact and effort.

**Priority framework:**
1. **Critical (fix immediately):** Blacklist removal, authentication failures, >2% bounce rate
2. **High (fix within 1 week):** DMARC policy upgrade, list cleaning, bounce processing fixes
3. **Medium (fix within 2 weeks):** Content optimization, sunset policy implementation, sending pattern normalization
4. **Low (fix within 1 month):** BIMI setup, advanced segmentation, A/B testing framework

**Actions:**
1. Create a sequenced action list using the priority framework.
2. For blacklist removal: identify the listing, follow the specific delisting process, document the cause and prevention measure.
3. For authentication: implement fixes per `references/authentication-setup-guide.md`.
4. For list hygiene: execute cleaning per `references/list-hygiene-guide.md`.
5. Establish sending calendar with consistent volume ramp.

**Output:** Prioritized remediation plan with owners, timelines, and success criteria.

### Step 7: Monitoring and Continuous Improvement

Set up ongoing monitoring to maintain deliverability gains.

**Actions:**
1. Configure Google Postmaster Tools alerts for reputation changes.
2. Set up automated seed-list testing on a weekly cadence.
3. Implement real-time bounce and complaint monitoring with threshold alerts:
   - Bounce rate alert: >1.5% per campaign
   - Complaint rate alert: >0.05% per campaign
4. Schedule quarterly list hygiene reviews.
5. Create a monthly deliverability dashboard tracking all Quick Reference dimensions.
6. Document a runbook for common deliverability incidents (blacklisting, sudden reputation drop, provider-specific blocking).

**Output:** Monitoring configuration and deliverability dashboard template. See `assets/quality-checklist.md` for ongoing audit use.

---

## Worked Examples

### Example 1: Fashion Ecommerce Brand with Gmail Spam Problem

**Situation:** An online fashion retailer (250K subscriber list) using Klaviyo sees their Gmail open rates drop from 22% to 9% over 8 weeks. Their Black Friday campaign drove 40% of annual email revenue last year, and the holiday season is 10 weeks away.

**Step 1 -- Baseline Assessment:**
| Metric | Current Value | Target |
|---|---|---|
| Overall open rate | 12.4% | >20% |
| Gmail open rate | 9.1% | >20% |
| Outlook open rate | 18.7% | >20% |
| Yahoo open rate | 16.2% | >20% |
| Bounce rate | 3.2% | <1% |
| Spam complaint rate | 0.12% | <0.05% |
| List size | 248,600 | -- |
| Last list cleaning | 14 months ago | Every 90 days |

Google Postmaster Tools shows domain reputation as "Low" and IP reputation as "Medium."

**Step 2 -- Authentication Audit:**
- SPF: Present but includes 11 DNS lookups (exceeds 10-lookup limit). Fails intermittently.
- DKIM: 1024-bit key, aligned. Functional but should upgrade to 2048-bit.
- DMARC: `v=DMARC1; p=none;` -- No enforcement, no reporting configured.
- Return-path: Misaligned (using Klaviyo default, not custom bounce domain).

**Step 3 -- List Health Analysis:**
| Segment | Count | Percentage |
|---|---|---|
| Active (30 days) | 62,150 | 25.0% |
| Lapsing (31-90 days) | 49,720 | 20.0% |
| Inactive (91-180 days) | 54,692 | 22.0% |
| Dead (180+ days) | 82,038 | 33.0% |

Verification service results: 8,400 invalid addresses (3.4%), 2,100 spam traps identified (0.84%), 4,200 role accounts (1.7%).

**Step 4 -- Content Scan:**
- Image-to-text ratio: 85% images, 15% text (too image-heavy)
- Subject lines frequently use ALL CAPS and multiple exclamation marks
- No plain-text MIME part in any campaign
- List-Unsubscribe header missing; only a small footer link present
- Average email size: 340KB (3.4x recommended maximum)

**Step 5 -- Infrastructure Review:**
- Shared IP through Klaviyo (acceptable)
- Sending pattern: 2-3 campaigns per week, but skipped 3 weeks in August, then sent 5 campaigns in one week
- Custom sending domain configured but bounce domain not set up

**Step 6 -- Remediation Plan:**

| Priority | Action | Timeline | Expected Impact |
|---|---|---|---|
| Critical | Remove 8,400 invalid addresses and 2,100 spam traps | Day 1 | Reduce bounce rate from 3.2% to ~1.5% |
| Critical | Fix SPF record: flatten to reduce lookups below 10 | Day 1 | Resolve intermittent SPF failures |
| High | Suppress 82,038 dead subscribers from regular campaigns | Day 2 | Reduce complaint rate, improve engagement ratios |
| High | Configure DMARC reporting: add rua tag | Day 2 | Gain visibility into authentication failures |
| High | Set up custom bounce domain in Klaviyo | Day 3 | Align return-path for SPF |
| Medium | Redesign templates: 60/40 text-to-image ratio | Week 1-2 | Reduce spam filter scoring |
| Medium | Add plain-text parts and List-Unsubscribe header | Week 1 | Improve Gmail compliance |
| Medium | Implement sunset policy: suppress 180+ day inactives | Week 2 | Long-term list health |
| Low | Upgrade DKIM to 2048-bit | Week 3 | Future-proof authentication |
| Low | Move DMARC to p=quarantine after 30 days of monitoring | Week 4 | Strengthen domain protection |

**Step 7 -- Results after 6 weeks:**
| Metric | Before | After | Change |
|---|---|---|---|
| Overall open rate | 12.4% | 24.8% | +100% |
| Gmail open rate | 9.1% | 22.3% | +145% |
| Bounce rate | 3.2% | 0.6% | -81% |
| Spam complaint rate | 0.12% | 0.03% | -75% |
| Active list size | 248,600 | 156,200 | -37% (intentional) |
| Revenue per email | $0.04 | $0.11 | +175% |

---

### Example 2: Supplement Brand Blacklisted After Migration

**Situation:** A health supplements DTC brand (80K subscribers) migrated from Mailchimp to Omnisend. Two weeks after migration, delivery rates collapse. Customer service reports customers are not receiving order confirmations.

**Step 1 -- Baseline Assessment:**
| Metric | Pre-Migration | Post-Migration |
|---|---|---|
| Delivery rate | 97.8% | 72.4% |
| Open rate | 24.1% | 8.3% |
| Bounce rate | 0.8% | 11.6% |
| Spam complaints | 0.03% | 0.22% |

**Step 2 -- Authentication Audit:**
- SPF: Old Mailchimp include still present, Omnisend include added. Record is valid but contains stale data.
- DKIM: Mailchimp DKIM key still in DNS. Omnisend DKIM not yet configured -- emails are unsigned.
- DMARC: `v=DMARC1; p=quarantine;` -- Emails failing DKIM are being quarantined by receiving servers. This is the primary cause of the delivery collapse.
- Custom bounce domain: Not configured in Omnisend.

**Step 3 -- List Health Analysis:**
During migration, the full list was imported without suppression lists. Result:
- 3,200 previously hard-bounced addresses reimported and mailed
- 1,800 previously unsubscribed contacts reimported (CAN-SPAM violation risk)
- 12,400 addresses inactive for 1+ year reimported and mailed in the first blast

The initial Omnisend campaign was sent to all 80K contacts at once -- no warm-up on the new sending infrastructure.

**Step 4 -- Content Scan:**
- Transactional emails (order confirmations, shipping) are sending from the same domain and IP as marketing -- reputation damage is affecting transactional delivery.
- Health supplement content includes terms frequently flagged by spam filters: "miracle," "guaranteed results," "doctor recommended," "free trial."

**Step 5 -- Infrastructure Review:**
- Omnisend shared IP pool: The brand's sending behavior has not yet been isolated, but volume spike triggered provider-level throttling.
- IP check reveals listings on Spamhaus SBL and Barracuda BRBL.
- No dedicated sending subdomain -- marketing and transactional both send from supplements-brand.com.

**Step 6 -- Remediation Plan:**

| Priority | Action | Timeline |
|---|---|---|
| Critical | Configure Omnisend DKIM signing immediately | Hour 1 |
| Critical | Remove old Mailchimp SPF include | Hour 1 |
| Critical | Reimport suppression lists: hard bounces, unsubscribes, spam complaints | Hour 2 |
| Critical | Submit delisting requests to Spamhaus and Barracuda with evidence of corrective action | Day 1 |
| Critical | Separate transactional emails to subdomain (transact.supplements-brand.com) with own authentication | Day 1-2 |
| High | Suppress all 12,400 long-inactive contacts | Day 1 |
| High | Begin IP warm-up: start with 500/day to engaged-only segment, double every 2-3 days | Day 2-14 |
| Medium | Set up mail.supplements-brand.com for marketing sends | Week 2 |
| Medium | Rewrite templates to remove spam trigger health claims | Week 2-3 |
| Low | Implement engagement-based sending segments in Omnisend | Week 3-4 |

**Results after 4 weeks:**
- Delivery rate recovered to 96.2%
- Delisted from both Spamhaus and Barracuda within 5 days of request
- Transactional email delivery rate: 99.4% (isolated subdomain)
- Open rate: 21.7% (approaching pre-migration levels)
- Warm-up completed successfully, sending to 45K engaged subscribers

---

## Common Mistakes

1. **Sending to the entire list without segmentation.** Mailing 180-day-inactive subscribers alongside active ones drags down engagement ratios and trains mailbox providers to deprioritize your messages. Always segment by engagement recency and adjust frequency accordingly.

2. **Ignoring Google Postmaster Tools data.** Google processes ~30% of all email. If your domain reputation shows "Low" in Postmaster Tools, you have a Gmail problem regardless of what your ESP dashboard says. Check Postmaster Tools weekly at minimum.

3. **Flattening SPF records incorrectly.** When SPF exceeds 10 DNS lookups, some senders hardcode IP addresses to flatten it. This breaks when the ESP changes IPs. Use an SPF flattening service that auto-updates, or restructure includes to stay under the limit natively.

4. **Setting DMARC to p=reject before monitoring.** Jumping straight to a reject policy without first collecting aggregate reports at p=none will cause legitimate email from third-party senders (review request tools, loyalty platforms) to be silently rejected. Always start at p=none with rua reporting, then move to quarantine, then reject.

5. **Not migrating suppression lists during ESP changes.** When switching ESPs, the suppression list (hard bounces, unsubscribes, spam complaints) must transfer. Failing to do so means remailing people who already opted out or bounced, which causes immediate reputation damage and potential legal liability.

6. **Buying or renting email lists.** Purchased lists contain spam traps, invalid addresses, and unengaged recipients. Even a small purchased list segment (5-10% of total) can poison domain reputation for months. There is no legitimate shortcut to list building.

7. **Sending high-volume campaigns on inconsistent schedules.** Going from 0 sends in a week to 500K in a day triggers volume-based throttling at every major provider. Maintain consistent sending cadence and increase volume gradually (no more than 2x per week during ramp-up).

8. **Using URL shorteners in email body.** Bit.ly, TinyURL, and similar shorteners are heavily abused by spammers. Spam filters penalize their presence. Always use full, branded URLs or your own redirect domain.

9. **Neglecting the plain-text version.** Sending HTML-only emails without a plain-text MIME alternative raises spam scores. Every email should include a well-formatted plain-text part that mirrors the HTML content.

10. **Treating deliverability as a one-time fix.** Deliverability is an ongoing discipline. Lists decay at 25-30% per year, mailbox provider algorithms change, and sending patterns shift. Quarterly audits using the full workflow are essential to maintaining inbox placement.

---

## Resources

- **Google Postmaster Tools** -- https://postmaster.google.com -- Free domain and IP reputation monitoring for Gmail delivery.
- **MXToolbox** -- https://mxtoolbox.com -- DNS lookup, blacklist checking, SPF/DKIM/DMARC validation.
- **dmarcian** -- https://dmarcian.com -- DMARC deployment and reporting platform.
- **mail-tester.com** -- https://www.mail-tester.com -- Send a test email and receive a deliverability score with specific improvement recommendations.
- **Spamhaus** -- https://www.spamhaus.org -- Check and request delisting from the most widely used DNS blacklist.
- **GlockApps / Inbox Monster** -- Seed-list based inbox placement testing across major providers.
- **ZeroBounce / NeverBounce / BriteVerify** -- Email list verification services for identifying invalid, risky, and spam-trap addresses.
- **Litmus / Email on Acid** -- Email rendering testing across clients and devices.
- **RFC 7489 (DMARC)** -- https://datatracker.ietf.org/doc/html/rfc7489 -- The DMARC specification.
- **M3AAWG Best Practices** -- https://www.m3aawg.org/published-documents -- Industry best practices for messaging anti-abuse.
