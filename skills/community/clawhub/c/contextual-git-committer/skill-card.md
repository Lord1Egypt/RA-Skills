## Description:

AI-powered Git assistant that analyzes staged changes and terminal history to craft meaningful, conventional commit messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill inside a Git repository to analyze staged changes and receive three candidate commit messages in conventional, detailed, and emoji styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent shell commands and staged source diffs can contain credentials, private paths, unpublished code, or operational details in model-facing output.

Mitigation: Review before installing; use only where staged diffs and shell history are appropriate to share, and make history collection opt-in, scoped, previewed, and redacted before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liverock/skills/contextual-git-committer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns three commit message options and may include local Git context in agent-facing output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
