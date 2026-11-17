## Description:

Extract structured JSON data from 40+ supported platforms via the Bright Data CLI (`bdata pipelines`) when a user provides a known platform URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and run Bright Data `bdata pipelines` commands for supported platform URLs, then verify JSON or NDJSON outputs before using them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline outputs can include personal or restricted platform data such as profiles, reviews, comments, posts, or business records.

Mitigation: Collect only data the user is authorized to process, follow target platform terms, and protect local output files.

Risk: Pipeline names, supported platforms, and input shapes can change over time.

Mitigation: Run `bdata pipelines list` before use and verify command output for parse errors, record counts, and per-record errors.

Risk: Large review, comment, post, or batch jobs can trigger long-running server-side work and consume quota.

Mitigation: Use the documented timeout guidance and keep batch parallelism low.

## Reference(s):

- [Data Feeds skill page](https://clawhub.ai/meirk-brd/skills/brightdata-data-feeds)
- [Data-feeds worked examples](references/examples.md)
- [bdata pipelines flag reference](references/flags.md)
- [Data-feeds patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON, NDJSON, JSONL, or CSV output verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can produce local platform data files containing product, profile, review, post, comment, or business records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
