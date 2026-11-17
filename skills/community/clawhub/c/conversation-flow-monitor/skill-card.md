## Description:

Monitors and prevents conversation flow issues by implementing robust error handling, timeouts, and recovery mechanisms for reliable agent interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edkuo7](https://clawhub.ai/user/edkuo7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add timeout handling, recovery patterns, health checks, and diagnostic logging to agent conversations that may otherwise stall during browser, file, network, or multi-step workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory promotion or workspace-document edits can change future agent behavior without enough scoping or user control.

Mitigation: Disable automatic memory promotion and AGENTS.md/SOUL.md/TOOLS.md edits unless each proposed change is inspected and approved.

Risk: Heartbeat log cleanup and diagnostic logging can remove audit history or retain sensitive conversation details.

Mitigation: Configure log retention and redaction before use, and require review before enabling automatic cleanup in sensitive workspaces.

Risk: Placeholder or unpinned installation commands can install code from an unverifiable source.

Mitigation: Install only from an immutable, verified release source and avoid placeholder npx or GitHub commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edkuo7/skills/conversation-flow-monitor)
- [README](artifact/README.md)
- [Usage Examples](artifact/examples.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or maintain local diagnostic logs when integrated with the provided monitoring scripts.]

## Skill Version(s):

1.0.1 (source: server release evidence, package.json, CHANGELOG, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
