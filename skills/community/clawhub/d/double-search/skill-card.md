## Description: <br>
双搜索功能 (Tavily + Kimi) - 支持并行搜索和结果合并 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjs028-coder](https://clawhub.ai/user/wjs028-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run parallel web searches through Tavily and Kimi/Moonshot, then combine per-source results into a single response for research, content creation, market analysis, and technical lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily and Moonshot/Kimi external services. <br>
Mitigation: Use only with provider-approved data and avoid submitting secrets, private internal text, regulated data, or personal information as queries. <br>
Risk: The installer can print partial API key prefixes and run a networked test query. <br>
Mitigation: Review install.sh before execution and run it only in an environment where partial key prefixes and test traffic are acceptable. <br>
Risk: The skill depends on API keys and third-party service availability. <br>
Mitigation: Configure TAVILY_API_KEY and, when needed, KIMI_API_KEY through trusted secret handling and expect reduced functionality if a provider fails or is unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wjs028-coder/double-search) <br>
- [Publisher profile](https://clawhub.ai/user/wjs028-coder) <br>
- [Tavily API endpoint](https://api.tavily.com/search) <br>
- [Tavily API key setup](https://app.tavily.com/) <br>
- [Moonshot/Kimi API](https://api.moonshot.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionaries containing query, merged_results, and source_breakdown fields, plus console text and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and optionally KIMI_API_KEY; sends search queries to external Tavily and Moonshot/Kimi APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
