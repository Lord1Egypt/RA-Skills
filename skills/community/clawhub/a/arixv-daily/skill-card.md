## Description:

Fetches daily arXiv papers for configured categories, helps an agent summarize them, and supports scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hislocked](https://clawhub.ai/user/hislocked)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure daily arXiv category subscriptions, fetch recent papers, generate concise paper summaries, and deliver them through a chosen channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The run script can install unpinned Python packages automatically.

Mitigation: Review run.sh before execution and install requests and beautifulsoup4 manually in a virtual environment with pinned versions.

Risk: Subscription and push settings may send generated summaries to an unintended channel.

Mitigation: Confirm the category, schedule, channel, account, and chat identifier before enabling recurring timers.

Risk: The workflow writes local configuration and paper data files.

Mitigation: Review the references and data directories for sensitive delivery settings and remove stale generated data when it is no longer needed.

## Reference(s):

- [arXiv](https://arxiv.org/)
- [arXiv recent papers example](https://arxiv.org/list/cs.CV/recent)
- [ClawHub skill page](https://clawhub.ai/hislocked/skills/arixv-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, plain-text paper records, configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch commands accept an arXiv category, save path, and optional date; generated summaries are intended for scheduled delivery.]

## Skill Version(s):

0.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
