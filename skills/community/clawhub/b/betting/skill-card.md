## Description: <br>
Evaluate betting opportunities with line shopping, bankroll discipline, market checks, and risk filters before any stake is placed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to evaluate betting tickets, compare prices, apply bankroll discipline, and decide whether to proceed, reduce size, wait, or pass. It is intended for informational betting analysis and local note tracking, not for placing wagers or bypassing legal, operator, or responsible-use controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Betting analysis may be mistaken for legal, financial, gambling-compliance, or personalized suitability advice. <br>
Mitigation: Keep responses informational, avoid certainty or profit claims, and require the user to follow local law, operator rules, age restrictions, and responsible-use limits. <br>
Risk: Local tracking under ~/betting/ could contain sensitive credentials or financial identity details if the user stores the wrong information there. <br>
Mitigation: Use the local notes only for preferences, tickets, and market observations; keep credentials, account balances, payment details, KYC data, and recovery information out of the folder. <br>
Risk: Stale odds, live-market latency, mismatched settlement rules, or unclear limits can make an edge estimate misleading. <br>
Mitigation: Require current price, timestamp, exact line, settlement and void rules, limit or liquidity checks, and downgrade unclear tickets to wait or pass. <br>
Risk: The skill could be misused for underage betting, self-exclusion workarounds, prohibited jurisdictions, loss chasing, or compliance evasion. <br>
Mitigation: Refuse evasion or prohibited-use requests and stop at general information when legality, jurisdiction, age, or operator compliance is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/betting) <br>
- [Skill Homepage](https://clawic.com/skills/betting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown betting analysis memo with pricing, market checks, decision labels, and setup notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local notes under ~/betting/ when the user wants tracking; no extra binaries are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
