## Description:

TinkerClaw Agent Superpowers gives OpenClaw agents disciplined engineering workflows for planning, verification, multi-agent code review, systematic debugging, and anti-over-engineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to add disciplined coding workflows, including upfront planning, fresh verification evidence, systematic debugging, and separate spec and quality reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can make coding sessions more process-heavy by encouraging planning, sub-agent review, commits, and fresh verification.

Mitigation: Apply the full workflow to non-trivial coding work and scale the review depth to the task size.

Risk: Copying the AGENTS.md guidance makes the behavior persist across future sessions.

Mitigation: Review the persistent rules before copying them and install them only when the team wants this operating style.

Risk: Instruction-only skills can still change agent behavior in ways that affect development workflow.

Mitigation: Review the skill text and security summary before deployment, then verify outputs with fresh commands before accepting completion claims.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/globalcaos/skills/agent-superpowers)
- [Systematic Debugging Extended Guide](references/debugging-guide.md)
- [Implementer Sub-Agent Prompt Template](references/implementer-prompt.md)
- [Plan Template](references/plan-template.md)
- [Code Quality Reviewer Prompt Template](references/quality-reviewer-prompt.md)
- [Spec Compliance Reviewer Prompt Template](references/spec-reviewer-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with prompt templates and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; no scripts, network calls, or credential access are included in the artifact.]

## Skill Version(s):

1.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
