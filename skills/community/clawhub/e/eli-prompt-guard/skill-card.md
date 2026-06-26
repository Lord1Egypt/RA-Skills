## Description: <br>
Automatically detects and blocks prompt injection attempts across multiple platforms to protect against unauthorized commands and data leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danlct27](https://clawhub.ai/user/danlct27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check outbound automated posts, form submissions, API calls, and shared file writes before content leaves the agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound automated submissions may still contain prompt-injection, credential, or PII content that detection patterns miss. <br>
Mitigation: Use the guard as a pre-submit check, keep detection patterns current, redact sensitive data in alerts, and require owner review for high-severity findings. <br>
Risk: The skill can pause or reject legitimate submissions when content matches detection patterns. <br>
Mitigation: Scope enabled platforms to active workflows and let the owner approve, reject, or review flagged content before submission. <br>
Risk: Review and logging workflows may expose submitted content if configured too broadly. <br>
Mitigation: Confirm full-content review is acceptable for the data being handled, log only the necessary submissions, and sanitize notification previews. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danlct27/eli-prompt-guard) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes owner review prompts, severity labels, sanitized previews, and approve/reject/review decision paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
