## Description: <br>
Retrieves astronomy and astrophysics papers from the user's arXiv mirror API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqqian](https://clawhub.ai/user/zqqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to retrieve astronomy papers by date, topic, similar arXiv ID, or specific arXiv ID, then present concise researcher-facing lists and summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Astronomy paper searches are routed through a disclosed external arXiv mirror API. <br>
Mitigation: Avoid private or sensitive research queries unless the user trusts that external service. <br>
Risk: The external API may be unavailable, incomplete, or unable to answer a requested astronomy lookup. <br>
Mitigation: Use structured or official paper sources as a fallback and clearly state when the answer is based on a fallback source. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/zqqian/astro-arxiv-search) <br>
- [arXiv mirror by-date endpoint](https://arxiv.q-cs.cn/ai/by-date?date={YYYY-MM-DD}&only_title=true) <br>
- [arXiv mirror recommendation endpoint](https://arxiv.q-cs.cn/ai/recommend?topic={topic}&period={int}&date={YYYY-MM-DD}&limit={30}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown with paper metadata, API-derived summaries, and concise retrieval notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses arXiv IDs, dates, topics, periods, categories, and similarity scores when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
