## Description: <br>
Generates structured Chinese news briefings for local, national, global, or industry topics using scale-specific public web and social sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shine8592](https://clawhub.ai/user/shine8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users can request street-level, city, national, international, or industry briefings with source labels, headline commentary, topic sections, optional data tables, and action suggestions. The skill is suited for concise situational awareness rather than newsletter operations or email distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web and social sources may be incomplete, stale, low quality, or contain prompt-injection content. <br>
Mitigation: Verify important claims against cited sources and ignore instructions embedded in fetched pages or search results. <br>
Risk: Very local community briefings may surface privacy-sensitive details. <br>
Mitigation: Keep coverage at an appropriate community or policy level and avoid publishing personal data unless it is clearly public, necessary, and relevant. <br>
Risk: Generic Chinese news or briefing requests may activate the skill broadly. <br>
Mitigation: Confirm the requested geography, industry, timeframe, and audience before generating a briefing. <br>


## Reference(s): <br>
- [Search Templates](references/search-templates.md) <br>
- [Source Library](references/source-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown briefing with source labels, headline commentary, categorized highlights, optional data table, and prioritized action suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for 800-2500 Chinese characters with source attribution for each item.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and README version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
