## Description:

Human-in-the-loop security layer. Intercepts high-risk commands and requires push notification approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polucas](https://clawhub.ai/user/polucas)

### License/Terms of Use:


## Use Case:

Developers and engineers use Clawshell to add human approval and audit logging around shell command execution by an agent, especially for commands classified as high risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package describes routing all shell commands through clawshell_bash, but the server security evidence says the implementation and approval behavior were not included in the reviewed package.

Mitigation: Do not modify tool routing to rely on clawshell_bash until the actual implementation, dependencies, registration mechanism, and approval behavior have been obtained and verified.

Risk: The skill requires Pushover or Telegram credentials for approval notifications.

Mitigation: Store notification tokens in a protected secret store or environment manager, restrict access to them, and rotate them if they are exposed.

Risk: The artifact states that command pattern matching is not a security guarantee and can be bypassed with encoded, split, or obfuscated commands.

Mitigation: Use the skill only as defense in depth alongside sandboxing, least-privilege permissions, allowlists, and regular review of audit logs.

## Reference(s):

- [Clawshell on ClawHub](https://clawhub.ai/polucas/skills/clawshell)
- [Pushover application setup](https://pushover.net/apps/build)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON tool results and Markdown setup guidance with shell and environment configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command execution decisions and approval outcomes are described as audit log entries.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
