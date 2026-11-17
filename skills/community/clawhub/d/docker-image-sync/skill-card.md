## Description:

Syncs Docker Hub images to a CNB.tool registry via GitHub Actions to help OpenClaw pull images when direct Docker Hub access fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lufei4](https://clawhub.ai/user/lufei4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure a private GitHub Actions proxy that syncs requested Docker images into CNB, then pull those images locally when Docker Hub access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub and CNB tokens may be handled by OpenClaw and persisted in local configuration.

Mitigation: Prefer gh auth login, avoid pasting tokens into chat, use short-lived narrowly scoped tokens, protect local secret files, and rotate any token previously exposed.

Risk: The skill creates or updates a private GitHub repository, sets Repository Secrets, and pushes a GitHub Actions workflow.

Mitigation: Inspect the workflow before running it, confirm the repository is private, and restrict any GitHub token to the required repository and workflow, contents, and secrets permissions.

Risk: The sync workflow pulls Docker images and republishes them into a CNB registry for later local pulls.

Mitigation: Review requested image names and GitHub Actions results before relying on synced images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lufei4/skills/docker-image-sync)
- [GitHub CLI](https://cli.github.com)
- [Docker Desktop for Linux install docs](https://docs.docker.com/desktop/install/linux-install/)
- [CNB](https://cnb.cool/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status messages and commands for setup, image sync, and local image pull operations.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
