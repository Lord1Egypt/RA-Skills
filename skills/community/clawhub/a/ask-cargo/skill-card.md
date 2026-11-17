## Description:

Deploys a Slack-triggered agent that answers questions from a go-to-market repository and workspace, proposes changes as pull requests, captures selected threads, and routes approved work to deployed agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Go-to-market teams and developers use it to deploy a shared Slack agent that answers from their repository and workspace, opens reviewable pull requests, captures selected internal threads, and routes approved jobs to the agents that own them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata requests @cargo-ai/cli@latest, so the installed CLI version can change between reviews.

Mitigation: Review the package release before installing and use an approved pinned version if the installation workflow supports it.

Risk: Selected Slack thread content can be written into persistent cadence and context files.

Mitigation: Review channel reach before deployment, keep the bot out of customer-shared channels, and capture only appropriate internal threads.

Risk: The security assessment is incomplete because one referenced file was not fully interpreted.

Mitigation: Review the uninterpreted file and the deployment’s Slack access before relying on the assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/ask-cargo)
- [Project homepage](https://github.com/getcargohq/gtm-skills)
- [Capture entry format](references/capture-entry.md)
- [Agent roster](references/roster.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files]

**Output Format:** [Slack thread responses and pull request diffs; repository files in Markdown and code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that run work or incur spend wait for explicit approval in the Slack thread.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
