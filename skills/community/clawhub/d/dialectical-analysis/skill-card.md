## Description: <br>
辩证分析 uses pro, con, and arbitrator agent roles to generate multilingual business feasibility analysis through structured debate, optional knowledge search, and multi-dimensional scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philonis](https://clawhub.ai/user/philonis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, business analysts, and strategy teams use this skill to evaluate business decisions by staging constructive and critical debate, summarizing consensus and disagreement, and producing actionable recommendations. It is suited to market-entry, product, finance, legal, and operational feasibility questions where assumptions need to be challenged. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business topics and constraints may be sent to Tavily, Brave, or DuckDuckGo when knowledge search is enabled. <br>
Mitigation: Use only topics suitable for external search providers, disable or modify search for confidential work, and use dedicated API keys. <br>
Risk: Generated local workspace files may retain sensitive strategy, finance, market-entry, or client information. <br>
Mitigation: Periodically delete generated workspace files when retention matters and review the skill before use on confidential analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/philonis/dialectical-analysis) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Multi-dimensional analysis framework](artifact/prompts/multi_dimensional.md) <br>
- [V2 report template](artifact/templates/v2_report.md) <br>
- [Tavily Search API](https://tavily.com) <br>
- [Brave Search API](https://brave.com/search/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured JSON debate records, and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs match the user's input language and may create local workspace files for debate state, agent rounds, arbitrator summaries, and final reports.] <br>

## Skill Version(s): <br>
3.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
