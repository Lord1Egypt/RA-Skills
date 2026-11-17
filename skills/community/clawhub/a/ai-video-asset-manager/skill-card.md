## Description:

Helps agents manage AI video production assets, including character, scene, and prop records, shot planning, generation logs, consistency checks, and rework tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlxeva](https://clawhub.ai/user/dlxeva)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and production teams use this skill to keep AI video assets, shot plans, reference indexes, generation records, consistency checks, and rework notes organized across a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch downloader can fetch arbitrary URLs and write files outside the intended asset directory.

Mitigation: Review URLs and filenames before use, restrict downloads to trusted HTTPS sources, enforce destination containment, avoid silent overwrites, and add size and content-type checks before production use.

Risk: The project initializer creates or updates files under user-provided project paths.

Mitigation: Run the initializer only on intended project directories and review generated files before committing or using them in production workflows.

## Reference(s):

- [Consistency Rules](references/consistency-rules.md)
- [Project Templates](references/project-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown records, project directory structures, Python helper commands, and project configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces asset cards, shot cards, reference indexes, generation logs, consistency check records, rework records, and initialization/download commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
