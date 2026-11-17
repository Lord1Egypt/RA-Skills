## Description:

Generate and prioritize US equity long-side edge research tickets from EOD observations, then export pipeline-ready candidate specs for trade-strategy-pipeline Phase I.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to turn market observations, EOD anomalies, and trading hypotheses into structured research tickets and Phase I-compatible strategy artifacts for backtesting handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM idea generation can execute a local command supplied through --llm-ideas-cmd.

Mitigation: Use --llm-ideas-cmd only with trusted executables in a constrained workspace.

Risk: Exporting untrusted ticket files or using overwrite behavior can create unsafe strategy artifact writes.

Mitigation: Validate ticket sources, constrain candidate IDs and output paths, and avoid --force unless the destination is known.

Risk: Generated research tickets and strategy specs may be incorrect or unprofitable.

Mitigation: Review each candidate, validate interface compatibility, and run independent backtests before any trading use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-edge-dv)
- [Ideation Loop](references/ideation_loop.md)
- [Pipeline Interface v1](references/pipeline_if_v1.md)
- [Research Ticket Schema](references/research_ticket_schema.md)
- [Signal Mapping](references/signal_mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance plus YAML strategy specifications, JSON metadata, validation output, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces research tickets and optional strategy.yaml plus metadata.json files; it does not run backtests or provide live trading signals.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
