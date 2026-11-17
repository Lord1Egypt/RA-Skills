## Description:

Configurable quality evaluation for AI agent outputs. Define criteria, run evaluations, track quality over time. No LLM-as-judge, no API calls, pattern-based automated checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use Agent Scorecard to evaluate text outputs from AI agents against configurable quality dimensions, compare changes, and track quality trends over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool reads the response, configuration, and history files selected by the user, which may contain sensitive agent outputs.

Mitigation: Use trusted local configurations, avoid processing sensitive outputs unless local storage is acceptable, and keep generated history and report files in controlled locations.

Risk: Report generation and history tracking can write files to user-selected paths, including replacing existing report files.

Mitigation: Review output paths before running reports or history saves, and keep backups for important evaluation data.

Risk: Automated scoring is pattern-based and may miss semantic issues or produce false positives on surface-level checks.

Mitigation: Use manual or blended scoring for decisions that require factual, semantic, or high-stakes quality judgment.

## Reference(s):

- [Agent Scorecard ClawHub Page](https://clawhub.ai/theshadowrose/skills/agent-scorecard)
- [README.md](artifact/README.md)
- [LIMITATIONS.md](artifact/LIMITATIONS.md)
- [config_example.json](artifact/config_example.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal summaries, JSON evaluation records, JSONL history, and Markdown or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-selected text and configuration files; report and history outputs are written only to paths selected by the user.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
