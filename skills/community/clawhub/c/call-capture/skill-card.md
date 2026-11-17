## Description:

Collects recorded sales calls, turns them into reviewed log entries, and proposes recurring insights for a go-to-market knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales leaders, account executives, and revenue operations teams can use this skill in a Cargo project to collect completed recorder calls, create call logs, and propose recurring insights through a reviewable pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call transcripts may contain sensitive information that is sent to hosted model services and stored as raw captures in a repository.

Mitigation: Confirm that your organization permits this handling, and limit captured data and repository access to what the workflow needs.

Risk: The workflow has broad workspace-variable access and repository write capability, and the security scan did not inspect every file.

Mitigation: Review the planned workspace access and repository permissions, inspect the skill and its proposed changes, and require a human to review and merge each pull request.

## Reference(s):

- [Provider setup and adapter guidance](artifact/references/providers.md)
- [Recorder API reference](artifact/references/recorder-apis.md)
- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/call-capture)

## Skill Output:

**Output Type(s):** [Markdown files, Code changes, Pull request]

**Output Format:** [Call logs and knowledge-base updates in Markdown, proposed in a GitHub pull request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled collection; proposed changes require human review and merge.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
