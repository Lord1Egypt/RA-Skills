## Description:

Extracts real-time stock-positive market news from Cailian Press (CLS), filtered by time window, sector, and event type for catalyst identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningjingzhiyuande](https://clawhub.ai/user/ningjingzhiyuande)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to collect Cailian Press market-news items and structure likely positive stock catalysts for downstream research and scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured CLS endpoint or source may be unclear before installation.

Mitigation: Confirm the endpoint or source the skill will use before installing or running it.

Risk: Catalyst classifications may be mistaken for financial advice.

Mitigation: Treat catalyst output as research input and review source URLs, timestamps, and confidence before downstream scoring or decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningjingzhiyuande/skills/cls-news-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table or structured rows containing ticker, company, catalyst, source URL, timestamp, and confidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filtered by time window, sector, and event type; catalyst output should be treated as research input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
