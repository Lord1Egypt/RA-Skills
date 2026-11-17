## Description: <br>
Code Analyze helps teams perform structured multi-domain analysis of code, architecture, data, text, decisions, and visualizations, including batch reviews, cross-perspective validation, custom frameworks, and trend tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and engineering teams use this skill to review codebases and architecture decisions, generate prioritized analysis reports, and track quality or risk trends over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive code or analysis findings may be retained in local reports and history. <br>
Mitigation: Use the skill only on code you are allowed to analyze and review the .code-analyze reports and history before sharing or committing them. <br>
Risk: Optional external LLM endpoints, webhooks, or email notifications may send code or findings outside the local environment. <br>
Mitigation: Disable external endpoints and notification channels unless they are explicitly approved for the project data. <br>
Risk: The release evidence reports conflicting privacy guidance around local-only storage versus optional external integrations. <br>
Mitigation: Confirm the configured data flow before installation and treat external integrations as opt-in only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analyze) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration snippets, and structured analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or refer to local .code-analyze reports, framework definitions, history files, and optional notification settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
