## Description:

Research competitor advertising on Meta, TikTok, and LinkedIn, including hooks, offers, calls to action, and how long ads have run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can research competitor or category ads across Meta, TikTok, and LinkedIn, then review an ad table and a report of advertisers, run duration, messaging angles, offers, and calls to action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DataXAPI package is unpinned, creating a supply-chain risk when it runs with the agent's permissions.

Mitigation: Install a reviewed exact package version before use.

Risk: The agent environment may have access to local files and the DataXAPI API key.

Mitigation: Use a narrowly scoped, budget-limited API key and avoid exposing it in output.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill page](https://clawhub.ai/data-x-api/skills/dataxapi-ad-library-research)

## Skill Output:

**Output Type(s):** [CSV data, Markdown report, Advertising analysis]

**Output Format:** [CSV table and Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One row per ad; fields a platform does not provide are left empty.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
