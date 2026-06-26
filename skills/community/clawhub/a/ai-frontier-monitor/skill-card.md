## Description: <br>
AI frontier intelligence briefing - aggregate, score, and deliver structured daily briefings from 5 tracks: RSS enterprise, 36kr hotlist, arXiv papers, GitHub Trending, and Anthropic web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lynxpurr](https://clawhub.ai/user/lynxpurr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to collect public AI news, papers, repositories, and market signals, score them, and produce concise Chinese-language frontier briefings for daily monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local scripts and contacts public web sources while generating briefings. <br>
Mitigation: Invoke it explicitly for AI briefing tasks and expect outbound requests to the configured public data sources. <br>
Risk: Generated reports may be sent to Feishu. <br>
Mitigation: Review the Feishu recipient configuration before enabling delivery. <br>
Risk: Runtime candidate data and generated briefings are saved under the skill directory. <br>
Mitigation: Review saved files periodically and avoid placing sensitive non-public inputs in briefing candidates. <br>


## Reference(s): <br>
- [Briefing Configuration](references/BRIEFING_CONFIG.md) <br>
- [Data Sources](references/data-sources.md) <br>
- [Scoring System](references/scoring.md) <br>
- [ClawHub Release Page](https://clawhub.ai/lynxpurr/ai-frontier-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown briefing text with optional saved Markdown files and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first briefings, tiered sections, signal summaries, source links, and optional Feishu delivery.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
