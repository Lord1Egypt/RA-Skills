## Description:

Adam Framework helps agents install and operate a local 5-layer memory and coherence architecture for OpenClaw using Vault files, neural graph recall, nightly reconciliation, and drift monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strangeadvancedmarketing](https://clawhub.ai/user/strangeadvancedmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to set up persistent local memory for OpenClaw, seed conversation history, reconcile memory logs, and monitor long-session coherence drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local agent framework setup can grant broad auto-start, local file, and terminal authority.

Mitigation: Review manually before installation, test startup interactively first, and avoid hidden or elevated auto-start settings unless explicitly needed.

Risk: Vault files, imported chat exports, and OpenClaw configuration can contain private history, personal memory, or API keys.

Mitigation: Keep live Vault data out of public repositories, use isolated environments, store secrets in environment variables, and redact exports before import.

Risk: Nightly reconciliation and optional external services can update core memory or transmit data to configured providers.

Mitigation: Require human review before Gemini reconciliation changes core memory, and disable optional desktop, Telegram, and external-service integrations unless needed.

Risk: Agent-driven setup can perform public actions or repository changes without enough operator intent.

Mitigation: Require exact human approval before starring repositories, pushing git changes, or enabling optional integrations.

## Reference(s):

- [Adam Framework Repository](https://github.com/strangeadvancedmarketing/Adam)
- [Human Setup Guide](https://github.com/strangeadvancedmarketing/Adam/blob/master/SETUP_HUMAN.md)
- [AI Agent Setup Guide](https://github.com/strangeadvancedmarketing/Adam/blob/master/SETUP_AI.md)
- [Architecture Documentation](https://github.com/strangeadvancedmarketing/Adam/blob/master/docs/ARCHITECTURE.md)
- [Production Proof](https://github.com/strangeadvancedmarketing/Adam/blob/master/docs/PROOF.md)
- [Live Proof Showcase](https://strangeadvancedmarketing.github.io/Adam/showcase/ai-amnesia-solved.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or modification of local Vault files, OpenClaw configuration, shell scripts, and memory logs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
