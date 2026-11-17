## Description:

Creates or reuses Jira Cloud issues and related Bitbucket Cloud branches, with previews and verification of issue and branch details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvolutionor](https://clawhub.ai/user/alvolutionor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to create Jira issues, update their assignment, status, and sprint, and create or reuse related Bitbucket branches in requested repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the workflow can create Jira issues, change issue fields, and push Bitbucket branches.

Mitigation: Review the preview and requested repositories before applying writes; use narrowly scoped Jira and Bitbucket tokens.

Risk: Private configuration or API credentials could be exposed if stored with public project files.

Mitigation: Keep WORKFLOW_CONFIG outside the repository and supply credentials through a credential manager.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alvolutionor/skills/create-branch)
- [Private configuration and usage](artifact/references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with issue and branch links and verified status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Previews by default; reports incomplete steps when verification fails.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
