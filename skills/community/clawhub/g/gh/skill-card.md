## Description:

Use the GitHub CLI (gh) to perform authenticated GitHub operations including auth checks, repo creation, cloning, forking, issues, pull requests, releases, and basic repo management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trumppo](https://clawhub.ai/user/trumppo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to have an agent perform GitHub CLI workflows for repositories, issues, pull requests, and releases, then report resulting URLs or status back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated gh commands can create or modify repositories, issues, pull requests, releases, and comments.

Mitigation: Review the requested gh action and target repository before execution, especially repo creation, issue or PR comments, PR merges, releases, deletes, and force-push-related work.

Risk: Repository visibility or ownership can be set incorrectly during repository creation.

Mitigation: Confirm the target owner and intended visibility before creation, and use --private when creating private repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository, issue, pull request, or release URLs returned by gh.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
