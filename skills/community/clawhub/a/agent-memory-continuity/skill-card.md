## Description:

Solve the "agent forgot everything" problem with search-first protocol, automated memory sync, and context preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a search-first memory protocol, daily memory logging, and recurring local sync scripts for multi-session conversation continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores conversation history in local plaintext memory files, which may expose sensitive secrets or personal data if used in an inappropriate workspace.

Mitigation: Use it only where persistent plaintext memory is acceptable, avoid entering secrets or sensitive personal data, and review generated memory files regularly.

Risk: The activation script may create recurring local execution through cron.

Mitigation: Review the cron entry before and after activation, run it only in a trusted workspace path, and remove the cron entry when the skill is no longer used.

Risk: The security evidence reports weak scoping and a cron command-injection risk.

Mitigation: Do not run activation scripts with untrusted or unusual workspace paths, and inspect shell commands before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/highlander89/skills/agent-memory-continuity)
- [SAPCONET Homepage](https://sapconet.co.za)
- [Memory Continuity Documentation](https://docs.sapconet.co.za/memory-continuity)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Agent Memory Protocol Template](templates/AGENT_MEMORY_PROTOCOL.md)
- [Memory Configuration](config/memory-config.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, configuration files, and reusable memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local memory files, configuration files, and optional recurring sync entries in the target workspace.]

## Skill Version(s):

1.0.0 (source: release evidence, metadata.clawhub.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
