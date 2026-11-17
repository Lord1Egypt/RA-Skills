## Description: <br>
Identifies high-ROI business processes and designs automation workflows, including process audits, scoring, scheduled task setup, and basic monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, operations, finance, and HR employees use this skill to map repetitive workflows, prioritize automation opportunities by ROI, and draft workflow or cron configurations for agent-assisted implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward persistent scheduled jobs. <br>
Mitigation: Require explicit confirmation before creating or changing cron jobs, run dry-runs first, and keep a human approval step for production schedules. <br>
Risk: The skill can guide agents toward external integrations such as API calls, email, messaging, or database writes. <br>
Mitigation: Require explicit confirmation before API calls, email read/send actions, external messages, or database writes, and verify credentials are stored outside the skill content. <br>
Risk: The skill includes payment, HR, account, and customer-impacting automation scenarios. <br>
Mitigation: Keep human approval for financial, HR, account, and customer-impacting actions, especially before payment-related steps or customer-visible changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bizauto-flow-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, text, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include process maps, ROI scoring, workflow YAML, cron entries, and monitoring metric summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, target metadata, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
