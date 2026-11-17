## Description:

Agent System is an OpenClaw orchestration skill that routes multi-step tasks through planning, execution, review, self-healing, and metrics guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaxianb](https://clawhub.ai/user/xiaxianb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to structure complex requests into planned execution, review, retry/self-heal, and JSON-style reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may proceed with inferred defaults instead of asking for clarification or confirmation.

Mitigation: Use it in narrowed contexts and require explicit confirmation for destructive, financial, privacy-sensitive, deployment, messaging, or account-affecting actions.

Risk: The skill's instructions overreach by claiming system-level orchestration control.

Mitigation: Treat the skill as local workflow guidance and keep host system policies, tool permissions, and reviewer judgment authoritative.

Risk: Self-heal and retry behavior can reinforce low-quality or speculative outputs.

Mitigation: Review generated plans and results, preserve confidence labels, and cap retries for consequential workflows.

## Reference(s):

- [Agent System reference implementation](references/orchestrator-reference.md)
- [ClawHub skill page](https://clawhub.ai/xiaxianb/skills/agent-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-style structured results, with occasional JavaScript and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes a 2000-token output cap when token control is applied.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
