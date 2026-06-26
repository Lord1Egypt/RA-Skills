## Description: <br>
Aggregates current Chinese hot-trend lists from Zhihu, Weibo, Baidu, Bilibili, Douyin, and Toutiao, then outputs ranked reports, JSON data, and content topic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agents use this skill to fetch public Chinese trend lists across six platforms, compare hot topics, export JSON, and draft content angles from current trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public trend platforms when invoked. <br>
Mitigation: Install it only in environments where outbound requests to Zhihu, Weibo, Baidu, Bilibili, Douyin, and Toutiao are acceptable, and review network policy before deployment. <br>
Risk: Generic trigger phrases such as “热点” or “趋势” may activate the skill more often than intended. <br>
Mitigation: Narrow local trigger phrases or require an explicit platform or command phrase in workflows where accidental invocation would be disruptive. <br>
Risk: Live platform APIs can be unavailable, region-limited, or change response formats. <br>
Mitigation: Treat missing platform results as expected operational degradation and verify trend-sensitive outputs before publication or business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-hot-trends-6) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text trend report by default, optional JSON array, and Markdown-oriented topic recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on live public platform endpoints and may skip platforms that are unavailable or region-limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
