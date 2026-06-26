## Description: <br>
Helps agents perform lightweight, compliant analysis of publicly visible Douyin videos, author pages, keyword searches, and trending lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to manually review public Douyin pages and summarize visible engagement, timing, and topic patterns for internal analysis and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be used on login-only or restricted content. <br>
Mitigation: Use it only with publicly visible Douyin pages and avoid content that requires authentication or special access. <br>
Risk: Automated or high-volume collection could conflict with platform controls or terms. <br>
Mitigation: Keep use manual and lightweight, respect rate limits, and do not attempt to bypass anti-bot or human-verification controls. <br>
Risk: Users may try to repurpose the workflow for downloads, watermark removal, or interface bypass. <br>
Mitigation: Limit the skill to summaries and visible metric analysis; do not use it for downloads, watermark removal, reverse engineering, or direct interface calls. <br>


## Reference(s): <br>
- [Douyin homepage](https://www.douyin.com/) <br>
- [Douyin trending lists](https://www.douyin.com/discover) <br>
- [Douyin search](https://www.douyin.com/search) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/douyin-trends) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and step-by-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public engagement metrics, links, topic labels, and trend summaries when those fields are visible on public pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
