## Description:

Publish local changes to a GitHub pull request and keep working the PR until review feedback is addressed and required checks are green.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to publish local changes as a GitHub pull request, run a pre-publish review gate, address approved review feedback and failing CI, and continue until actionable review threads and required checks are clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through PR publication, commits, pushes, review-feedback fixes, and CI investigation.

Mitigation: Confirm the intended files, branch, and PR target before publication, and give explicit permission only for the GitHub or local-code actions you want.

Risk: Automated review and CI fixes can change local code in ways that need project-specific judgment.

Mitigation: Review proposed changes, approve only selected findings, and run relevant local validation before pushing fixes.

Risk: Some GitHub actions, such as posting comments or changing PR state, can affect collaboration workflow.

Mitigation: Require explicit user authorization before posting GitHub comments, resolving threads, requesting reviewers, changing labels or titles, marking ready, closing, or merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patrick-erichsen-2/skills/all-green)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command summaries, review findings, code-change descriptions, and PR status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PR URLs, head SHAs, local validation results, required-check status, and remaining blockers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
