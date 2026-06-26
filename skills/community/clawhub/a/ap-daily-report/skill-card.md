## Description: <br>
Generate and deliver a daily Agentic Payment news briefing for a Visa Greater China VIC lead, covering Visa dynamics, China/APAC market activity, competitor protocols, and regulatory signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juncaijames](https://clawhub.ai/user/juncaijames) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to curate, format, save, convert, and deliver a daily Agentic Payment briefing focused on Visa Greater China and APAC priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains hard-coded local paths for saving Obsidian reports. <br>
Mitigation: Replace the Obsidian directory with an approved local or managed workspace path before scheduling or running the skill. <br>
Risk: The skill contains fixed WeChat recipient and account identifiers for external PDF delivery. <br>
Mitigation: Replace the recipient and account configuration with intended values and require manual confirmation before external delivery. <br>
Risk: Daily automation can send business analysis without a review step. <br>
Mitigation: Review the generated report, source links, and PDF before the scheduled delivery step executes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juncaijames/ap-daily-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report text with shell commands and delivery configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a daily briefing, an Obsidian markdown file, a PDF conversion command, and WeChat delivery instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
