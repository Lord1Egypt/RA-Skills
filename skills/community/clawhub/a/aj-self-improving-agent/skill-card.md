## Description: <br>
Captures learnings, errors, and corrections in markdown logs so coding agents can improve future workflows and promote recurring lessons to project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceundefeated](https://clawhub.ai/user/aceundefeated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record corrections, command failures, missing capabilities, and recurring best practices as structured markdown entries. It also provides optional reminders and hook setup guidance for promoting useful lessons into durable agent context files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs and promoted prompt files can capture sensitive project details, secrets, customer data, command output, or private transcript context. <br>
Mitigation: Redact secrets, tokens, customer data, full command output, and private transcript details before saving entries or promoting them into durable agent context. <br>
Risk: Incorrect or misleading learning entries can be promoted into future agent guidance. <br>
Mitigation: Review proposed entries and scan changes before promotion into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions. <br>
Risk: Optional hooks can inject reminders or inspect command output during agent workflows. <br>
Mitigation: Enable hooks only after reviewing their configured paths and script contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aceundefeated/aj-self-improving-agent) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Learning Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries intended for local .learnings files and optional promotion into agent context files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
