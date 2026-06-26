## Description: <br>
中文AI Agent专用多平台聚合搜索工具，开箱即用，国内网络友好。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niukesi](https://clawhub.ai/user/niukesi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to collect Chinese web search results across multiple platforms and return deduplicated results for research, market analysis, competitive analysis, and news tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to external search engines and Jina Reader. <br>
Mitigation: Avoid sensitive, proprietary, or regulated queries and disclose external query routing to users before deployment. <br>
Risk: The artifact includes embedded API keys that should be treated as unsafe shared credentials. <br>
Mitigation: Replace bundled keys with environment-managed credentials or remove them before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niukesi/cn-ai-search) <br>
- [Publisher profile](https://clawhub.ai/user/niukesi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text search results with titles, URLs, sources, and abstracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result count, per-platform count, platform selection, sort order, and output format are configurable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
