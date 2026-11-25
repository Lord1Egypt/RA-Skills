## Description:

Analyzes a post’s comment section to summarize praise, complaints, questions, buying intent, and reusable customer quotes, with an optional CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and product teams use the skill to understand audience reactions to a specific post and turn comments into a CSV table and a language-matched report for copy, FAQs, or product briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the DataXAPI CLI without a pinned version may expose the environment to later package changes.

Mitigation: Pin a reviewed package version and check its source before installation.

Risk: The security scan could not resolve several local path-like references, so those references were not assessed.

Mitigation: Review unresolved references and inspect the skill before running it.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-comment-analysis)

## Skill Output:

**Output Type(s):** [CSV file, Markdown report, Text analysis]

**Output Format:** [CSV table and a Markdown comment report in the user’s language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CSV has one row per returned comment; unavailable platform fields are left empty. The report groups praise, complaints, questions, buying intent, and reusable quotes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
