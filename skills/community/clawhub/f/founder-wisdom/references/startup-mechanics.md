# Startup Legal Mechanics

The legal and structural decisions you make in the first months of a company set the floor for everything that comes after. Most of them are cheap to get right and expensive to get wrong. This file draws on Carolynn Levy, Jon Levy, and Jason Kwon's YC Startup School lecture on legal mechanics.

This file is not legal advice. Treat it as a checklist of what experienced founders typically do, with the recognition that your specific situation may differ and a qualified startup attorney should sign off on the details.

## Core axioms

**Incorporate as a Delaware C-Corp from day one.** Delaware is the default for venture-backed tech startups because the legal precedent is mature, the process is fast, and investors expect it. The C-Corp structure (versus LLC or S-Corp) is required for venture investment in nearly all cases. Founders who incorporate as an LLC "to keep things simple" usually end up paying lawyers to convert to a Delaware C-Corp before their first priced round. Skip the conversion cost.

**Use a startup-focused incorporation service.** Clerky and Stripe Atlas are the standard tools. They don't stop after formation — they handle the post-incorporation documents (board resolutions, stock purchases, IP assignments) that most founders forget about. Forming the entity is 20% of the work; getting the rest of the paperwork right is the 80% that protects you.

**Use a startup-focused incorporation service.** Clerky and Stripe Atlas are the standard tools. They don't stop after formation — they handle the post-incorporation documents (board resolutions, stock purchases, IP assignments) that most founders forget about. Forming the entity is 20% of the work; getting the rest of the paperwork right is the 80% that protects you.

Quick comparison: **Stripe Atlas** is cheaper (around $500), processes faster (1–2 days), files 83(b) elections electronically, integrates with Mercury/Brex for pre-EIN banking, but stops after initial formation. **Clerky** costs more (~$800 lifetime), processes a little slower (2–3 days), but supports ongoing legal workflows (SAFEs, hiring docs, equity grants) for the life of the company. Atlas is better for founders on a tight budget who want fast formation. Clerky is better for venture-track companies planning to raise within 12–18 months because it grows with you. Both are dramatically better than hiring a lawyer to draft from scratch at the formation stage.

**Treat the corporation as a separate entity from day one.** Open a corporate bank account. Don't pay company expenses from your personal card and "expense them later." Don't pay personal expenses from the corporate account. The discipline isn't about taxes (though it matters there too); it's about establishing that the corporation is a real, separate legal entity. Co-mingling can pierce the corporate veil and put your personal assets at risk if anything ever goes wrong.

**All founders are subject to vesting — including the founders.** Standard is four years with a one-year cliff. If you walk at month 11, you keep zero shares. If you walk at month 14, you keep 25%. This is non-negotiable for any company that will raise outside capital — investors will require it if you don't have it. Founders who skip vesting because "we trust each other" learn the hard way when one co-founder leaves at month 18 with 25% of the company.

**Allocate stock by future execution, not past contribution.** All the hard work and value creation is ahead of you. Founders who allocate based on "I had the idea first" or "I spent six months on the prototype" are pricing the past, which is cheap compared to the future. The negotiation should be: who's committed to working full-time, who's contributing what skills, who's accepting what cash compensation tradeoff, and who's bringing what network. Past contribution is one factor, not the deciding one.

**Founders contribute IP to the company as part of the stock purchase.** This is the step founders forget. When you buy your founder shares, the consideration is usually a small amount of cash plus the assignment of any IP you've created related to the business. If you wrote prototype code at MIT and the company never formally takes ownership of it, the IP belongs to you (or possibly to MIT) — not the company. Investors will catch this in diligence and either kill the round or force you to fix it under time pressure. Get the IP assignment right at incorporation.

**File the 83(b) election within 30 days of purchasing founder stock.** Critical for tax reasons that take 20 pages to explain properly. The short version: filing 83(b) lets you pay tax on the stock at its (very low) value today rather than at its (much higher) value as it vests. If you miss the 30-day window, you can owe ordinary income tax on the vested value of your stock every year for the next four years. This has destroyed founders' personal finances. As of 2025, the IRS supports electronic filing via Form 15620 through ID.me — substantially better than the certified-mail-and-pray method that used to be the only option. File the same day you buy your stock so you don't forget.

**Section 1202 (QSBS) is the most consequential tax provision founders ignore.** Qualified Small Business Stock allows founders and early shareholders to exclude up to $15M (or 10x basis, whichever is greater) in capital gains at exit — federal tax of $0 on a qualifying exit. This is real money, often the largest single financial decision in a founder's career, and it depends on choices made at incorporation. The eligibility requirements are non-trivial:
- The company must be a domestic C-Corp at the time of issuance. LLCs, S-Corps, and partnerships don't qualify, and any conversion later only starts the clock from the conversion date — pre-conversion shares are permanently disqualified.
- Aggregate gross assets must stay under $75M (post-July 2025; $50M for shares issued earlier) at the moment of issuance.
- At least 80% of assets must be used in an active qualified trade or business. SaaS qualifies. Professional services (law, medicine, consulting, finance) don't.
- The stock must be originally issued — bought directly from the company, not on a secondary market.
- Under the 2025 OBBBA tiered structure for shares issued after July 4, 2025: hold 3 years for 50% exclusion, 4 years for 75%, 5 years for 100%. Earlier shares require the full 5-year hold for any exclusion.

The S-Corp trap is the most expensive QSBS mistake. Founders who file an S-Corp election (Form 2553) for short-term tax convenience permanently disqualify their QSBS treatment for the period of the election. Don't do it unless you've consulted a startup tax specialist and explicitly decided QSBS doesn't apply to your situation.

**Section 1045 lets you defer QSBS gains by rolling into new QSBS.** If you sell qualifying stock before hitting the 5-year (or new tiered) holding period, you can defer the gain by reinvesting the entire proceeds into newly-issued QSBS within 60 days. Useful for serial founders and early-stage angels. Original stock must have been held for more than 6 months. The replacement stock's basis is reduced by the deferred gain.

**Pre-money vs. post-money option pool: the silent down-round.** When investors require an option pool expansion to cover hires before the next round, they almost always insist it be created **pre-money** — which means the dilution falls entirely on the founders and existing shareholders, not on the new investors. A $10M pre-money round with a "10% pre-money option pool" effectively reduces your true valuation by 10% before the new money comes in. Negotiate for the smallest option pool that genuinely covers planned hires through the next round, and understand that this is one of the most consequential terms in the term sheet — often more impactful than the headline valuation.

**Set up vesting documentation before your first hire.** Every employee, advisor, and contractor who gets equity should sign a stock option agreement with vesting terms, board approval, and a current 409A valuation. Cap-table cleanliness is one of the things investors diligence first. Sloppy early grants compound into months of legal cleanup at exactly the wrong moment.

**Use SAFEs or convertible notes for early money, then equity for priced rounds.** YC's standard SAFE (Simple Agreement for Future Equity) is the simplest legal instrument for seed-stage capital. Convertible notes are more complex but sometimes appropriate. Priced equity rounds (Series Seed, Series A) come later, when valuation is more credible. Founders who try to do priced rounds at the very earliest stage often overpay in legal fees and dilute themselves more than necessary.

**Use Y Combinator's free legal documents where appropriate.** YC publishes free, lawyer-vetted standard forms for SAFE notes, founder agreements, employee option grants, and other common documents at ycombinator.com/documents. Using standard documents reduces legal cost and signals to investors that you're not trying to negotiate non-standard terms. Negotiate only the things worth negotiating.

**Advisory boards rarely earn their equity.** Founders set up advisory boards because it feels like a milestone — "we have advisors!" — but most advisors deliver less than the equity they're granted is worth. Be ruthless: a great advisor who gives you 30 high-impact hours a year is worth 0.25%. An advisor who shows up to one dinner a quarter is worth zero. Use the standard YC Advisor Agreement (the FAST template) with monthly vesting and clear deliverables, not nebulous "open to call when needed" arrangements.

**Don't form a formal board too early.** At the seed stage, your board is usually just the founders. You don't need an "advisory board" or "board of directors" with outside members until investors require it (typically at Series A). Adding board members early creates governance overhead without corresponding value. Keep decision rights with the people doing the work.

## Common founder mistakes

- Incorporating in California or Nevada because it's where they live. Almost always re-incorporated in Delaware later at significant cost.
- Operating as a partnership or LLC for the first year, then converting. The conversion is doable but expensive and creates tax complications — and permanently disqualifies any pre-conversion shares from QSBS treatment.
- Electing S-Corp status (Form 2553) for short-term tax convenience. Permanently disqualifies QSBS for the period of the election. Can cost millions at exit.
- Skipping the 83(b) election because the founder didn't know about it or thought it didn't apply. Painful and irreversible.
- Accepting a "pre-money option pool" without negotiating its size. A 10% pre-money pool reduces effective valuation by ~10% — often more impactful than the headline number that founders fixate on.
- Splitting equity 50/50 with a handshake and no vesting. The single most common founder-breakup catastrophe.
- Letting an employee or contractor work for months without signed IP assignment paperwork. The work they produce may not legally belong to the company.
- Promising equity verbally to early employees ("we'll figure it out, you'll get 1%") without board approval, stock option agreements, or 409A valuations. These promises become disputes at exit.
- Hiring a generalist lawyer instead of a startup specialist. Startup law has its own conventions and a non-specialist will either overcharge or miss things.
- Giving up board seats to angel investors. Board seats are scarce and powerful; once granted, almost impossible to take back. Use observer rights or just regular investor updates instead.

## What to read

- [YC's free legal documents](https://www.ycombinator.com/documents) — SAFE forms, founder agreements, option grants
- "[Startup Legal Mechanics](https://www.ycombinator.com/library/7R-startup-legal-mechanics)" — Levy/Levy/Kwon lecture
- "[A Guide to Seed Fundraising](https://www.ycombinator.com/library/4A-a-guide-to-seed-fundraising)" — Geoff Ralston (covers the legal mechanics of SAFEs and equity rounds)
