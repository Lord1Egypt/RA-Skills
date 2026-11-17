## Description:

Claw Compactor helps agents reduce LLM context and workspace token usage with deterministic compression, benchmark reporting, and optional Engram memory compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli-2025](https://clawhub.ai/user/gandli-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to benchmark, compress, and audit workspace context, memory files, session transcripts, and prompt payloads before sending them to LLMs. It is suited for reducing repeated context cost while preserving operationally useful information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory and proxy components can expose private chats.

Mitigation: Use deterministic compression features unless Engram or the proxy is explicitly needed, and periodically inspect or delete memory under memory/engram.

Risk: The included proxy can run powerful agent actions without strong safeguards.

Mitigation: Set a strong PROXY_AUTH_TOKEN, bind the proxy to loopback or a protected network, and avoid USE_CLI_AGENTS unless it is sandboxed.

Risk: External or plaintext model endpoints can leak sensitive context.

Mitigation: Do not point OPENAI_BASE_URL at an untrusted or plaintext remote endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gandli-2025/skills/claw-compactor)
- [Architecture Reference](references/architecture.md)
- [Compression Techniques](references/compression-techniques.md)
- [Benchmark Reference](references/benchmarks.md)
- [Documentation Index](docs/README.md)
- [Proxy Documentation](proxy/README.md)
- [Security Policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON reports, configuration snippets, and compressed text or markdown artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce lossy summaries for observation memory and reversible markers for supported compression stages.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
