## Description:

Helps agents write, deploy, and interact with GenLayer Python smart contracts that use LLM calls, web access, and consensus-safe non-determinism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acastellana](https://clawhub.ai/user/acastellana)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate GenLayer Intelligent Contract code, follow SDK and CLI patterns, deploy to local or test networks, and reason about LLM or web-enabled contract consensus behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready deploy, write, and account commands can affect contracts, balances, or wallet accounts.

Mitigation: Require explicit user approval before deploy, write, or account operations; prefer localnet or low-value test accounts.

Risk: Private keys or sensitive account material could be exposed through command arguments or agent logs.

Mitigation: Do not paste production private keys into command arguments; use safer secret-handling workflows outside the skill guidance.

Risk: LLM prompts, user text, URLs, and fetched webpages may leave the local environment or influence generated contract behavior.

Mitigation: Treat those inputs as untrusted data, validate outputs against expected schemas, and review contract logic before deployment.

Risk: Unpinned dependencies or skill revisions can change generated behavior over time.

Mitigation: Pin GenLayer dependencies and the skill revision before use in security-sensitive workflows.

## Reference(s):

- [GenLayer SDK API Reference](artifact/references/sdk-api.md)
- [Equivalence Principles - In-Depth Guide](artifact/references/equivalence-principles.md)
- [GenLayer Contract Examples](artifact/references/examples.md)
- [GenLayer Deployment Guide](artifact/references/deployment.md)
- [GenVM Internals](artifact/references/genvm-internals.md)
- [GenLayer Docs](https://docs.genlayer.com)
- [GenLayer SDK](https://sdk.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [GenLayer GitHub](https://github.com/genlayerlabs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell command snippets, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing development guidance; the skill itself does not execute commands or deploy contracts.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and changelog state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
