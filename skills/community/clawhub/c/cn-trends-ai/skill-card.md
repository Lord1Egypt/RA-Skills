## Description: <br>
Fetches real-time public trending topics from Zhihu, Weibo, Baidu, and Bilibili. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and filter current Chinese platform trends for monitoring, topic discovery, or content planning. It can return a readable report or JSON for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Zhihu, Weibo, Baidu, and Bilibili, and those services may rate-limit requests or change their public APIs. <br>
Mitigation: Use in an environment where those outbound requests are allowed, handle empty or failed fetches, and review behavior after platform API changes. <br>
Risk: The script depends on the certifi Python package for certificate validation. <br>
Mitigation: Install certifi from a trusted package source and keep the runtime dependency reviewed with normal dependency management. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freedompixels/cn-trends-ai) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text trend report or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trend items include title, platform, heat, URL, category, and excerpt when available.] <br>

## Skill Version(s): <br>
1.3.2 (source: server-resolved release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
