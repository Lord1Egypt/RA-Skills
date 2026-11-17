## Description:

Classify construction data by type (structured, unstructured, semi-structured), analyze data sources, and recommend appropriate storage and processing methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data analysts, engineers, and project teams use this skill to classify user-provided construction datasets or file paths, identify their structure and format, and choose storage, processing, and integration approaches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can analyze local project files or file paths supplied by the user, which may expose unrelated private data if users provide broad or unnecessary inputs.

Mitigation: Use only construction datasets intended for classification and avoid providing unrelated private files unless they are required for the analysis.

Risk: Classification and storage recommendations may be incomplete or incorrect when source metadata, samples, or file extensions are limited.

Mitigation: Validate inputs before processing and review recommendations against construction data requirements before acting on them.

## Reference(s):

- [Data-Driven Construction](https://datadrivenconstruction.io)
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/data-type-classifier)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured tables and optional JSON, CSV, or Excel export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include classification summaries, storage recommendations, processing-tool suggestions, integration options, quality considerations, and confidence scores.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact/claw.json states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
