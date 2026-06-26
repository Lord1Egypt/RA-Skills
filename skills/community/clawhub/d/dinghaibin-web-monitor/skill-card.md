## Description: <br>
Monitor web pages for content changes with CSS selector targeting, hash-based comparison, saved state, and notification integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check web pages or selected page elements for content changes, persist comparison state, and trigger notifications for price tracking, content alerts, and availability monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTPS certificate verification is disabled during page fetching. <br>
Mitigation: Avoid sensitive or security-critical monitoring unless TLS verification is fixed. <br>
Risk: The notification option can run user-supplied shell commands when a webpage changes. <br>
Mitigation: Do not use notification commands that modify files, expose secrets, or perform account actions. <br>
Risk: Saved state may include full page content from monitored pages. <br>
Mitigation: Prefer hash-only mode for private pages so full page content is not stored locally. <br>


## Reference(s): <br>
- [Web Monitor Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/dinghaibin-web-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON state files and optionally run notification commands through the bundled monitor script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
