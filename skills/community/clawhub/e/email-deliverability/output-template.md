# Email Deliverability Audit Report Template

Use this template to structure deliverability audit findings. Fill in each section with data from the workflow steps.

---

## Report Header

```
DELIVERABILITY AUDIT REPORT
Client:          [Brand Name]
Domain:          [sending-domain.com]
ESP:             [Klaviyo / Mailchimp / Omnisend / etc.]
Audit Date:      [YYYY-MM-DD]
Auditor:         [Name]
Report Period:   [Start Date] to [End Date] (last 90 days recommended)
```

---

## Executive Summary

**Overall Deliverability Grade:** [A / B / C / D / F]

**Key Findings:**
1. [Most critical finding -- one sentence]
2. [Second most critical finding -- one sentence]
3. [Third finding -- one sentence]

**Estimated Revenue Impact:** [Estimated monthly revenue lost due to deliverability issues]

**Recommended Priority:** [Critical -- immediate action / High -- action within 7 days / Medium -- action within 30 days]

---

## Section 1: Baseline Metrics

| Metric | Current Value | Industry Benchmark | Status |
|---|---|---|---|
| Overall Delivery Rate | __% | >97% | [Strong/Acceptable/Weak] |
| Inbox Placement Rate | __% | >95% | [Strong/Acceptable/Weak] |
| Open Rate (aggregate) | __% | 15-25% | [Strong/Acceptable/Weak] |
| Click-Through Rate | __% | 1.5-3.5% | [Strong/Acceptable/Weak] |
| Hard Bounce Rate | __% | <1% | [Strong/Acceptable/Weak] |
| Soft Bounce Rate | __% | <3% | [Strong/Acceptable/Weak] |
| Spam Complaint Rate | __% | <0.05% | [Strong/Acceptable/Weak] |
| Unsubscribe Rate | __% | <0.5% | [Strong/Acceptable/Weak] |

**Provider-Specific Inbox Placement:**

| Provider | Inbox | Spam | Missing | Volume Share |
|---|---|---|---|---|
| Gmail | __% | __% | __% | __% |
| Outlook/Hotmail | __% | __% | __% | __% |
| Yahoo/AOL | __% | __% | __% | __% |
| Apple Mail | __% | __% | __% | __% |
| Other | __% | __% | __% | __% |

**Google Postmaster Tools:**
- Domain Reputation: [High / Medium / Low / Bad]
- IP Reputation: [High / Medium / Low / Bad]
- Spam Rate: __%
- Authentication Rate: __%

---

## Section 2: Authentication Status

| Protocol | Status | Details | Action Required |
|---|---|---|---|
| SPF | [Pass/Fail/Partial] | [Record summary, lookup count] | [Yes/No -- detail] |
| DKIM | [Pass/Fail/Partial] | [Key length, alignment status] | [Yes/No -- detail] |
| DMARC | [Pass/Fail/Partial] | [Policy level, reporting config] | [Yes/No -- detail] |
| BIMI | [Pass/Fail/N/A] | [VMC status, logo file] | [Yes/No -- detail] |
| Return-Path | [Aligned/Misaligned] | [Bounce domain config] | [Yes/No -- detail] |
| TLS | [Enforced/Optional/None] | [Encryption status] | [Yes/No -- detail] |

**SPF Record:**
```
v=spf1 [current record contents]
```
DNS Lookups: [X]/10

**DKIM Selector(s):**
```
[selector]._domainkey.[domain] -> [key summary]
```

**DMARC Record:**
```
v=DMARC1; p=[policy]; [full record]
```

---

## Section 3: List Health

**List Composition:**

| Segment | Count | Percentage | Recommendation |
|---|---|---|---|
| Active (0-30 days) | __ | __% | Continue mailing |
| Lapsing (31-90 days) | __ | __% | Reduce frequency / re-engage |
| Inactive (91-180 days) | __ | __% | Re-engagement campaign or suppress |
| Dead (180+ days) | __ | __% | Suppress from regular sends |
| Never Engaged | __ | __% | Verify and suppress |
| **Total** | **__** | **100%** | |

**Risk Flags:**

| Risk Type | Count | Percentage | Action |
|---|---|---|---|
| Invalid addresses | __ | __% | Remove immediately |
| Spam traps (known) | __ | __% | Remove immediately |
| Role accounts | __ | __% | Review and suppress |
| Disposable domains | __ | __% | Remove immediately |
| Catch-all domains | __ | __% | Monitor bounce behavior |
| Duplicate addresses | __ | __% | Deduplicate |

**List Decay Projection:**
- Current monthly decay rate: __%
- Projected list size in 6 months (without new acquisition): __
- Recommended cleaning frequency: [Monthly / Quarterly]

---

## Section 4: Content Analysis

| Factor | Finding | Score Impact | Fix Priority |
|---|---|---|---|
| Image-to-text ratio | [X% image / Y% text] | [High/Med/Low] | [Priority] |
| Spam trigger words | [Count and examples] | [High/Med/Low] | [Priority] |
| Subject line patterns | [Issues found] | [High/Med/Low] | [Priority] |
| Email size | [X KB] | [High/Med/Low] | [Priority] |
| Plain-text part | [Present/Missing] | [High/Med/Low] | [Priority] |
| List-Unsubscribe header | [Present/Missing] | [High/Med/Low] | [Priority] |
| Unsubscribe visibility | [Visible/Hidden] | [High/Med/Low] | [Priority] |
| URL shorteners | [Found/None] | [High/Med/Low] | [Priority] |
| Broken HTML | [Issues found] | [High/Med/Low] | [Priority] |
| Preheader text | [Present/Missing] | [High/Med/Low] | [Priority] |

---

## Section 5: Infrastructure Assessment

| Component | Current State | Recommendation |
|---|---|---|
| IP Type | [Dedicated/Shared] | [Recommendation] |
| IP Warm-up Status | [Complete/In Progress/Not Started] | [Recommendation] |
| Sending Subdomain | [Configured/Not Configured] | [Recommendation] |
| Bounce Domain | [Custom/Default] | [Recommendation] |
| Feedback Loops | [Enrolled/Not Enrolled] | [Recommendation] |
| Volume Consistency | [Consistent/Erratic] | [Recommendation] |

**Blacklist Status:**

| Blacklist | Status | Listing Reason | Delisting Action |
|---|---|---|---|
| Spamhaus SBL | [Clean/Listed] | [Reason if listed] | [Action if listed] |
| Spamhaus XBL | [Clean/Listed] | [Reason if listed] | [Action if listed] |
| Barracuda BRBL | [Clean/Listed] | [Reason if listed] | [Action if listed] |
| SORBS | [Clean/Listed] | [Reason if listed] | [Action if listed] |
| SpamCop | [Clean/Listed] | [Reason if listed] | [Action if listed] |
| URIBL | [Clean/Listed] | [Reason if listed] | [Action if listed] |

---

## Section 6: Remediation Plan

| # | Action | Priority | Owner | Deadline | Status | Expected Impact |
|---|---|---|---|---|---|---|
| 1 | [Action description] | [Critical/High/Med/Low] | [Name] | [Date] | [Not Started/In Progress/Done] | [Expected metric change] |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

---

## Section 7: Monitoring Plan

**Alerts Configured:**

| Alert | Threshold | Notification | Owner |
|---|---|---|---|
| Bounce rate spike | >1.5% per campaign | [Email/Slack] | [Name] |
| Complaint rate spike | >0.05% per campaign | [Email/Slack] | [Name] |
| Blacklist detection | Any new listing | [Email/Slack] | [Name] |
| Reputation drop | Below "Medium" in GPT | [Email/Slack] | [Name] |

**Review Schedule:**
- Weekly: Google Postmaster Tools check, campaign metric review
- Monthly: Seed-list inbox placement test, blacklist scan
- Quarterly: Full list hygiene audit, authentication review, content audit

---

## Appendix

**Tools Used:**
- Inbox placement: [GlockApps / Inbox Monster / Everest]
- List verification: [ZeroBounce / NeverBounce / BriteVerify]
- Authentication: [MXToolbox / dmarcian / mail-tester.com]
- Rendering: [Litmus / Email on Acid]
- Blacklists: [MXToolbox / multirbl.valli.org]

**Data Sources:**
- ESP dashboard export (date range: __)
- Google Postmaster Tools (date range: __)
- Seed-list test results (test date: __)
- List verification report (verification date: __)
