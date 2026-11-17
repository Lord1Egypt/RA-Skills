# Marketing Compliance — Consent, Claims, Disclosure, Rights

The CMO carries personal-scale reputational risk and company-scale legal risk on four things: how data was collected, what was claimed, what was disclosed, and what was used without permission. Rules differ by jurisdiction and change; what follows is the durable structure plus where to stop and get counsel.

## Red Flags — Stop and Route to Counsel

| Signal (observable) | Suspicion | Action |
|---------------------|-----------|--------|
| A list was bought, scraped, or "found", or its origin cannot be evidenced | No lawful basis to contact | Do not send. Suppress the list; keep it out of the ESP entirely |
| Personal data of EU/UK/Brazil/California residents processed with no documented basis or notice | Data-protection exposure | Stop the processing, involve the DPO or counsel before the next send |
| A performance, income, health, safety, or environmental claim with no evidence on file | Unsubstantiated claim | Pull the claim until substantiation exists in writing |
| A competitor named alongside a factual comparison you cannot source and date | Comparative-advertising exposure | Remove or source it against a dated, reproducible test |
| Personal data exposed, lost, or accessed without authorization | Breach with statutory deadlines | Legal and security lead; marketing publishes nothing before counsel clears it (`comms.md`) |
| A promotion with a prize, an entry cost, and a random winner | Possible unlawful lottery | Redesign (free entry route or skill-based) before announcing |
| Children under 13, or a product plausibly appealing to them, in the targeting | Children's-privacy regime | Counsel before any collection or targeting |
| A regulated category (health claims, finance, alcohol, gambling, political) in the copy | Sector-specific rules and pre-clearance | Counsel and, where required, platform pre-approval before launch |

Anything in this table suspends the playbooks in this skill until it is resolved.

## Consent and Contactability

- **Collect the basis, store the proof.** For every contact record, keep what they consented to, when, how, and the exact wording shown. A consent you cannot evidence is not a consent.
- **Consent is per channel and per purpose.** An email opt-in is not an SMS opt-in; a product-update opt-in is not a promotional opt-in.
- **EU/UK (GDPR/ePrivacy)**: a lawful basis is required for processing and, for most marketing email to individuals, prior consent; non-essential cookies and trackers need consent *before* they fire. Penalties reach the higher of €20 million or 4% of global annual turnover — this is a board-level risk, not a marketing detail.
- **US (CAN-SPAM)**: commercial email needs a valid physical postal address, honest headers and subject lines, and a working opt-out honoured within 10 business days. It is an opt-out regime — which is why the operational discipline in `lifecycle.md` matters more than the legal floor.
- **Canada (CASL)**: express or documented implied consent, with implied consent generally limited to a defined window after a transaction or inquiry. Among the strictest regimes for B2B email.
- **SMS and calls (US TCPA and analogues)**: prior express written consent for marketing messages to mobiles, plus quiet-hour restrictions. Text-message compliance failures are the most reliably litigated area in this file.
- **Suppression is global.** An unsubscribe applies across every system and every sender in the company, immediately. Two ESPs with unsynchronized suppression lists is a violation waiting to be reported.

## Claims and Substantiation

- Have the evidence **before** dissemination, not on request. Keep a claims file: the claim as written, the evidence, the date, the owner.
- "Up to" and best-case claims are read against the typical result; if the typical customer gets a fraction of it, the claim is misleading even when technically true.
- Testimonials and case studies require written permission and must reflect typical experience or say plainly that they do not.
- Comparative claims against a named competitor need a reproducible, dated test methodology and a re-check when their product changes. Screenshots age badly.
- Awards, certifications, and security posture: state exactly what was certified and when. "SOC 2 compliant" when a report is in progress is a claim someone in procurement will check.
- **Never fabricate**: statistics without a source, customers you do not have, logos of companies that are only trialling, reviews written in-house. This is where marketing careers end, not merely campaigns.

## Disclosure

- Paid endorsements, affiliate links, gifted products, and employee posts about their own employer all require a clear and conspicuous disclosure of the material connection (FTC Endorsement Guides in the US, equivalents elsewhere). "Clear and conspicuous" means before the fold, in the same medium, not buried in hashtags (`comms.md`).
- Sponsored content and native advertising must be labelled as advertising in the publication itself.
- Automatically generated or synthetic media in ads: disclosure obligations are expanding and platform policies already require it in several categories — check the current rule for the specific platform and market before shipping.
- Political and issue advertising carries its own registration and disclosure regimes; do not run it without specialist advice.

## Rights and Assets

- **Trademark clearance before attachment**: run a clearance search before naming a product, a campaign, or a category (`positioning.md`). Discovering a conflict after launch means paying twice.
- **Licensing**: stock images, fonts, music, and video have use-scope limits (territory, medium, duration, paid vs. organic). A "royalty-free" asset is not automatically licensed for paid advertising.
- **Customer logos and names** require permission, and the permission usually has scope and a term. Check the contract clause before the website refresh.
- **Employee and user-generated content**: get a written release for faces and voices. A UGC repost is a new use for a purpose the creator did not agree to.
- **AI-generated assets**: verify the tool's output-rights terms and your ability to enforce against copying before making one a distinctive brand asset (`brand.md`).

## Accessibility

Marketing sites are covered by accessibility expectations and, in a growing number of jurisdictions, by law. The practical floor: WCAG 2.1 AA — sufficient colour contrast, keyboard navigation, alt text with meaning, captions on video, forms with labels and readable errors. Beyond the legal exposure, captions and contrast measurably widen reach in feeds watched without sound.

## Sweepstakes, Contests, and Referral Incentives

Prize + chance + consideration is a lottery in most jurisdictions and is generally unlawful for private companies. Remove one element: a free entry route ("no purchase necessary"), or make it skill-judged. Publish full rules, eligibility, odds where required, the sponsor's identity, and the end date; register where thresholds require it; and exclude jurisdictions you cannot comply with rather than hoping.

Referral incentives interact with platform terms too: paying for reviews, or rewarding them in ways review sites prohibit, gets the whole profile removed (`demand.md`).

## Operating Discipline

- One legal review gate for every claim-bearing asset, sized to the risk: template-based copy self-serves against an approved claims library; anything new goes to review.
- Keep the claims library and the consent records where the team writing copy can actually see them.
- Re-verify jurisdiction-specific rules before entering a new market (`international.md`) and before a regulated-category campaign. Rules in this file describe the durable shape; the current text of any of them is what counsel confirms.
