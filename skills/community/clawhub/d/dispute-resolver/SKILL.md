---
name: dispute-resolver
description: Generate professional, evidence-grounded responses to refund disputes and customer complaints that protect the seller while keeping the buyer relationship intact. Use when answering refund/return disputes, platform claims, chargebacks, negative-review escalations, or drafting dispute-response playbooks.
---

# Dispute Resolver

Refund disputes and escalated complaints are one of the highest-stakes interactions an ecommerce seller faces — handle them poorly and you risk negative reviews, platform penalties, or lost customers; handle them well and you can convert a frustrated buyer into a loyal one. This skill generates professional, structured responses to customer disputes that are grounded in the evidence you provide, compliant with platform policies, and calibrated to de-escalate tension while protecting your legitimate business interests.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| First move | Classify dispute type + check deadline + inventory evidence before writing a word | Read the claim twice, list what's known vs. claimed | Fire off a defensive reply from emotion |
| Evidence use | Specific, dated, attached: tracking scan, photo timestamp, listing screenshot, chat log | Referenced precisely in text ("delivered 14:32 June 3, GPS-confirmed") | "Our records show you're wrong" |
| Tone | Empathy first sentence, facts middle, resolution last — never sarcasm, never blame | Neutral professional | Defensive, accusatory, or groveling with instant full refund |
| Resolution math | Decision matrix: refund cost vs. fight cost vs. lifetime value vs. precedent risk | Case-by-case judgment with the costs at least listed | Always fight, or always fold |
| Platform response | Within platform SLA, using the platform's required evidence format | Within 24h with evidence | After the deadline (= automatic loss) |
| Buyer communication | Separate message from the platform evidence submission, written for the buyer | One message covering both | Treating the buyer message as the legal brief |
| Pattern handling | Log every dispute by type/SKU/carrier; fix root causes quarterly | Note repeat offenders | Treat every dispute as a one-off |

## Solves

1. Dispute responses written angry — defensive replies that turn a winnable case into a penalty and a one-star review.
2. Evidence that exists but never gets used: tracking data, photos, chat logs sitting unorganized while the appeal window closes.
3. Not knowing when to fight vs. when to refund — losing money on both ends by fighting $8 disputes and folding on $200 fraud.
4. Platform-specific evidence requirements (TikTok Shop, Shopee, Amazon, PayPal/Stripe chargebacks) that sellers discover after losing.
5. Refund-abuse patterns (serial "item not received", used-item returns, wardrobing) handled case-by-case instead of systemically.
6. Buyer messages and platform submissions confused into one document that serves neither audience.
7. Disputes treated as firefighting with no log, so the same product defect generates the same dispute forever.

## Workflow

### Step 1 — Triage the dispute
Classify the type: item not received (INR), item not as described (INAD/SNAD), damaged in transit, wrong item, return condition dispute, unauthorized purchase/chargeback, or service complaint escalation. Capture: platform and its response deadline, order value, dispute history of this buyer, and what stage this is (first message, platform claim, appeal, chargeback). Deadlines rule everything — a perfect response after the SLA is a loss.

### Step 2 — Inventory the evidence
List what exists vs. what's claimed: tracking events (delivery scan, GPS/photo confirmation), weight at carrier intake, product photos/QC records before shipping, listing content as the buyer saw it (screenshot the live listing NOW — it proves what was promised), serial/batch numbers, chat history, return-package photos and weights, prior dispute records for this buyer. Mark each item: have / can get / doesn't exist. Never assert evidence you cannot attach.

### Step 3 — Decide the resolution strategy
Run the decision matrix (see `references/resolution-decision-matrix.md`): full refund (cost of goods low, customer valuable, case weak, or goodwill ROI positive), partial refund (genuine but minor issue, or shared fault), replacement (defect confirmed, product margin supports it), fight with evidence (clear fraud/abuse or strong proof and meaningful value), or refund + report (fraud below fight threshold — refund but log and report the buyer). The output states WHICH strategy and WHY, including the math.

### Step 4 — Draft the platform/evidence response
Structure for the platform reviewer (a stranger with 90 seconds): one-line case summary → numbered facts with dated evidence references → policy citation (the platform's own rule that decides the case) → requested outcome. No emotion, no buyer-blaming adjectives, no walls of text. Format evidence per the platform's requirements (file types, what counts as proof of delivery, return-condition photo standards) — see `references/platform-rules.md`.

### Step 5 — Draft the buyer message
Separate document, different goal: keep the customer. Structure: acknowledge the frustration (one genuine sentence, no corporate apology spam) → state what you found, factually and without accusation → offer the resolution with clear next steps → close forward-looking. If fighting the claim, the buyer message stays respectful and explains what the evidence shows without "calling them a liar" — leave the verdict to the platform. Tone calibration patterns in `references/response-templates.md`.

### Step 6 — Handle the outcome and appeals
If lost: assess appeal viability (new evidence? policy misapplied?) and deadline; appeals that re-argue without new substance fail. If won: send the buyer a graceful close-out (winning the case and losing the review is half a win). Either way, request review removal/revision only where the platform allows and the resolution genuinely addressed the issue.

### Step 7 — Log and prevent
Record: dispute type, SKU, carrier, buyer, outcome, cost. Monthly: rank root causes — a SKU with 3 INAD disputes has a listing-accuracy problem; a carrier lane with INR clusters needs signature confirmation; a buyer with 4 refunds needs a block-list entry. Deliver the response package using `references/output-template.md` and run `assets/dispute-response-checklist.md` before sending.

## Worked Example 1 — INR dispute with delivery confirmation

**Input:** "TikTok Shop buyer opened a refund claim: 'Package never arrived, I want my $67 back.' Tracking shows delivered June 3, 14:32, with GPS coordinates matching the address and a delivery photo of the package on a doormat. Buyer has 2 prior orders, no disputes. Claim deadline: 48h. The buyer also messaged: 'I was home all day, nobody came.'"

**Process:** Triage: INR, platform claim stage, moderate value, clean buyer history — could be genuine porch theft or carrier misdelivery, not obvious fraud. Evidence: delivery scan + GPS + photo = strong platform case. Strategy: fight the auto-refund with evidence BUT offer the buyer a constructive path — clean-history buyers with photo-confirmed delivery are usually theft victims, not fraudsters; pure "we won, tough luck" costs a 2-order customer and invites a chargeback. Platform response: facts numbered (1. carrier X tracking #, delivered June 3 14:32; 2. GPS matches shipping address; 3. delivery photo attached; 4. package weight at intake matches product), cite platform proof-of-delivery policy, request claim denial. Buyer message: empathize, share the delivery photo, suggest checking household members/neighbors/building office, offer to help file a carrier claim, and — judgment call by seller policy — a one-time 30% goodwill credit if nothing turns up.

**Output:** Platform evidence submission (4 numbered facts + 3 attachments + policy cite), buyer message with photo and search suggestions, recommendation: signature confirmation for this zip code going forward (second INR from the area in 60 days), and a log entry.

## Worked Example 2 — Return-condition dispute (used item returned)

**Input:** "Shopee buyer returned a $129 hair dryer after 12 days claiming 'defective, won't turn on'. The returned unit arrived with hair residue inside the filter, a scratched barrel, and a missing concentrator nozzle — it clearly works (we tested it on video) and was clearly used. Platform is asking if we accept the return for full refund. Buyer threatened a one-star review in chat: 'refund me or I leave you a review you'll regret.'"

**Process:** Triage: return-condition dispute + review extortion (separate violation!). Evidence: unboxing video of the return (timestamped), test video showing the unit powers on, photos of residue/scratch/missing nozzle, outbound QC photo showing pristine condition and included nozzle, chat screenshot of the review threat. Strategy: fight — evidence is strong, value meaningful, and the review threat is itself reportable; folding here trains repeat behavior. Platform response: dispute the full refund — request rejection or deduction per platform's used/incomplete-return policy, attach video stills + photos + QC record; separately report the chat message under review-extortion policy (most platforms void review leverage once reported). Buyer message: factual and calm — received unit shows use and a missing part, attach photos, state the deduction/rejection per policy, no reference to the threat (that conversation belongs to the platform report).

**Output:** Platform dispute submission + extortion report (two separate filings), buyer message, and prevention notes: add "tamper/usage indicators" QC step for high-return SKUs, and log the buyer ID. Flag: review-extortion reporting paths differ by platform — verify current procedure.

## Common Mistakes

1. **Writing the response in the emotional moment.** The first draft written angry costs more than the dispute. Triage → evidence → strategy → THEN write.
2. **Missing the deadline while perfecting the response.** A good-enough submission inside the SLA beats a perfect one outside it. Calendar the deadline at triage.
3. **One document for two audiences.** The platform reviewer needs numbered facts and policy; the buyer needs empathy and a path. Mixing them fails both.
4. **Asserting evidence you don't attach.** "Our tracking proves delivery" without the tracking detail/attachment reads as bluster to a reviewer processing hundreds of cases.
5. **Calling the buyer a liar.** Even in fraud cases, accuse the facts, not the person: "the returned item shows usage indicators" not "the buyer used it and is lying."
6. **Fighting everything or refunding everything.** Both lose money. The decision matrix exists because $12 disputes aren't worth your hour and $200 fraud isn't worth your silence.
7. **Ignoring buyer history.** A first-time claim from a 5-order customer and a third claim from a 3-order account deserve different default strategies.
8. **Folding to review extortion.** "Refund or bad review" is a platform violation in most marketplaces — report it; don't pay it. Paying it makes you a target.
9. **No dispute log.** Without type/SKU/carrier logging, you fight the same preventable dispute monthly. The log turns disputes into product and operations fixes.

## Resources

- `references/output-template.md` — dispute response package format (platform submission + buyer message + log entry)
- `references/resolution-decision-matrix.md` — fight/refund/partial/replace decision framework with the math
- `references/platform-rules.md` — evidence standards and dispute mechanics by platform type, chargebacks included
- `references/response-templates.md` — tone-calibrated message skeletons per dispute type
- `assets/dispute-response-checklist.md` — pre-send quality checklist
