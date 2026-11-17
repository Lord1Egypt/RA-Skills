## Description:

Guides developers building Claude API or Anthropic SDK features, including structured outputs, tool calling, streaming, multi-provider routing, multi-agent orchestration, evaluation, memory, RAG pipelines, and production deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmy974](https://clawhub.ai/user/jimmy974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and implement AI-powered application features with Claude and Anthropic SDK patterns across Python, TypeScript, and Next.js systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example agent patterns can access local files or sensitive user context without sufficient boundaries.

Mitigation: Add workspace-bound file access, explicit user approval for sensitive reads, and redaction before external model calls.

Risk: Conversation history and stored memory can leak across users or persist longer than intended.

Mitigation: Use per-user or per-tenant memory isolation with explicit retention and deletion controls.

Risk: RAG content can carry prompt-injection instructions into agent workflows.

Mitigation: Apply prompt-injection defenses around retrieved content and review generated actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmy974/skills/ai-integration)
- [Publisher profile](https://clawhub.ai/user/jimmy974)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation patterns and example snippets; examples require review and hardening before production use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
