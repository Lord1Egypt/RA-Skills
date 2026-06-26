## Description: <br>
Evaluate a franchise opportunity like an investor by analyzing Franchise Disclosure Document inputs for investment cost, fees, Item 19 performance, unit growth and closures, payback, cash-on-cash return, and red flags before producing a structured buy, hold, or pass assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dotcomcj2](https://clawhub.ai/user/dotcomcj2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, franchise evaluators, and agents use this skill to screen franchise opportunities, summarize FDDs, compare brands as investments, and identify financial or disclosure risks. It supports educational due diligence and should not replace legal, accounting, or investment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill output could be mistaken for financial or legal advice. <br>
Mitigation: Use it as an educational screening tool and have the FDD and franchise agreement reviewed by a qualified franchise attorney and accountant before relying on the output. <br>
Risk: Incorrect or outdated FDD source data can produce misleading investment metrics. <br>
Mitigation: Verify the FDD year and source before analysis and confirm assumptions such as revenue, EBITDA margin, royalties, and ad fees. <br>
Risk: Incomplete FDD inputs can make payback, cash-on-cash return, or closure analysis unreliable. <br>
Mitigation: Treat missing Item 7, Item 19, or Item 20 values as explicit limitations and avoid filling gaps with invented numbers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dotcomcj2/franchise-analyzer-skill) <br>
- [Franchise Fast Track](https://franchisefasttrack.io) <br>
- [Franchise Fast Track FDD database](https://franchisefasttrack.io/fdd-database) <br>
- [Franchise Fast Track franchise directory](https://franchisefasttrack.io/franchise-directory) <br>
- [FDD Item cheat sheet](reference/fdd-items.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown franchise analysis report with optional local calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports missing FDD inputs instead of inventing figures; calculator output is deterministic for supplied numeric inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
