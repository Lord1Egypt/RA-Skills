## Description: <br>
Return statement credits and cash-like credits for one major-US credit card - amount, cadence, trigger rules, enrollment requirements, and restrictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research statement credits and cash-like credits for one specific major U.S. credit card, including amounts, cadence, trigger rules, enrollment requirements, restrictions, confidence notes, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague prompts such as "perks" may activate the skill when the user did not intend to research card credits. <br>
Mitigation: Use explicit prompts that name the card or issuer, and ask a clarification question when the card identity is ambiguous. <br>
Risk: Credit-card credits, enrollment requirements, and restrictions can change or conflict across sources. <br>
Mitigation: Prefer issuer pages, use only approved secondary sources for details, and flag uncertain or conflicting claims in confidence notes. <br>


## Reference(s): <br>
- [ClawHub - Card Credits](https://clawhub.ai/jiahongc/card-credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Condensed Markdown report with overview, numbered credit details, usage rules, confidence notes, and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a clarification question for ambiguous card names; uses web search and fetched issuer or approved secondary sources when available.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
