## Description: <br>
Extract real restaurant insights from Dianping reviews: filter noise, detect fake reviews, build personalized dining guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Dianping restaurant reviews, identify suspicious feedback, summarize genuine sentiment, rank restaurants against dining preferences, and produce dish-level ordering guides. <br>

### Deployment Geography for Use: <br>
Global, with practical coverage focused on mainland China where Dianping restaurant data is available. <br>

## Known Risks and Mitigations: <br>
Risk: The included CLI uses sample data rather than live Dianping access. <br>
Mitigation: Treat generated recommendations as examples unless the skill is connected to current, authorized review data. <br>
Risk: Adapting the skill for live scraping could create terms-of-service, rate-limit, or privacy issues. <br>
Mitigation: Keep collection read-only, avoid account credentials, respect Dianping rate limits and terms, and do not store precise location or reviewer data beyond the session. <br>
Risk: Fake-review and sentiment scores can be wrong or incomplete when review samples are sparse, stale, or biased. <br>
Mitigation: Show confidence warnings for limited data and use the results as dining guidance rather than authoritative claims about restaurants or reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/dianping-restaurant-guide) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Fake review detection signals](references/signals.json) <br>
- [Input schema](schemas/input.schema.json) <br>
- [Output schema](schemas/output.schema.json) <br>
- [OpenClaw input schema URI](https://openclaw.dev/skills/dianping-restaurant-guide/input.schema.json) <br>
- [OpenClaw output schema URI](https://openclaw.dev/skills/dianping-restaurant-guide/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON reports with restaurant rankings, authenticity findings, sentiment summaries, ordering guides, and route plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticity scores, suspicious-review signals, dining-profile rankings, dish recommendations, warnings, and budget estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
