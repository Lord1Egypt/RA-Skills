## Description:

基于8维发展模型（D0关系、D1运动、D2学业、D3认知、D4社交、D5习惯、D6动机、D7兴趣），帮助家长持续记录、整理和分析儿童成长档案，并关注内在动机和关系安全感。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill to turn child growth observations into structured Markdown records, monthly notes, quarterly assessments, trend summaries, and practical guidance. It is intended for personal tracking and reflection, not as a standalone clinical, educational, or developmental diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive records about a minor and includes hardcoded child-specific details.

Mitigation: Replace the child name, birth month, baseline data, and file paths with private placeholders before use.

Risk: Child records may be exposed if used in shared workspaces or locations with broad backup, sync, or indexing access.

Mitigation: Use a private storage location and require explicit confirmation before recording or reading child records.

Risk: Growth data and benchmark comparisons can be overread as definitive judgments.

Mitigation: Treat records as observation aids only, combine them with caregiver judgment, and avoid using the skill as a standalone clinical or educational assessment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duzhilei951/skills/child-growth-tracker)
- [External Benchmark Reference Data](artifact/references/benchmarks.md)
- [Monthly Note Template](artifact/references/template-monthly.md)
- [Quarterly Assessment Template](artifact/references/template-quarterly.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown records, tables, summaries, and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update child growth record files in a workspace when the user requests tracking or assessment.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter, artifact manifest, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
