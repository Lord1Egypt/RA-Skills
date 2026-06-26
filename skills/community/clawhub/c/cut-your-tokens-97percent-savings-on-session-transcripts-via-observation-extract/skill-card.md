## Description: <br>
Claw Compactor v6.0 - 50%+ savings through rule-based compression, dictionary encoding, session observation compression, and progressive context loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeromomo](https://clawhub.ai/user/aeromomo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to estimate, compress, deduplicate, and summarize workspace memory files and OpenClaw session transcripts so agents can load less context while retaining important facts and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process local OpenClaw transcripts and workspace memory files that may contain private paths, commands, transcript-derived facts, or secrets. <br>
Mitigation: Run benchmark and command-specific dry-run modes first, review affected files, and keep version control or backups before writing changes. <br>
Risk: The full pipeline and heartbeat or cron automation can rewrite workspace memory without interactive review. <br>
Mitigation: Avoid full or unattended automation on important workspaces until the files it touches and the automation schedule are explicitly acceptable. <br>
Risk: Generated .codebook.json files and observation summaries may preserve sensitive facts from the original workspace or transcripts. <br>
Mitigation: Treat generated compression artifacts as sensitive and review storage or sharing controls before distributing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aeromomo/cut-your-tokens-97percent-savings-on-session-transcripts-via-observation-extraction) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/aeromomo) <br>
- [References Overview](references/README.md) <br>
- [Architecture](references/architecture.md) <br>
- [Compression Techniques](references/compression-techniques.md) <br>
- [Performance Benchmarks](references/benchmarks.md) <br>
- [Testing](references/testing.md) <br>
- [Compression Prompts](references/compression-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON reports, compressed memory files, observation summaries, tiered summaries, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rewrite workspace memory files, create codebooks and observation summaries, and emit dry-run or JSON reports depending on the selected command.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
