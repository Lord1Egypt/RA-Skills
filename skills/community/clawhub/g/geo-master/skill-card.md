## Description: <br>
品牌AI可见性监控Skill，自动搜索Kimi、讯飞星火、文心一言、智谱等AI平台，检测品牌关键词可见性，生成0-100 GEM评分，分析未被推荐的原因，并支持飞书推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, growth, and GEO teams use this skill to check whether target brands appear across AI answer platforms, compare visibility signals, and generate a concise report with scoring and optimization guidance. Developers can also configure quota behavior, API keys, and optional Feishu delivery for operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand keywords, search results, and reports may be sent to third-party AI platforms, Tavily, or Feishu when configured. <br>
Mitigation: Use the skill only for data approved for those services, leave the Feishu webhook empty or run with --no-push unless delivery is intended, and review external data-sharing requirements before deployment. <br>
Risk: The artifact includes a hardcoded Tavily credential fallback. <br>
Mitigation: Remove the bundled fallback and require TAVILY_API_KEY to be supplied through a secret manager or environment variable before real deployment. <br>
Risk: The bundled API service pattern could expose brand-search functionality if deployed publicly. <br>
Mitigation: Keep the API service private, require strong authentication, and avoid exposing it directly to the public internet. <br>


## Reference(s): <br>
- [GEO Master ClawHub Listing](https://clawhub.ai/qiji0802/geo-master) <br>
- [Publisher Profile](https://clawhub.ai/user/qiji0802) <br>
- [YK-Global Website](https://yk-global.com) <br>
- [Tavily Search API Endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown reports, terminal status text, configuration guidance, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a 0-100 GEM visibility score, per-platform findings, excerpts when available, and optimization guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
