## Description:

Fetches daily arXiv papers for configured categories, helps schedule paper retrieval and delivery, and guides the agent to summarize and send results to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hislocked](https://clawhub.ai/user/hislocked)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure recurring arXiv category subscriptions, fetch recent papers, generate concise paper summaries, and send scheduled paper digests through a configured delivery channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the skill may silently install unpinned Python packages.

Mitigation: Install reviewed, pinned dependencies in a virtual environment before running the helper script.

Risk: The security review notes recurring timers and persisted delivery identifiers for scheduled pushes.

Mitigation: Review timer settings and remove scheduled jobs and like-*.txt configuration files when the subscription is no longer needed.

Risk: The skill stores fetched paper data, generated summaries, and delivery configuration locally.

Mitigation: Keep output paths inside the skill directory and avoid adding sensitive account or chat identifiers beyond what delivery requires.

## Reference(s):

- [arXiv](https://arxiv.org/)
- [arXiv recent category listings](https://arxiv.org/list/cs.CV/recent)
- [ClawHub skill page](https://clawhub.ai/hislocked/skills/arxiv-daily)
- [Publisher profile](https://clawhub.ai/user/hislocked)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, configuration text, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local subscription configuration files and daily paper data or summary files.]

## Skill Version(s):

0.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
