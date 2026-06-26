## Description: <br>
Searches Douyin videos by natural-language keywords and returns video results or related keyword suggestions when login is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and other users can ask an agent to search public Douyin videos from natural-language requests and receive video result summaries or suggested search terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use browser automation with saved Douyin session state, including a broader OpenClaw profile fallback. <br>
Mitigation: Use a dedicated browser profile for this skill, remove or disable the broader profile fallback before deployment, and do not share or commit the profile directory. <br>
Risk: Douyin browser automation may fail, require login, or be rate-limited as platform controls change. <br>
Mitigation: Prefer the documented suggestion fallback when login is unavailable, avoid repeated high-volume searches, and review results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-search) <br>
- [Douyin](https://www.douyin.com/) <br>
- [README](README.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries with optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Douyin video URLs, authors, engagement metrics, login prompts, or keyword suggestions.] <br>

## Skill Version(s): <br>
2026.5.10 (source: server release metadata; artifact skill version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
