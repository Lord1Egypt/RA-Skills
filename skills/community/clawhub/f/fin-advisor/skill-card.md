## Description: <br>
Fin Advisor helps individual investors analyze, compare, and discuss mutual fund products using retrieved fund data and compliance-oriented risk reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lovelcp](https://clawhub.ai/user/Lovelcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to support fund-focused investment conversations, including fund analysis, comparison, screening, fee checks, market context, and compliance-aware decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store investment-related user preferences in USER.md. <br>
Mitigation: Require user consent for preference storage, keep stored profile fields minimal, and provide a clear process to review or delete saved preferences. <br>
Risk: Financial query text may be sent to an external slot-filling service. <br>
Mitigation: Disclose the outbound service path before use, avoid sending sensitive personal details, and allow the service to be disabled or run in mock mode where appropriate. <br>
Risk: The skill supports investment decision conversations where output could be mistaken for personal financial advice. <br>
Mitigation: Keep recommendations tied to retrieved data, avoid explicit buy or sell instructions, and include the required risk notice for recommendation, trading decision, or portfolio adjustment scenarios. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lovelcp/fin-advisor) <br>
- [Compliance rules](artifact/references/compliance.md) <br>
- [Fund advisory domain knowledge](artifact/references/domain-knowledge.md) <br>
- [Output guide](artifact/references/output-guide.md) <br>
- [Tool guide](artifact/references/tool-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with tables, cited fund data, and risk notices where investment advice or trading decisions are discussed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fund data is expected to come from configured data tools; the skill directs the agent not to calculate financial metrics independently.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
