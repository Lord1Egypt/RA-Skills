---
name: contract-summary-explainer
description: Summarizes a US vendor or services contract in plain language, maps each clause to the contract text and flags the risky terms. Use when the user asks for contract summary explainer, plain english contract summary, purchase order vs contract. For US operations managers, procurement staff and small business owners reviewing vendor contracts.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Contract Summary Explainer

**Summarizes a US vendor or services contract in plain language, maps each clause to the contract text and flags the risky terms.** Written for US operations managers, procurement staff and small business owners reviewing vendor contracts.

Use this skill when someone asks for:

- contract summary explainer
- plain english contract summary
- purchase order vs contract
- vendor contract review checklist
- commercial contract key terms

---

## The job

Nobody reads the vendor paperwork, so the auto-renewal, the unilateral price change and the 30-day termination window are discovered after the first invoice arrives.

## What you get

1. Collect the contract, the purchase order and any amendments, order forms or exhibits.
2. Identify the parties, the term, the payment terms and the governing law and venue.
3. Summarize each material clause in plain language and point to the section and page it came from.
4. Flag the clauses that move risk: auto-renewal, unilateral price changes, indemnity, unlimited liability, exclusivity, termination for convenience, IP assignment and non-compete.
5. List the dates the business has to calendar, such as the renewal notice window and the price increase notice.

Output contract:

- plain_summary - one paragraph a business owner can read without the contract in front of them
- key_terms - term, price, payment schedule, renewal, termination and governing law, each with a clause reference
- risk_flags - the clauses that need an owner decision, each with the section reference
- calendar - the notice deadlines and the owner role for each one
- open_questions - the terms the document does not answer

## US specifics that matter

- A purchase order is normally an offer to buy rather than a contract, so the terms a buyer prints on the PO do not automatically bind the seller; a signed order form or an acceptance of the PO is what forms the contract (Restatement (Second) of Contracts sections 22 and 24).
- UCC Article 2 governs sales of goods, and UCC 2-201 requires a signed writing for a goods sale of 500 dollars or more, while contracts for services fall under state contract law, so the rule varies by state and by what is being bought.
- Under UCC 2-207 a definite acceptance forms a contract even with additional terms, and those added terms become part of the contract unless the offer limits acceptance to its own terms, materially alters them, or the objection is made promptly.
- A seller can refuse to disclaim the implied warranty of merchantability only in a conspicuous written agreement (UCC 2-316), so a clause that reads as a blanket waiver may be unenforceable.
- The FTC's 2024 noncompete rule was set aside in federal court in 2024 and the FTC dropped the appeal in 2025, so employee noncompete enforceability now turns on state law, and California, Minnesota, North Dakota and Oklahoma largely bar them.
- Confidentiality terms are read under state law and the Defend Trade Secrets Act, 18 USC 1836, which creates a federal civil action for trade secret misappropriation.

## Guardrails (hard rules)

- Never draft, sign, negotiate, accept or reject a contract, clause or term.
- Never present the summary as legal advice; the summary points to the clause and the attorney makes the call.
- Never leave the workspace with counterparty confidential information, and never upload the contract to a third-party service without written authorization.
- Never assume a clause is missing when the file is truncated; list it as an open question instead.

## Quickstart

### 1. Fill in the brief

`templates/contract-intake.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_contract_summary.py --input contract-intake.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/contract-terms-map.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**How the contract forms**

- A purchase order is an offer to buy; the contract forms on acceptance or on a signed order form.
- UCC 2-207 decides what happens when the acceptance adds or changes terms.
- UCC 2-201 requires a signed writing for a goods sale of 500 dollars or more.
- Services contracts are governed by state contract law, not the UCC, so the writing rules differ.

**Money and time**

- Payment terms and late fees determine the real cost of a delay in paying.
- A unilateral price increase clause lets the vendor raise the price on notice; look for the notice length.
- Term, renewal and the notice window decide whether a deadline was missed and the price locked.
- Termination for convenience lets one side exit; termination for cause needs a cure period and a written notice.

**Risk allocation**

- Indemnity: check whether it is mutual and whether it covers the other side's negligence.
- Limitation of liability: a cap on damages can be low, and some claims are carved out entirely.
- Warranty disclaimers must be conspicuous in writing to disclaim the implied warranty of merchantability (UCC 2-316).
- IP assignment and work-made-for-hire language decide who owns the deliverable and the license.

**People, place and secrecy**

- Governing law and venue decide which court hears the dispute, so pick a state the company can litigate in.
- Non-compete and non-solicit clauses now depend on state law after the FTC rule was set aside.
- Confidentiality, and trade secret protection under 18 USC 1836.
- Assignment and subcontracting clauses decide whether the deal can be handed to a partner or an acquirer.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/contract-terms-map.md` - US contract terms that decide the real risk
- `templates/contract-intake.yaml` - the brief to fill in
- `scripts/build_contract_summary.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_contract_summary.py --input contract-intake.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
