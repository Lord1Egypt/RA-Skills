## Description:

Claude Code Evolution guides experienced OpenClaw administrators through a five-stage upgrade covering structured memory, tool permissions, coordinator-worker collaboration, security hardening, and prompt optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yudch999-bot](https://clawhub.ai/user/yudch999-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and experienced OpenClaw administrators use this skill to plan and apply an architecture upgrade that adds structured memory, permission modeling, coordinator-worker protocols, security tooling, and prompt optimization. The skill is best handled as an administrative change workflow because it includes scripts that can affect credentials, configuration, and agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact administrative workflows include credential migration, permission sandboxing, and prompt optimization tools that should not be treated as production security controls without review.

Mitigation: Install only in a test OpenClaw workspace first and fix the approval gate, credential storage, redaction, and missing sandbox or configuration resources before production use.

Risk: Credential migration can affect sensitive configuration if run without preparation.

Mitigation: Use an explicit strong password, run a dry-run or test workflow first, and back up configuration before migration.

Risk: Permission and prompt changes can alter agent behavior and operational policy.

Mitigation: Review proposed configuration changes, validate memory and permission behavior, and benchmark prompt changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yudch999-bot/skills/claude-code-evolution)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Agent role definitions](references/agent-role-definitions.md)
- [Coordinator-worker protocol](references/coordinator-worker-protocol-v1.md)
- [Coordinator-worker test scenarios](references/coordinator-worker-test-scenarios.md)
- [Memory index template](references/memory-index-template.md)
- [Tool classification configuration](references/tools-classification-config.yaml)
- [Reference pointers memory template](references/memory-templates/reference-pointers.md)
- [User profile memory template](references/memory-templates/user-profile.md)
- [Feedback logs memory template](references/memory-templates/feedback-logs.md)
- [Project states memory template](references/memory-templates/project-states.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python scripts, YAML configuration, memory templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes administrative scripts and reference templates for OpenClaw memory, permissions, credential handling, sandboxing, coordinator-worker workflows, testing, benchmarking, and prompt optimization.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
