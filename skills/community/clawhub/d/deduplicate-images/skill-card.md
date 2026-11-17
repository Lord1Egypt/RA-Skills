## Description:

Recursively scans image folders, compares images with a configurable similarity threshold, and moves lower-quality duplicates to a local trash folder while keeping higher-resolution originals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onealmeng](https://clawhub.ai/user/onealmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize photo collections, media libraries, and e-commerce image sets by identifying visually similar images and moving likely duplicates out of their source folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically move many image files out of their original folders without a review or rollback step.

Mitigation: Run it first on a copied test folder with a strict similarity value, and avoid whole home directories, shared libraries, or irreplaceable archives until a dry-run or review mode is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onealmeng/skills/deduplicate-images)
- [ClawHub publisher profile](https://clawhub.ai/user/onealmeng)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a local Python image deduplication script using a target folder path and similarity threshold.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
