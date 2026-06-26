## Description: <br>
Use when helping a user choose consumer electronics products through source-aware market research, comparison, and recommendation. MVP focuses on Bluetooth earbuds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fina1ee](https://clawhub.ai/user/fina1ee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare Bluetooth earbuds in a specific market, budget, currency, and use case, then produce source-aware recommendations with tradeoffs, links, and confidence notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported reports may save the user's region, budget, preferences, shortlist, and links to a local Markdown file. <br>
Mitigation: Check the destination path before saving or sharing reports, especially in shared or persistent environments. <br>
Risk: Prices, availability, and seller legitimacy can change after the report is generated. <br>
Mitigation: Verify current prices, availability, store reputation, warranty terms, and seller legitimacy before buying. <br>
Risk: A recommendation or product link could be mistaken for approval to purchase. <br>
Mitigation: Treat the skill as an advisor only; it does not authorize checkout or replace the user's final buying decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fina1ee/digital-product-advisor) <br>
- [Bluetooth Earbuds Buying Logic](references/bluetooth-earbuds.md) <br>
- [Parameter Model](references/parameters.md) <br>
- [Scoring Framework](references/scoring-framework.md) <br>
- [Markdown Export Policy](references/export-policy.md) <br>
- [Source Quality Guide](references/source-quality.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown reports, shortlist tables, recommendation prose, and optional saved .md report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product links, source notes, weighted scores, assumptions, tradeoffs, and confidence level.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
