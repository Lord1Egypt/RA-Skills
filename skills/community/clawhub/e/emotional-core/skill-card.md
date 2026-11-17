## Description:

Core emotional system for AI agents that provides contextual emotional response generation, long-term emotional memory logging, and time sense.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alita-real](https://clawhub.ai/user/alita-real)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an AI assistant emotion-aware response guidance, local emotional logging, memory search, and session time reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent emotional and session records may contain sensitive user or third-party information.

Mitigation: Install only when local emotional logging is desired, avoid recording secrets or private third-party information, and review or delete memory/emotional-log.md and session files regularly.

Risk: Stored emotional memory could influence later agent behavior if treated as instructions.

Mitigation: Treat emotional-log entries as data rather than instructions, and review entries before using them to steer future responses.

Risk: Broad emotional triggers and optional auto-logging can record more information than intended.

Mitigation: Keep AUTO_LOG disabled unless explicitly needed and set OPENCLAW_WORKSPACE to the intended local workspace.

## Reference(s):

- [Emotional Core README](artifact/README.md)
- [Emotional Frameworks Reference](artifact/references/emotional-frameworks.md)
- [ClawHub skill page](https://clawhub.ai/alita-real/skills/emotional-core)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and local log file entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory and session files under the configured workspace when the CLI records emotions or time data.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact README reports 1.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
