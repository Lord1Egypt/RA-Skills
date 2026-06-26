## Description: <br>
Claw Compactor is a token compression skill for OpenClaw agents that reduces workspace token usage with deterministic compression layers and optional Engram observational memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli-2025](https://clawhub.ai/user/gandli-2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to benchmark, compress, and summarize agent workspace context, memory files, session transcripts, and prompt material before those tokens are sent to an LLM. It is especially relevant for long-running OpenClaw-style workflows that need lower token spend, tiered memory summaries, or reusable compressed context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full or automatic compression can rewrite workspace and memory files. <br>
Mitigation: Run benchmark or dry-run modes first and keep backups before enabling full or auto compression. <br>
Risk: The bundled proxy and dashboards can expose prompt traffic, tokens, worker state, or metrics if reachable from an untrusted network. <br>
Mitigation: Keep the proxy local or behind strong authentication, rotate default tokens, and avoid exposing dashboard or metrics endpoints publicly. <br>
Risk: Autonomous CLI-agent mode can run high-impact agent actions through configured workers. <br>
Mitigation: Leave USE_CLI_AGENTS disabled unless workers are sandboxed and the operational boundary is explicitly reviewed. <br>
Risk: Environment files, Redis state, memory files, prompt previews, and LLM endpoints may contain sensitive data. <br>
Mitigation: Treat those paths as secrets-bearing data, restrict file permissions, and avoid collecting or sharing them in logs or benchmark artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli-2025/claw-compactor) <br>
- [SKILL.md](SKILL.md) <br>
- [Architecture reference](references/architecture.md) <br>
- [Benchmarks reference](references/benchmarks.md) <br>
- [Compression techniques](references/compression-techniques.md) <br>
- [Testing reference](references/testing.md) <br>
- [Proxy README](proxy/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, optional JSON reports, and compressed text or memory summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update workspace memory files, tiered summaries, dictionary codebooks, benchmark reports, and Engram observation or reflection files depending on the selected command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
