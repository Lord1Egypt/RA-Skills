# Cargo Claim Drafter (Carmack Amendment)

**Platforms:** Claude · Openclaw · Codex
**Domain:** Logistics / Freight Claims

## Purpose

Drafts a U.S. interstate cargo loss, damage, or shortage claim against a motor or rail carrier under the Carmack Amendment (49 U.S.C. § 14706 for motor carriers, § 11706 for rail carriers, 49 C.F.R. Part 370 for filing procedure). Walks shipment intake, exception classification, evidence capture, claim-amount computation (uncapped and released-value-capped), and produces a DRAFT claim letter that satisfies the four 49 C.F.R. § 370.3(b) minimum filing requirements, an evidence index, and a deadline tracker showing the minimum nine-month filing window and the minimum two-year-and-one-day post-disallowance suit window. The output supports — never replaces — claims-team and counsel review before submission.

## When to Use

- A consignee or shipper has identified loss, damage, shortage, non-delivery, spoilage, or contamination on an interstate freight movement
- A 3PL, broker, or freight forwarder operations team needs to draft a Carmack claim on a customer's behalf
- A traffic / logistics manager is preparing the first written notice of claim within the minimum nine-month filing window
- A claims team is converting a concealed-damage discovery into a formal Carmack claim within the carrier's tariff inspection window
- A claimant has received a written disallowance and needs to capture the suit-window deadline before referring to counsel
- A standardised internal claim packet is being assembled for repeated submission against a specific carrier

## What It Does

**Phase 1: Shipment Intake**
1. Confirms jurisdiction (interstate vs. intrastate), carrier type (motor § 14706 / rail § 11706 / intermodal), and that the proposed defendant is actually a Carmack carrier (not a broker)
2. Captures shipper, consignee, claimant, originating / connecting / delivering carriers, BOL number and type, pickup / scheduled / actual delivery dates, commodity (with NMFC item / class), pieces / weight / cube, declared or released value, pro number, and any special service
3. Documents tender in good condition — the first Carmack prima facie element — with clean BOL, origin inspection / pulp / serial records, packaging compliance, and seal numbers

**Phase 2: Exception and Evidence Capture**
4. Classifies the exception (visible damage, concealed damage, shortage, non-delivery, loss in transit, temperature / spoilage, contamination) and walks an exception-specific evidence checklist
5. Captures mitigation and salvage values, plus any insurance subrogation context, so damages are computed net of recoveries without double-counting

**Phase 3: Claim Amount Computation**
6. Walks the actual-loss measure — invoice cost + recoverable freight + reasonable foreseeable damages – salvage – mitigation recoveries — and produces a visible computation worksheet
7. Applies any released-value or limited-liability cap under 49 U.S.C. § 14706(c), computing both uncapped and capped amounts and leaving the choice to counsel
8. Flags consequential / special / lost-profit damages for counsel review under the "contemplation of the parties" doctrine

**Phase 4: Carmack-Compliant Claim Letter**
9. Drafts a written claim that explicitly carries all four 49 C.F.R. § 370.3(b) elements — written communication, sufficient identification of the shipment, assertion of carrier liability, and demand for a specified or determinable sum — addressed to the carrier's claims department per its tariff / BOL
10. Cites Part 370 acknowledgement (30-day) and disposition (120-day) timelines, preserves the two-year-and-one-day suit window from any written disallowance, and labels the draft for claims-team and counsel review

**Phase 5: Evidence Index and Deadline Tracker**
11. Produces a numbered evidence index so every assertion in the claim letter is anchored to a specific document, date, and custody trail
12. Produces a deadline tracker covering the statutory nine-month filing minimum, 30-day acknowledgement, 120-day disposition, two-year-and-one-day suit window, and any tariff-specific concealed-damage notice window — flagging any carrier attempt to shorten statutory minimums

## Output

A claim packet consisting of a DRAFT Carmack-compliant claim letter (with each 49 C.F.R. § 370.3(b) element marked), a numbered evidence index, an itemised claim-amount computation showing both uncapped and capped figures, a deadline tracker covering the statutory and tariff-specific windows, and an Open Questions list for any unresolved input.

## Notes

This skill **drafts** a Carmack cargo claim to support — never replace — claims-team and counsel review. The skill does not opine on litigation outcome, does not opine on whether a particular released-value or shortened-statute clause is enforceable, does not draft release or settlement language, and does not file the claim with the carrier. The skill applies the Carmack Amendment by default and flags purely intrastate shipments (state common-carrier law governs) and ocean / international moves (Carmack does not apply; Hague-Visby, COGSA, or Montreal regimes govern). The skill refuses to assert facts the evidence index does not support: assertions without supporting evidence are marked OPEN. The skill never signs the claim and never opines on litigation strategy.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
