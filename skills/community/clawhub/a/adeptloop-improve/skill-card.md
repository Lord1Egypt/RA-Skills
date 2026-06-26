## Description: <br>
Daily improvement briefings with one-click fixes for your AI agent. Observes traces, diagnoses failures, and applies fixes conversationally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pedrocarballo](https://clawhub.ai/user/pedrocarballo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure AdeptLoop tracing, receive daily performance briefings, inspect failures, and apply or revert suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables ongoing third-party telemetry for agent diagnostics. <br>
Mitigation: Confirm what diagnostics-otel sends, how to disable collection, and whether the data handling fits the deployment before installation. <br>
Risk: The skill stores an AdeptLoop API key in local configuration files. <br>
Mitigation: Keep openclaw.json and ~/.openclaw/.env out of version control and rotate the key if it is exposed. <br>
Risk: Suggested fixes and rollback actions can modify project files and git branches. <br>
Mitigation: Inspect each proposed diff before applying or reverting changes. <br>


## Reference(s): <br>
- [AdeptLoop Improve on ClawHub](https://clawhub.ai/pedrocarballo/adeptloop-improve) <br>
- [AdeptLoop](https://adeptloop.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily briefings are intended to stay under 500 tokens and present one fix recommendation at a time.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
