# Email Deliverability Quality Checklist

Use this checklist for ongoing audits. Review quarterly at minimum, or before any high-stakes campaign.

---

## Authentication (8 items)

- [ ] SPF record exists and passes validation
- [ ] SPF DNS lookup count is under 10
- [ ] SPF includes all current sending services (no stale entries)
- [ ] DKIM signing is active for every sending source
- [ ] DKIM key length is 2048-bit
- [ ] DMARC record is published with rua reporting configured
- [ ] DMARC policy is at p=quarantine or p=reject
- [ ] Custom bounce/return-path domain is configured for SPF alignment

## Sender Reputation (7 items)

- [ ] Google Postmaster Tools domain reputation is "Medium" or higher
- [ ] Google Postmaster Tools IP reputation is "Medium" or higher
- [ ] Sending IP/domain is clean on Spamhaus (SBL, XBL, PBL)
- [ ] Sending IP/domain is clean on Barracuda BRBL
- [ ] Sending IP/domain is clean on SORBS, SpamCop, and URIBL
- [ ] Feedback loops are enrolled with major providers (Outlook, Yahoo, AOL)
- [ ] Google Postmaster spam rate is below 0.10%

## List Hygiene (9 items)

- [ ] List verified through a validation service within the last 90 days
- [ ] Hard bounce suppression is processing automatically after each send
- [ ] Unsubscribe requests are honored within 24 hours
- [ ] Sunset policy is defined and actively enforced
- [ ] Subscribers inactive for 180+ days are suppressed from regular campaigns
- [ ] Role accounts (info@, admin@, sales@) are excluded from marketing sends
- [ ] No purchased, rented, or scraped addresses exist in the list
- [ ] Signup forms use double opt-in or real-time validation
- [ ] Acquisition sources are tracked and monitored for quality

## Sending Infrastructure (6 items)

- [ ] Sending subdomain is configured (not sending from bare root domain)
- [ ] Transactional and marketing emails use separate subdomains or IPs
- [ ] Sending volume is consistent week-over-week (no >2x spikes)
- [ ] TLS encryption is enforced for email transmission
- [ ] Bounce handling retries soft bounces appropriately and suppresses persistent failures
- [ ] IP warm-up was completed before reaching full volume (if dedicated IP)

## Content Quality (10 items)

- [ ] Email size is under 100KB total
- [ ] Image-to-text ratio is at least 60% text / 40% images
- [ ] Plain-text MIME part is included alongside HTML
- [ ] List-Unsubscribe header (RFC 8058 one-click) is present
- [ ] Unsubscribe link is visible and functional in email footer
- [ ] No URL shorteners (bit.ly, tinyurl, etc.) in email body
- [ ] Subject lines avoid ALL CAPS, excessive punctuation, and spam trigger phrases
- [ ] Preheader text is set and meaningful (not default or empty)
- [ ] Alt text is present on all images
- [ ] HTML is well-formed with no broken tags or unclosed elements

## Engagement and Monitoring (6 items)

- [ ] Open rate is above 15% across the active list
- [ ] Spam complaint rate is below 0.05% per campaign
- [ ] Hard bounce rate is below 1% per campaign
- [ ] Unsubscribe rate is below 0.5% per campaign
- [ ] Engagement-based segments are defined and used for send targeting
- [ ] Deliverability dashboard or alerting is configured and reviewed weekly

## Compliance (4 items)

- [ ] Physical mailing address is included in email footer
- [ ] Sender name and From address accurately identify the brand
- [ ] Consent records are stored for each subscriber (date, source, method)
- [ ] Suppression list is maintained across ESP migrations (bounces, unsubs, complaints)

---

**Total items: 50**

**Scoring guide:**
- 45-50 checked: Strong deliverability posture
- 35-44 checked: Acceptable with improvement areas
- 25-34 checked: Weak -- prioritize remediation
- Below 25: Critical -- deliverability is at significant risk

**Review frequency:** Quarterly full audit. Weekly spot-check on Engagement and Monitoring section.
