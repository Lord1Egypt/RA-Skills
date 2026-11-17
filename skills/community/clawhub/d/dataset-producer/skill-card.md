## Description:

Produce complete, publish-ready AI/ML datasets in HuggingFace format (parquet shards + README.md with YAML frontmatter + dataset card + provenance script).

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkd](https://clawhub.ai/user/darkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to package training, fine-tuning, evaluation, and benchmark datasets into HuggingFace-compatible releases with schema validation, parquet sharding, dataset-card metadata, licensing, and provenance artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation or dataset-building logs may expose sensitive or regulated data.

Mitigation: Control logs when processing confidential data, and mask or disable raw PII output before sharing logs.

Risk: Old dataset shards may remain in an output folder and become part of a publishable dataset.

Mitigation: Build into a fresh output directory for every run and inspect the dataset folder before upload.

Risk: A dataset may be published before licensing, PII, provenance, and generated files are reviewed.

Mitigation: Inspect the complete dataset folder and only push to HuggingFace when explicitly requested with appropriate credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darkd/skills/dataset-producer)
- [Dataset card template](artifact/references/card-template.md)
- [Clarifying questions](artifact/references/clarifying-questions.md)
- [Dataset format guide](artifact/references/format-guide.md)
- [Multi-config datasets](artifact/references/multi-config.md)
- [Quality checklist](artifact/references/quality-checklist.md)
- [Schema reference](artifact/references/schemas.md)
- [Smoke test guide](artifact/references/smoke-test.md)
- [YAML frontmatter spec](artifact/references/yaml-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell commands, plus generated dataset files such as parquet shards, README.md, LICENSE, create_dataset.py, stats.json, and feature specifications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local review before any optional HuggingFace upload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
