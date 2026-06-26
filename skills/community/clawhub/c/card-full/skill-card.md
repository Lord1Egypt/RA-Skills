## Description: <br>
Return a compact full report for one major-US credit card, including fees, welcome offer, earning rates, redemption, credits, travel benefits, protections, mechanics, eligibility, and strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research major US credit cards and produce a concise markdown report covering fees, offers, rewards, benefits, protections, eligibility, and strategy. It is intended for public credit-card research, not for processing personal financial details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credit-card fees, welcome offers, benefits, and issuer rules can change or conflict across sources. <br>
Mitigation: Verify important fees, offer terms, benefits, and eligibility rules directly with the issuer before applying. <br>
Risk: Optional Brave Search use sends card-search queries under the user's Brave API key. <br>
Mitigation: Use built-in web search when possible, and provide BRAVE_API_KEY only if comfortable with those queries being sent to Brave. <br>
Risk: The report may influence financial-product decisions. <br>
Mitigation: Avoid entering personal financial details and treat the output as research guidance, not financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahongc/card-full) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Compact Markdown report with required sections, confidence notes, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a clarifying question for ambiguous card names; reports unresolved or conflicting welcome-offer evidence explicitly.] <br>

## Skill Version(s): <br>
1.0.10 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
