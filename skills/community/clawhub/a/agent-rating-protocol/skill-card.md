## Description:

Agent Rating Protocol helps agents rate collaborators, check reputation, and export verifiable reputation bundles using a decentralized trust-scoring workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill after transactions to submit blind bilateral ratings, before tasks to compare agent reputations, and when they need to present a verifiable track record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned PyPI package before use.

Mitigation: Install in an isolated Python environment and pin or audit the agent-rating-protocol package before using it in sensitive workflows.

Risk: The documented workflows read and write local rating store files such as ratings.jsonl.

Mitigation: Use a dedicated rating store path and avoid pointing the workflow at sensitive files unless the package code has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexfleetcommander/skills/agent-rating-protocol)
- [Publisher Profile](https://clawhub.ai/user/alexfleetcommander)
- [Vibe Agent Making](https://vibeagentmaking.com)
- [Agent Rating Protocol PyPI Package](https://pypi.org/project/agent-rating-protocol/)
- [Rating Protocol Whitepaper](https://vibeagentmaking.com/whitepaper/rating-protocol/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and pip or pip3 to install the agent-rating-protocol package.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
