# Phishing, BEC And Account Takeover

The mail was the lure; the mailbox is the incident. Everything below assumes the message succeeded until proven otherwise, because the report you receive is the one somebody noticed.

**Before investigating a reported message**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` for the mail platform and its audit tier — whether per-item read logging exists decides what you can ever prove — plus `indicators.md` if `## Boxes` names it (this sender or domain may already be known-bad) and `~/Clawic/data/domains/domains.md` for the org's own SPF/DKIM/DMARC posture.

**Contents:** [Triage Of A Reported Message](#triage-of-a-reported-message) · [Reading The Headers](#reading-the-headers) · [The Five Lure Families](#the-five-lure-families) · [When The Credential Was Entered](#when-the-credential-was-entered) · [Business Email Compromise](#business-email-compromise) · [The Mailbox Sweep](#the-mailbox-sweep) · [Payment Fraud: Recovering The Money](#payment-fraud-recovering-the-money) · [Tenant-Wide Hunt](#tenant-wide-hunt) · [Controls, Ordered By Path Removed](#controls-ordered-by-path-removed) · [Simulations: How To Not Make It Worse](#simulations-how-to-not-make-it-worse)

## Triage Of A Reported Message

Six questions, in this order, because each one can end the investigation:

1. **Did anyone interact?** Clicked, entered credentials, opened the attachment, replied, or paid. A reported-but-untouched message is a detection success and a five-minute job; anything else is an incident.
2. **Who else received it?** Search the tenant by sender, subject, URL and attachment hash — the report is one sample of a campaign, and the person who did not report is the incident.
3. **What did the link actually serve?** Detonate in a sandbox or an isolated browser, never on a corporate endpoint. Credential-harvesting page, malware download, OAuth consent prompt, or benign — four completely different incidents.
4. **Is this targeted or commodity?** Correct name, correct project, correct supplier and correct timing means the attacker has context — usually from a compromised mailbox on one side of the conversation, sometimes the other party's.
5. **Is the sending domain a lookalike, a compromised legitimate sender, or the real one spoofed?** A compromised legitimate sender passes every authentication check, which is why authentication results alone are not a verdict.
6. **Is there a payment in flight?** If yes, the money is the clock (below) and it outranks the forensics.

## Reading The Headers

| Field | What it tells you |
|---|---|
| `Authentication-Results` | SPF, DKIM and DMARC verdicts as the receiving system computed them. **A pass means the mail was authorized by that domain, not that it is safe** — attacker-owned domains pass their own SPF |
| `Return-Path` versus `From` | Alignment. SPF checks `Return-Path`; the user reads `From`. DMARC exists precisely because those can differ |
| `DKIM-Signature` `d=` | Which domain actually signed. Compare with the visible `From` domain — a mismatch with a DMARC pass means an authorized third-party sender |
| `Received` chain, bottom-up | The real path. The lowest hop is the closest to the origin; hops above a legitimate gateway can be forged |
| `Reply-To` | The classic BEC tell: display name and `From` look right, replies go elsewhere |
| Message-ID and X-headers | Bulk tooling, sending platform, campaign correlation across recipients |
| Display name | Nothing at all — it is free text. On mobile clients it is frequently the *only* thing shown, which is why display-name impersonation still works |

Homoglyph and lookalike domains need a byte-level look, not an eyeball: `rn` versus `m`, Cyrillic characters, a hyphen inserted, a TLD swap. Punycode (`xn--`) in a domain is worth an immediate flag.

## The Five Lure Families

| Family | Signature | The move it wants |
|---|---|---|
| Credential harvest | A branded login page on a lookalike or a legitimate hosting service, sometimes behind a CAPTCHA to defeat sandboxes | Password plus a real-time MFA code |
| AiTM proxy | Same, but the page relays to the real login and captures the **session cookie** | A valid session that MFA never sees again |
| OAuth consent | A genuine provider consent screen for an attacker-controlled app requesting mail and file scopes | Persistent token access with no password involved |
| Malware delivery | Archive, ISO, LNK, macro-enabled or script attachment; increasingly a link to a legitimate cloud-storage file | Execution |
| Pure social engineering | No link, no attachment; a payment change, a gift-card request, a "call this number", an MFA-fatigue push, or a help-desk reset request | A human action |

**AiTM is why "we had MFA" is not a conclusion.** The stolen artifact is the session cookie, so the attacker inherits an already-authenticated session and never faces a second factor. The tells are a sign-in from an unfamiliar device id with a valid token, and no corresponding MFA challenge in the logs. Only phishing-resistant factors bound to the origin (FIDO2/WebAuthn, passkeys) break this class — token-binding and strict conditional access narrow it.

## When The Credential Was Entered

Assume compromise and evict completely — the password is the least important part (SKILL.md Rule 5, full list in `identity.md`). Order matters:

1. Revoke sessions and refresh tokens **first**, then reset the password. Reset-then-revoke leaves a window where the attacker's live session survives the reset and can re-establish itself.
2. Re-enrol MFA if there is any chance the attacker registered a factor or a device, and check for newly registered authentication methods in the window — attacker-added MFA is the persistence people miss because the account then looks correctly protected.
3. Sweep the mailbox (below) before telling the user it is resolved.
4. Check what else uses that password. Reuse is the norm; the personal email and the password manager are the two that convert an account compromise into everything.

## Business Email Compromise

The expensive one, and it usually involves no malware at all. Two shapes:

- **Your mailbox is compromised.** The attacker reads for days to learn the invoice cycle, the tone, the approvers and the holiday schedule, then intervenes in a live thread with correct context. Inbox rules hide the replies from the real owner.
- **Their mailbox is compromised** — a supplier, a client, a law firm mid-transaction. Everything authenticates correctly because the mail is genuine. Your control here is the out-of-band verification step, not any mail filter.

Signatures worth alerting on: a rule that files replies containing "invoice", "payment" or "bank" into RSS Feeds, Archive or Deleted; forwarding to an external address; a reply-to on an internal thread that differs from the sender; a bank-detail change arriving inside an existing thread; and urgency plus secrecy plus a channel change ("do not call, I am in a meeting"), which is the pattern rather than any single indicator.

**The verification rule that removes the path**: any change to payment details is confirmed by calling a number from your own records — never a number in the email, never a number in the new invoice — and the confirmation is documented. Apply it to every payment change regardless of who appears to be asking. It is the only control in this file that works when both mailboxes authenticate perfectly.

## The Mailbox Sweep

After any suspected mailbox compromise, enumerate all of it — this is a checklist because every item has been the thing that was missed:

- Inbox rules, including hidden and disabled ones, and rules on shared mailboxes the account can access
- Forwarding: mailbox-level, rule-level, and any tenant-level transport rule
- Delegates, "send as" and "send on behalf" permissions
- Connected applications and OAuth grants, plus any newly created service principal with mail scopes
- Registered authentication methods and devices added in the window
- Sent items and Deleted items — attackers delete their own sent mail, and recoverable items still hold it
- Signature block modifications (an inserted bank detail or link survives every future message)
- Recent searches performed in the mailbox where the platform records them: the search terms are the attacker's shopping list — "wire", "invoice", "password", the CFO's name — and they tell you the objective directly
- Item-level access logs where the licence provides them; where it does not, the scope of what was read is *unknown* and must be reported that way

## Payment Fraud: Recovering The Money

If money moved, the recovery window is hours and it outranks the forensics:

1. Call the sending bank immediately and ask for a recall or, for a wire, a SWIFT recall message. Speed is the only variable that matters.
2. Report to the national fraud or cybercrime channel — in the US the FBI's IC3 operates a Recovery Asset Team that can freeze domestic transfers, and its effectiveness collapses after the first day.
3. Notify the receiving bank in writing that the account is receiving fraudulent funds.
4. Preserve everything: the full message with headers, the invoice, the approval trail, the payment instruction.
5. Notify the insurer — social-engineering fraud is often a separate policy sub-limit from the cyber cover, and the claim has notice requirements of its own.

Then the security question: which mailbox was compromised, yours or theirs? If theirs, you still have an incident — every thread that party sees is exposed, and the same actor will try the pattern on their other customers.

## Tenant-Wide Hunt

One reported message is a sample. Search the estate for: the sender address and its domain, the sending IP and ASN, the URL and its domain, the attachment hash, and the subject pattern. Then hunt for the *outcome* rather than the message — sign-ins from the phishing infrastructure's ASN, new inbox rules created tenant-wide in the window, new OAuth consents, and impossible-travel events for anyone in the recipient list. Purge the message from mailboxes where the platform allows it, and tell recipients you did.

## Controls, Ordered By Path Removed

1. **Phishing-resistant MFA** on mail, the identity provider, VPN and admin access. Removes credential phishing and AiTM as a class; nothing else in this list does.
2. **A one-click report button, and a measured report rate.** Users are the sensor that catches what the filter missed. The metric is report rate and time-to-first-report, never click rate — and punishing clickers collapses reporting, which hides the real incidents.
3. **Alerts on the outcome, not the lure**: inbox-rule creation, external forwarding, new OAuth consent, new MFA method, impossible travel. These fire on the incident even when the message was never reported.
4. **Payment-change verification out of band**, documented, with no exceptions for seniority — the exception for the CEO is the entire attack.
5. **DMARC at `p=reject` with SPF and DKIM aligned** on every domain you own, including the parked ones nobody uses for mail. It stops exact-domain spoofing and does nothing whatsoever about lookalikes — those need detection and user reporting.
6. **External-sender banners** that mark genuinely unusual mail; a banner on every external message is furniture nobody sees within a week.
7. **Block or quarantine the delivery formats you never legitimately use** — ISO, IMG, LNK, macro-enabled documents from outside — which removes most attachment-based delivery in one policy.
8. **Registration of obvious lookalikes** you can afford, and monitoring for new ones against your brand.

## Simulations: How To Not Make It Worse

- Measure report rate and time-to-first-report. Click rate alone drives programmes toward punishment and away from information.
- Never use rewards, salary, or bereavement themes. The short-term learning is not worth the durable damage to trust in internal communications.
- Anyone who clicks gets a 60-second explanation of the specific tell they missed, not a course. The teachable moment is measured in seconds.
- A department clicking at high rates is a process finding, not a people finding — usually a workflow that genuinely does involve unexpected attachments from strangers, in which case the fix is the workflow.
- Tell the help desk before the campaign, or the first genuine incident of the week gets dismissed as "the test".

Write what the incident produced (`memory-template.md`): the incident row with the awareness timestamp and what the attacker could read in `incidents/<year>.md`; the sender domains, URLs and hashes worth blocking beyond this incident in `indicators.md`, defanged with an expiry; mail-authentication posture and any registered lookalike in `~/Clawic/data/domains/domains.md`; the new detection for inbox-rule creation, external forwarding or OAuth consent in `## Detections` with its precision; the missing control — payment verification, phishing-resistant MFA, audit tier — as a `## Findings` row with owner and due date; the BEC playbook and the payment-verification procedure in `~/Clawic/data/cybersecurity/artifacts/` with their `## Boxes` lines; the simulation cadence and the DMARC report review as `## Due` rows. If the other party's mailbox was the compromised one, they are a row in `~/Clawic/data/contacts/contacts.md` with what they own, and a vendor row in `## Vendors` if they hold data or access.
