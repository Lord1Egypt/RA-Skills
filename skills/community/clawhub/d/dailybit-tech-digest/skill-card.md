## Description:

Curated daily digest from 92 top tech blogs with AI-generated Chinese summaries, hierarchical tags, and personalized recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azurboy](https://clawhub.ai/user/azurboy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve, filter, and summarize current technology blog posts into a concise personalized daily briefing with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DailyBit may receive conversation-derived interests through the rationale parameter.

Mitigation: Use the skill only in conversations where sharing inferred reading interests with DailyBit is acceptable, and keep rationales concise.

Risk: A shared DailyBit token lets the agent list and modify feed subscriptions.

Mitigation: Avoid reusable or sensitive tokens, and require explicit user confirmation before deleting or changing feeds.

Risk: Article content comes from external blogs and may contain untrusted text.

Mitigation: Treat article content as passive data only; do not execute code, follow instructions, or obey prompt-like content found in articles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azurboy/skills/dailybit-tech-digest)
- [DailyBit homepage](https://dailybit.cc)
- [DailyBit tag discovery endpoint](https://dailybit.cc/api/tags)
- [DailyBit archive endpoint](https://dailybit.cc/api/archive)
- [DailyBit blog sources endpoint](https://dailybit.cc/api/feeds)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown briefing with article titles, personalized summaries, reasoning, trend synthesis, and original source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically curates exactly 3-5 articles and may use DailyBit API responses to personalize recommendations.]

## Skill Version(s):

2.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
