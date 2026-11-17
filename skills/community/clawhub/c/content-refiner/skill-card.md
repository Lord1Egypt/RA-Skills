## Description: <br>
Content Refiner rewrites Chinese content for eight publishing platforms using local synonym-and-structure changes or an optional LLM mode with SimHash similarity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, marketers, and social media operators use this skill to adapt Chinese source text into platform-specific rewrites for Zhihu, Xiaohongshu, Douyin, Weibo, technical communities, CSDN, Bilibili, and ecommerce listings. The skill is intended for expression and style rewriting, not factual correction or original research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and includes connectivity troubleshooting guidance that may be broader than needed for content rewriting. <br>
Mitigation: Review before installing in agents with shell access, and disable or remove exec and network troubleshooting behavior unless it is explicitly required. <br>
Risk: LLM mode may send sensitive or proprietary input text to a configured model provider. <br>
Mitigation: Use local mode for sensitive content, and use LLM mode only when the data handling terms of the configured provider are acceptable. <br>
Risk: The skill rewrites expression but does not fact-check or correct the source material. <br>
Mitigation: Review rewritten outputs for factual accuracy, claims, and platform compliance before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-refiner) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-style structured text describing rewritten content, warnings, and change summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include original and rewritten text, target platform, selected mode, originality score, SimHash distance, error code, and change summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
