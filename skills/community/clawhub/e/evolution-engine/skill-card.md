## Description:

进化引擎 helps AI agents record corrections, reflect on completed work, maintain layered local memory, and reuse confirmed lessons with anti-pollution safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide an AI agent in recording user corrections, promoting confirmed patterns into local memory, and tracking evolution metrics for repeated workflows. It is not suitable for critical decisions that require deterministic certainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests or advertises command and network-related capabilities that exceed its described local-memory purpose.

Mitigation: Install with command execution and network/API access disabled or restricted unless the publisher provides a clear operational need.

Risk: The skill writes persistent memory records under ~/evolution-engine/, which can retain sensitive, stale, or unintended user information.

Mitigation: Review stored memory files regularly, avoid storing credentials or sensitive personal data, and delete or archive records only with explicit user intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/evolution-engine)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown guidance with local file paths and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files under ~/evolution-engine/ when the agent follows the skill.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
