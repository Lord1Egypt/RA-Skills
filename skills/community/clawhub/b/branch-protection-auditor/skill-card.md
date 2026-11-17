## Description:

Audit GitHub/GitLab branch protection rules across repositories, checking required reviews, status checks, force push restrictions, admin bypass, and CODEOWNERS enforcement before flagging gaps and generating recommended rulesets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and compliance teams use this skill to audit GitHub or GitLab branch protection coverage, identify repositories with weak controls, and prepare recommended protection rules before compliance reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided fix command can overwrite existing repository protections without preserving stronger controls.

Mitigation: Fetch existing branch-protection settings first, preserve current status checks and restrictions, target the actual default branch, and require explicit before-and-after review before applying changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, audit tables, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit findings, compliance mapping, and proposed branch-protection changes for review before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
