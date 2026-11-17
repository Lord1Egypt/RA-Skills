## Description:

Guides an agent through reviewing a branch, asking for approval before pushing, creating provider-specific pull requests, verifying settings, and reporting PR URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to publish reviewed branches and create verified pull requests across GitHub or Azure DevOps workflows. It is intended for branch-to-PR handoff, including multi-repo work items that need sibling PR links and deploy-order notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous phrases such as "PR this" or "ship this branch" can invoke a workflow that publishes repository branches.

Mitigation: Confirm the work item, branch, repositories, and exact tree before publication, and require explicit user approval before any push.

Risk: Configured defaults for reviewers, target branches, work-item links, auto-complete, or auto-merge can affect the resulting pull request.

Mitigation: Review push approval carefully and re-read each created PR to verify required reviewers, target branch, work-item link, and merge settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/create-pr)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples, PR body structure, and verification tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces branch review status, push approval prompts, PR description content, sibling PR references, and final PR URL tables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
