## Description:

Retrieve astronomy and astrophysics papers from the user's arXiv mirror API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqqian](https://clawhub.ai/user/zqqian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and astronomy researchers use this skill to discover, recommend, and inspect astronomy and astrophysics papers by arXiv update date, topic, similar paper, or arXiv ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Astronomy search terms, dates, and arXiv IDs may be sent to a third-party arXiv mirror.

Mitigation: Use the skill only when sharing those paper-discovery queries with the disclosed mirror is acceptable.

Risk: The mirror API may be unavailable, return unexpected shapes, or omit paper metadata.

Mitigation: State API failures or missing metadata directly and fall back to structured or official paper sources before generic web search.

## Reference(s):

- [API Reference](references/api.md)
- [Astro arXiv Search on ClawHub](https://clawhub.ai/zqqian/skills/astro-arxiv-search)
- [arXiv mirror day listing endpoint](https://arxiv.q-cs.cn/ai/by-date?date={YYYY-MM-DD}&only_title=true)
- [arXiv mirror recommendation endpoint](https://arxiv.q-cs.cn/ai/recommend?topic={topic}&period={int}&date={YYYY-MM-DD}&limit={30})

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with paper lists, summaries, dates, arXiv IDs, categories, and source metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a third-party arXiv mirror as the primary source and falls back to other available search methods only when needed.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
