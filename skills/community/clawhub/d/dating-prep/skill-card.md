## Description:

Pre-date research assistant that scans public social media profiles to produce a Dating Prep Report with interest mapping, personality-style observations, conversation topics, restaurant or activity suggestions, and caution notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill before a date or matchmaking meeting to summarize a person's public social profile signals into practical preparation guidance, including interests, likely conversation topics, date venue ideas, and cautions about overinterpreting public posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation access can expose logged-in account context or page data beyond the intended public-profile scope.

Mitigation: Use only explicit target profile URLs, avoid private tabs or account-only views, and validate the ManoBrowser endpoint before providing credentials.

Risk: The skill stores raw profile data locally, which can retain sensitive personal information from public social media pages.

Mitigation: Store only the minimum data needed for the report, prefer summaries when possible, and provide deletion controls for local profile captures and reports.

Risk: Profile-derived personality or compatibility observations can be misleading if treated as facts.

Mitigation: Label conclusions as limited inferences from public content and use the report as conversation preparation rather than a basis for definitive judgments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sophie-xin9/skills/dating-prep)
- [Publisher Profile](https://clawhub.ai/user/sophie-xin9)
- [ManoBrowser Dependency](https://github.com/ClawCap/ManoBrowser)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown report with structured sections and occasional inline shell commands for setup checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON profile captures and a local Markdown dating preparation report when executed with browser automation access.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
