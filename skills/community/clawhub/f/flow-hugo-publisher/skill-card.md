## Description:

Helps agents manage Hugo publishing workflows by checking Hugo and Git, managing a workspace, initializing a Hugo site and Git repository, previewing locally, committing changes, and guiding GitHub Pages deployment through GitHub Actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zamporen](https://clawhub.ai/user/zamporen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use this skill to prepare, preview, commit, and publish Hugo sites or articles to GitHub Pages while preserving workflow state across workspaces. It focuses on the publishing pipeline and does not create article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated Git staging and publishing may include files the user did not intend to commit or push.

Mitigation: Review the exact staged files before commits or pushes, avoid broad staging such as git add ., and check for credentials, private drafts, local configuration, and unrelated files.

Risk: The skill writes persistent local workspace metadata.

Mitigation: Treat the state file as local metadata and review it before sharing logs, workspaces, or machine snapshots.

Risk: Generated GitHub Actions workflows introduce third-party action dependencies and can publish site content publicly.

Mitigation: Review the generated workflow dependencies and GitHub Pages settings before enabling deployment or pushing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zamporen/skills/flow-hugo-publisher)
- [Workflow and command templates](references/workflow.md)
- [State file schema](references/state-schema.md)
- [User interaction points](references/interaction-points.md)
- [Validation and recovery checklist](references/validation-checklist.md)
- [Template catalog](references/template-catalog.md)
- [GitHub Actions deployment guide](references/github-actions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, workflow files, progress messages, and recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Hugo workspace files, GitHub Actions workflow configuration, deployment guidance, Git commits, and persistent local workspace state when the user approves those steps.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
