## Description:

Generates a structured Simplified Chinese AI news daily brief by collecting, deduplicating, classifying, and summarizing recent AI news from approved sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyieleven](https://clawhub.ai/user/wangyieleven)

### License/Terms of Use:

MIT-0

## Use Case:

AI product managers, industry researchers, strategy teams, and enterprise AI practitioners use this skill to produce a concise daily brief tracking important AI industry developments across approved sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled publishing can write to hard-coded Tencent Docs destinations without enough user control.

Mitigation: Use the scheduled publishing path only when the destination documents and account credentials are controlled, previewed, audited, and easy to disable; otherwise run the skill on demand and return the brief in the current session.

## Reference(s):

- [README](README.md)
- [Source Whitelist](references/sources.md)
- [Search Rules and Deduplication Rules](references/search-rules.md)
- [Output Template](references/output-template.md)
- [Category Taxonomy](references/category-taxonomy.md)
- [Validation Checklist](references/validation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Simplified Chinese Markdown daily brief with ranked news items, categories, summaries, source links, and takeaways.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to the last 24 hours and an approved source whitelist; item count depends on verified source availability.]

## Skill Version(s):

1.0.3 (source: server release metadata, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
