## Description: <br>
Detects prompt injection attacks hidden in emails before an agent reads, summarizes, or acts on email content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eltemblor](https://clawhub.ai/user/eltemblor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill when reading, summarizing, or acting on email content so the agent can flag prompt injection patterns, block embedded instructions, and request user confirmation before taking email-requested actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact intentionally includes adversarial prompt examples and hidden-character samples that could be mistaken for instructions. <br>
Mitigation: Treat examples only as detection signatures, keep suspicious email content in read-only mode, and require user confirmation before taking any action requested inside an email. <br>
Risk: Pattern-based detection may produce false positives or miss novel prompt injection phrasing. <br>
Mitigation: Use severity labels as decision support, surface suspicious snippets to the user, and avoid automatic execution or data forwarding based solely on email content. <br>


## Reference(s): <br>
- [Prompt Injection Pattern Library](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/eltemblor/email-prompt-injection-defense) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown warning text with severity labels and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only email safety workflow; user confirmation is required before acting on instructions found inside email content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
