## Description:

AI Daily News generates a daily AI news brief covering significant Chinese and international AI stories from the past 24 hours, with titles, recommendation rationale, scores, summaries, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[george351419-sys](https://clawhub.ai/user/george351419-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to request or receive a daily AI news brief about recent AI industry developments. The brief helps readers scan important AI stories with recommendation rationale, a 1-10 score, concise summaries, and original source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on live web search and external article pages, so retrieved source content can be incomplete, stale, or misleading.

Mitigation: Prioritize authoritative sources, retain original links, and review important items before using the brief for decisions.

Risk: The evidence notes that exact scheduled trigger behavior is not explicitly documented.

Mitigation: Confirm the scheduler behavior in the deployment environment before relying on unattended daily delivery.

Risk: The evidence notes that the skill does not explicitly document a language option.

Mitigation: Set the desired output language in the user request or deployment wrapper when a specific language is required.

## Reference(s):

- [AI news source reference](references/news_sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each item includes a title, recommendation rationale, 1-10 score, concise summary, and original link.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
