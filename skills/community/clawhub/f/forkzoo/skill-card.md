## Description:

Adopt and manage GitHub-native digital pets (tamagotchis) that evolve daily with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levi-law](https://clawhub.ai/user/levi-law)

### License/Terms of Use:


## Use Case:

External users and developers use ForkZoo to adopt, check, and interact with GitHub-hosted digital pets through agent-proposed shell commands and GitHub API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a powerful GitHub token to fork repositories, enable unrestricted GitHub Actions, dispatch workflows, and publish GitHub Pages content.

Mitigation: Review the skill before installing, use a fine-grained or throwaway token with the smallest possible repository permissions from a dedicated account, audit upstream ForkZoo repositories and workflows, and revoke the token after use.

## Reference(s):

- [ForkZoo ClawHub skill page](https://clawhub.ai/levi-law/skills/forkzoo)
- [ForkZoo main site](https://forkzoo.com)
- [ForkZoo GitHub organization](https://github.com/forkZoo)
- [Original forkMonkey project](https://github.com/roeiba/forkMonkey)
- [ForkZoo gallery](https://forkzoo.com/gallery)
- [ForkZoo leaderboard](https://forkzoo.com/leaderboard)
- [ForkZoo family trees](https://forkzoo.com/trees)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token when executing the provided scripts; scripts may call GitHub APIs, enable Actions, dispatch workflows, and configure Pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
