## Description:

Analyze the top 100 S&P 500 companies by market capitalization using CANSLIM-style signals and return a ranked shortlist in Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkmsteven](https://clawhub.ai/user/lkmsteven)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to run a local CANSLIM-style screen of large-cap U.S. stocks and produce a ranked Markdown summary. The skill is intended for stock-screening assistance, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies are unpinned.

Mitigation: Run the skill in an isolated Python environment and review or pin dependency versions before deployment.

Risk: The script contacts Wikipedia and market-data services and writes local stock-screening output.

Mitigation: Run it only where outbound network access and a local canslim_results.json file are acceptable, and review outputs before sharing.

Risk: The generated rankings may be mistaken for investment advice.

Mitigation: Present results as screening assistance only and include caveats for missing data, weak signals, and market-data limitations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkmsteven/skills/canslim-top100-us)
- [Wikipedia S&P 500 constituents](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown with a ranked table, concise assessment, explanatory bullets, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a locally generated canslim_results.json file and may report dependency, network, or missing-data failures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
