## Description:

Claw Compactor v6.0 provides rule-based workspace, memory, and session transcript compression using dictionary encoding, observation extraction, and progressive context summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeromomo](https://clawhub.ai/user/aeromomo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to estimate token usage, compress workspace memory files, convert session transcripts into concise observations, and generate progressive memory summaries for lower-cost context loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite many workspace files during compression.

Mitigation: Start with benchmark or dry-run mode in a version-controlled or disposable workspace before allowing write operations.

Risk: The skill can read global session transcripts and produce observations or codebooks that may retain sensitive transcript details.

Mitigation: Review generated observations and codebooks before committing or sharing them, and keep transcript-derived artifacts private unless approved.

Risk: Heartbeat or cron automation can cause recurring future workspace mutations.

Mitigation: Avoid install, heartbeat, or cron automation unless recurring compression is explicitly intended and its scope has been reviewed.

## Reference(s):

- [Architecture](references/architecture.md)
- [Compression Techniques](references/compression-techniques.md)
- [Benchmarks](references/benchmarks.md)
- [Testing](references/testing.md)
- [Compression Prompts](references/compression-prompts.md)
- [Reference Index](references/README.md)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate or update workspace memory files, codebooks, observation summaries, and tiered memory summaries; benchmark and dry-run modes are available for preview.]

## Skill Version(s):

6.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
