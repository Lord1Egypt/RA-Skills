# Email List Hygiene Guide

Systematic practices for cleaning, segmenting, and maintaining ecommerce email lists to protect sender reputation and maximize engagement.

---

## Why List Hygiene Matters

Email lists decay at 25-30% per year. Subscribers change jobs, abandon addresses, or lose interest. Every invalid or disengaged address you continue mailing erodes your sender reputation. Mailbox providers like Gmail and Yahoo track your engagement ratios -- the percentage of your sent mail that gets opened, clicked, or marked as spam. Mailing a bloated list full of dead addresses drives those ratios down, which pushes more of your email into spam, which further reduces engagement, creating a downward spiral.

For ecommerce specifically, list hygiene directly affects revenue. A clean 50K list that achieves 25% open rates will outperform a dirty 200K list at 8% open rates -- and cost less to send.

---

## List Verification

### When to Verify

- Before any major campaign (Black Friday, product launch)
- After importing a new list or migrating ESPs
- When bounce rates exceed 1.5% on any campaign
- On a quarterly schedule as ongoing maintenance
- Before re-engaging a dormant segment

### Verification Service Selection

Use a reputable verification service that checks for:

| Check Type | What It Catches | Priority |
|---|---|---|
| Syntax validation | Malformed addresses (missing @, invalid characters) | Essential |
| Domain validation | Non-existent domains, expired domains | Essential |
| Mailbox existence | Addresses that do not exist on valid domains | Essential |
| Spam trap detection | Known recycled and pristine spam traps | Essential |
| Disposable domain detection | Temporary email services (guerrillamail, tempmail, etc.) | High |
| Role account detection | info@, admin@, sales@, support@, webmaster@ | High |
| Catch-all domain identification | Domains that accept all addresses (cannot confirm validity) | Medium |
| Abuse/complainer detection | Addresses known to file spam complaints | Medium |

Recommended services: ZeroBounce, NeverBounce, BriteVerify, Kickbox. Budget $3-10 per 1,000 verifications.

### Post-Verification Actions

| Verification Result | Action |
|---|---|
| Valid | Keep in active list |
| Invalid | Remove immediately; add to suppression list |
| Spam trap | Remove immediately; investigate acquisition source |
| Disposable | Remove; block domain from future signups |
| Role account | Suppress from marketing; may keep for transactional if necessary |
| Catch-all | Keep but monitor; flag for removal if no engagement in 60 days |
| Risky/Unknown | Send to a small test segment first; suppress if bounce |

---

## Engagement-Based Segmentation

### Defining Engagement Tiers

Segment your list based on recency and frequency of interaction. Adjust thresholds based on your sending frequency -- these assume 2-4 emails per week.

**Tier 1 -- VIP / Highly Engaged (target: 10-15% of list)**
- Opened or clicked 3+ times in last 30 days
- Or purchased via email in last 30 days
- Treatment: Full sending frequency, early access, premium content

**Tier 2 -- Active / Engaged (target: 20-30% of list)**
- Opened or clicked at least once in last 30 days
- Treatment: Full sending frequency, standard campaigns

**Tier 3 -- Lapsing (target: 15-25% of list)**
- Last engagement 31-90 days ago
- Treatment: Reduced frequency (1-2 per week), re-engagement content, subject line testing

**Tier 4 -- Inactive (target: 10-20% of list)**
- Last engagement 91-180 days ago
- Treatment: Monthly re-engagement campaign only; sunset after one re-engagement attempt

**Tier 5 -- Dead / Unengaged (remainder)**
- No engagement in 180+ days, or never engaged after 90 days on list
- Treatment: Suppress from all sends; run one final re-engagement or remove

### Implementing Segments in Your ESP

Most ecommerce ESPs support dynamic segments based on engagement. Example Klaviyo segment definitions:

- **Engaged:** `Opened Email at least once in the last 30 days OR Clicked Email at least once in the last 30 days`
- **Lapsing:** `Opened Email at least once in the last 90 days AND Opened Email zero times in the last 30 days`
- **Inactive:** `Opened Email zero times in the last 90 days AND Was added to list more than 90 days ago`

Set campaign sending to target Engaged + Lapsing segments by default. Inactive and Dead segments should only receive re-engagement flows.

---

## Sunset Policy

A sunset policy defines when and how you stop mailing disengaged subscribers. This is the single most impactful list hygiene practice.

### Recommended Sunset Framework

```
Day 0:    Subscriber last engaged (opened or clicked)
Day 90:   Move to reduced frequency segment
Day 120:  Send re-engagement email 1 ("We miss you" / incentive offer)
Day 135:  Send re-engagement email 2 ("Last chance" / preference center)
Day 150:  Send final email ("We're removing you; click to stay")
Day 151:  No click on any re-engagement → suppress from all marketing
Day 365:  Remove from list entirely (retain in suppression list)
```

### Re-Engagement Campaign Best Practices

- **Subject lines that stand out:** Use their name, reference their last purchase, break your usual pattern ("We need to talk," "Should we stop emailing you?")
- **Offer an incentive:** 15-20% discount, free shipping, or exclusive access can recover 3-8% of inactive subscribers
- **Provide a preference center:** Let them choose frequency (weekly digest vs. daily) or topics (sales only, new arrivals only)
- **Make unsubscribing easy:** Paradoxically, making it easy to leave reduces spam complaints from people who stay
- **Measure the re-engagement series:** Track what percentage re-engage, and do not repeat the series more than once per subscriber

---

## Acquisition Hygiene

Prevent bad addresses from entering your list in the first place.

### Signup Form Best Practices

- **Double opt-in (confirmed opt-in):** Require new subscribers to click a confirmation link in a verification email. This eliminates typos, bots, and malicious signups. It reduces list growth rate by 20-30% but dramatically improves list quality.
- **Real-time validation on forms:** Use JavaScript-based validation (Kickbox, ZeroBounce API) to check addresses at the point of entry. Reject disposable domains, flag typos (gmial.com, yaho.com), and block role accounts.
- **CAPTCHA or honeypot fields:** Prevent bot signups that inject spam traps and invalid addresses.
- **Set expectations:** Tell subscribers what they will receive and how often. Mismatched expectations drive complaints.
- **Avoid pre-checked boxes:** Opt-in must be explicit. Pre-checked "subscribe to our newsletter" checkboxes during checkout produce disengaged subscribers and may violate GDPR.

### Acquisition Sources to Monitor

Track deliverability metrics by acquisition source. If addresses from a particular source (contest entry, partner co-registration, popup on a specific landing page) show high bounce or complaint rates, fix or shut down that source.

| Source | Typical Quality | Watch For |
|---|---|---|
| Website signup with double opt-in | High | Low volume but high engagement |
| Checkout opt-in (explicit) | High | Moderate engagement; transactional buyers may not engage with marketing |
| Checkout opt-in (pre-checked) | Low-Medium | High unsubscribe and complaint rates |
| Contest/giveaway entry | Low | Disposable addresses, no purchase intent |
| Partner co-registration | Low-Medium | Mismatched expectations, high complaints |
| In-store POS collection | Medium | Typo rates 5-15%, verify within 48 hours |
| Imported/purchased lists | Very Low | Never do this. Spam traps, legal liability, reputation damage |

---

## Ongoing Maintenance Schedule

### Weekly

- Review campaign-level bounce and complaint rates
- Check for any addresses that hard-bounced and verify they are suppressed
- Monitor Google Postmaster Tools for reputation changes

### Monthly

- Review engagement tier distribution -- is the active segment growing or shrinking?
- Remove any new role accounts or disposable domain signups
- Check unsubscribe processing -- are unsubscribes being honored within 24 hours?

### Quarterly

- Run full list through verification service
- Execute sunset policy on accumulated inactive subscribers
- Audit acquisition sources for quality
- Review and update segment definitions if sending frequency has changed
- Pull deliverability report and compare to previous quarter

### Annually

- Full list audit with engagement, acquisition source, and revenue-per-subscriber analysis
- Review and update sunset policy thresholds
- Benchmark against industry standards
- Clean up suppression list (remove entries older than compliance requirements)

---

## Metrics to Track

| Metric | Healthy Range | Action Trigger |
|---|---|---|
| List growth rate (net) | >2% monthly | <0% (shrinking faster than growing) |
| Hard bounce rate per campaign | <0.5% | >1% on any single campaign |
| Spam complaint rate | <0.05% | >0.08% (approaching Gmail's 0.10% threshold) |
| Unsubscribe rate per campaign | <0.3% | >0.5% consistently |
| Active subscriber percentage | >40% of total list | <30% (list is mostly dead weight) |
| Verification failure rate (quarterly) | <2% of new adds | >5% indicates acquisition problem |
| Re-engagement recovery rate | 3-8% of targeted inactives | <1% means re-engagement content needs work |

---

## Legal Compliance Notes

List hygiene intersects with legal requirements:

- **CAN-SPAM (US):** Honor unsubscribe requests within 10 business days. Suppression list must be maintained.
- **GDPR (EU/UK):** Requires explicit consent, right to erasure, and data portability. Sunset policies must account for consent records.
- **CASL (Canada):** Requires express consent with specific identification. Implied consent expires after 2 years of last purchase or 6 months of last inquiry.
- **Retention:** Keep suppression records (email address + date + reason) even after removing the full subscriber record, to prevent re-importing suppressed addresses during list migrations.
