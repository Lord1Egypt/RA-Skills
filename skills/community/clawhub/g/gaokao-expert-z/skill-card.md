## Description: <br>
提供高考志愿相关工具，获取学校和专业以往的录取分数线，提供推荐信息等。注意：往年的数据都是真实数据，当前2026年的数据还未发布，为提前获得完整体验，暂时基于2025年数据虚拟了一份，后面会及时更新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, families, counselors, and admissions-advice agents use this skill to query Chinese Gaokao admission scores, school and major information, enrollment plans, rank conversion, and admission-probability guidance through the Xiaobenyang service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Xiaobenyang API key in a local .env file. <br>
Mitigation: Use a dedicated API key, keep the .env file private, and avoid committing or sharing it. <br>
Risk: Gaokao scores, province, school, major, and preference inputs are sent to mcp.xiaobenyang.com. <br>
Mitigation: Use the skill only when sharing these admissions inputs with the provider API is acceptable. <br>
Risk: The artifact states that 2026 data is temporarily simulated from 2025 data until official 2026 data is available. <br>
Mitigation: Treat 2026 results as provisional and verify important admissions decisions against official school or examination-authority sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cainingnk/gaokao-expert-z) <br>
- [Xiaobenyang API Key Site](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API Endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiaobenyang API key and user-provided admissions query parameters such as province, score, school, major, category, and year.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
