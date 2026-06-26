## Description: <br>
Buffett-style Research Prioritization Assistant - decide whether a company deserves deeper research, what to check first, and get a copy-paste research prompt for your agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to decide whether a public company or ticker deserves deeper fundamental research and to generate a compact follow-up research prompt. It is a triage aid, not financial advice or a buy, sell, or hold recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be mistaken for financial advice or used as a complete investment decision. <br>
Mitigation: Treat outputs as research triage only and verify business quality, moat, risk, cash-flow quality, and valuation independently before acting. <br>
Risk: Broad activation phrases may trigger on generic investment questions. <br>
Mitigation: Use the skill only when the user is asking for Buffett-style company research prioritization, and clarify intent when a generic investment question could trigger it. <br>
Risk: Users could overshare sensitive financial details even though the skill does not request them. <br>
Mitigation: Avoid sharing brokerage logins, wallet keys, API keys, private portfolio files, or other sensitive financial details. <br>


## Reference(s): <br>
- [What Buffett Would Do on ClawHub](https://clawhub.ai/choosenobody/buffett-do) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a research-priority label, three verification checks, and a copy-paste research prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps outputs short and action-oriented; does not request API keys, wallet keys, brokerage logins, private files, or personal portfolio details.] <br>

## Skill Version(s): <br>
1.1.10 (source: server release evidence; artifact frontmatter lists 1.1.8 and artifact _meta.json lists 1.1.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
