## Description:

Generates a daily digest of Bitcoin Development mailing list activity and Bitcoin Core commits for recent discussions, code changes, and recurring morning summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawd21](https://clawhub.ai/user/clawd21)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to follow Bitcoin protocol discussions and Bitcoin Core commit activity without manually checking mailing-list threads and repository history. It can also support a daily briefing workflow through scheduled digest generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched mailing-list text is untrusted and may contain misleading or adversarial content.

Mitigation: Review generated summaries before relying on them and treat raw archived source text as untrusted input.

Risk: A daily schedule can repeatedly fetch public Bitcoin development content and retain raw copies locally.

Mitigation: Enable only schedules the user intends to run and periodically delete archives if indefinite retention is not desired.

## Reference(s):

- [Bitcoin Daily ClawHub page](https://clawhub.ai/clawd21/skills/bitcoin-daily)
- [Bitcoin Development mailing list](https://groups.google.com/g/bitcoindev)
- [Bitcoin Core commits](https://github.com/bitcoin/bitcoin/commits/master/)
- [bitcoindev public-inbox mirror](https://gnusha.org/pi/bitcoindev/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown summaries with linked mailing-list threads and pull requests, plus JSON and Markdown archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives raw public source data and generated summaries under ~/workspace/bitcoin-dev-archive/YYYY-MM-DD/.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
