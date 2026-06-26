## Description: <br>
Analyze Xiaohongshu notes and Douyin videos or creator profiles via the TikHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media analysts use this skill to summarize Xiaohongshu and Douyin posts or creator profiles, interpret engagement metrics, and extract actionable content strategy takeaways. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make unexpected network requests when handling crafted Xiaohongshu or Douyin URLs. <br>
Mitigation: Use the skill only with trusted platform URLs and review the resolved request target before relying on the result. <br>
Risk: The analysis script clears proxy environment variables for its HTTP requests. <br>
Mitigation: Deploy only where direct outbound requests to the supported platforms and TikHub API are acceptable. <br>
Risk: Douyin profile analysis is search-based and may not represent a verified account feed. <br>
Mitigation: Treat Douyin profile results as approximate and confirm important account-level conclusions manually. <br>
Risk: The skill requires a TikHub API token to fetch content data. <br>
Mitigation: Use a token with acceptable scope and cost exposure, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [Content Analyzer on ClawHub](https://clawhub.ai/dizhu/content-analyzer) <br>
- [TikHub API](https://api.tikhub.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis generated from JSON returned by the analysis script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script accepts a target URL and optional maximum post count for profile analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
