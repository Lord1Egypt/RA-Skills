## Description:

Feishu Auto Reply helps agents configure and test rule-based replies for Feishu messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[night556](https://clawhub.ai/user/night556)

### License/Terms of Use:

MIT

## Use Case:

External developers and workspace administrators use this skill to generate and test rule-based Feishu auto-reply configurations for common questions, working-hours responses, and @mention-limited replies. Treat this release as local rule-testing and configuration assistance unless a separate Feishu message-handling integration is verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may grant Feishu message, chat, or user permissions even though the reviewed code does not implement Feishu message handling or sending replies.

Mitigation: Verify a working Feishu integration before granting permissions; treat this release as a local config generator and rule tester.

Risk: Overbroad keyword or regular-expression rules could produce unintended replies if connected to a live workspace.

Mitigation: Test rules in a non-production chat, constrain matching patterns, and add rate limiting before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/night556/skills/feishu-auto-reply)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu permission notes and warnings about unimplemented message handling.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
