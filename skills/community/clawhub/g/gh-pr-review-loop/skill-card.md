## Description:

Drive a GitHub pull request through an iterative review-and-fix loop, including creating a PR when needed, inspecting review feedback, implementing fixes, pushing updates, resolving fixed threads, watching CI, and polling until the requested stop condition is met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevetdp](https://clawhub.ai/user/stevetdp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to keep an explicit GitHub PR review workflow moving: inspect comments and CI, apply validated fixes, maintain the requested branch history, push updates, and continue polling until approval criteria are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub credentials may allow writes outside the intended pull request scope.

Mitigation: Scope credentials to the target repository and branch where possible, and verify the repository, PR, active branch, and requested history strategy before edits, pushes, PR mutations, or thread resolution.

Risk: History rewrites or force pushes can damage unrelated or protected branches if applied to the wrong target.

Mitigation: Use force-with-lease only on the active PR head branch and treat ambiguous repository, branch, or permission state as a blocker.

Risk: Resolving review threads too early can hide unresolved feedback.

Mitigation: Resolve threads only after fixes are validated locally, pushed, and rechecked against the remote PR state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevetdp/skills/gh-pr-review-loop)
- [Publisher profile](https://clawhub.ai/user/stevetdp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status updates with inline shell commands and code changes in the target repository]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a pull request, push commits, resolve review threads, watch CI, and rewrite only the active PR branch when the requested workflow requires it.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
