## Description:

Browse and load ready-to-use AI/ML datasets with fast manipulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to record dataset-related operations, inspect recent local entries, search activity logs, and export accumulated records for lightweight workflow tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied dataset-related text is stored persistently in local plaintext logs and may later be searched or exported.

Mitigation: Do not enter secrets, access tokens, personal data, proprietary samples, or sensitive file paths unless local retention and export are acceptable.

Risk: The release is described as a dataset browser/loader, while the artifact primarily records activity text rather than loading datasets.

Mitigation: Review the artifact as a local activity logger and confirm that this behavior matches the intended use before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/datasets)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local log and export files under ~/.local/share/datasets.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
