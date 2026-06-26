## Description: <br>
AI情报哨兵 - 自动采集、分析与报告AI领域最新动态的多源情报系统 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaopengs](https://clawhub.ai/user/xiaopengs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, AI researchers, product teams, investors, and content creators use this skill to collect AI-domain updates from public sources, score and organize them, and generate structured morning, evening, or social-style reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts configured public news, RSS, GitHub, arXiv, HackerNews, Twitter/X, and website sources. <br>
Mitigation: Review config/sources.yaml before use and run the skill only in environments where outbound requests to those sources are acceptable. <br>
Risk: Twitter/X support may require a bearer token, and the WebUI can persist settings in browser localStorage. <br>
Mitigation: Use a low-privilege or throwaway token, avoid saving sensitive tokens in shared browser origins, and rotate or delete the token if exposure is possible. <br>
Risk: Generated reports summarize third-party content and may include stale, incomplete, or incorrect claims from source feeds. <br>
Mitigation: Review high-impact report items against their linked original sources before using them for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xiaopengs/ai-sentinel-2) <br>
- [API配置指南](artifact/references/api_setup.md) <br>
- [信息源添加指南](artifact/references/sources_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with command-line and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated report files under reports/YYYY-MM-DD/ and can use a local WebUI for source and settings management.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
