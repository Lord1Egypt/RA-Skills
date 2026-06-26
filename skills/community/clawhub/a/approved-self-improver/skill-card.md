## Description: <br>
Captures learnings, errors, corrections, feature requests, and pending improvement proposals so compatible coding agents can improve workflows with user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to capture errors, corrections, feature requests, and reusable learnings in local `.learnings` files. They can then review, promote, or apply user-approved skill improvements across OpenClaw and compatible agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can retain sensitive or private session details. <br>
Mitigation: Do not store secrets, environment values, private keys, raw transcripts, or full command output; use short redacted summaries. <br>
Risk: Optional hooks can influence future sessions by injecting reminders automatically. <br>
Mitigation: Keep hooks disabled or project-scoped until the scripts are reviewed and the workspace owner has opted in. <br>
Risk: Promoting learnings or sharing cross-session context can spread incorrect or private information. <br>
Mitigation: Require explicit confirmation before promotion, transcript reading, session messaging, sub-agent spawning, or new skill creation, and share only sanitized summaries. <br>
Risk: Self-improvement proposals can change skill behavior if applied without review. <br>
Mitigation: Apply skill changes only after user approval unless that exact skill has a recorded auto-update authorization. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/encryptshawn/approved-self-improver) <br>
- [Entry Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and optional code hooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local `.learnings` Markdown files and may provide improvement proposals; optional hooks inject reminders when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
