## Description:

Use this skill to audit CLI adapter projects for missing output fields, then batch-generate fixes and submit PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allens0104](https://clawhub.ai/user/allens0104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit CLI adapter projects for missing standard output fields, classify fix strategies, apply additive code changes, and prepare multi-file pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to inspect and edit adapter code across multiple files, which can introduce incorrect or unwanted changes if proposals are applied without review.

Mitigation: Review generated diffs before merging or submitting pull requests, and run the target project's existing build and test commands after changes.

Risk: Constructed output fields such as URLs can be wrong when the required data is unavailable or platform formats are misunderstood.

Mitigation: Skip fields that require unavailable external data, verify constructed URL formats for each platform, and keep changes additive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allens0104/skills/adapter-audit)
- [Publisher profile](https://clawhub.ai/user/allens0104)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with tables, code diffs, shell commands, and pull request text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include adapter coverage metrics, fix classifications, changed-file lists, and risk classification.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
