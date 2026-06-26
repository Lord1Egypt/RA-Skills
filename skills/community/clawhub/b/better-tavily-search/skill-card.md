## Description: <br>
Better Tavily Search helps agents retrieve fresh web evidence through Tavily for source finding, link discovery, official documentation lookup, current-event verification, and related external retrieval tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soymilkwinsagain](https://clawhub.ai/user/soymilkwinsagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and run compact Tavily searches, targeted extraction, and documentation site mapping when answers require fresh external sources or official web evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, extraction targets, and mapping targets are sent to Tavily or a Tavily-compatible endpoint. <br>
Mitigation: Use the skill only when that disclosure is acceptable, avoid confidential terms and internal URLs, and configure a limited Tavily API key. <br>
Risk: The skill can load credentials from the environment or ~/.openclaw/.env. <br>
Mitigation: Keep ~/.openclaw/.env private and avoid sharing logs, prompts, or command output that could reveal TAVILY_API_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soymilkwinsagain/better-tavily-search) <br>
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [Query Playbook](reference/query_playbook.md) <br>
- [Escalation Rules](reference/escalation_rules.md) <br>
- [Output Contract](reference/output_contract.md) <br>
- [Parameter Matrix](reference/param_matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Agent-oriented JSON, raw Tavily-style JSON, Markdown, or Brave-compatible result lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves query parameters, source URLs, snippets or chunks, domains, scores, usage metadata, response timing, and request identifiers when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
