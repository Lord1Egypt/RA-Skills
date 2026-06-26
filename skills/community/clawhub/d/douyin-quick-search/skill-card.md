## Description: <br>
Searches Douyin (抖音) content by natural language keyword, including video search, trending topics, and video detail extraction via web search and page fetching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content researchers, social media managers, and agents use this skill to discover Douyin videos, review trending topics, and summarize metadata from specific Douyin video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and provided Douyin URLs may be sent through external web search and page-fetching services. <br>
Mitigation: Use non-sensitive search terms and do not provide Douyin cookies, passwords, private account links, or other sensitive information. <br>
Risk: Douyin CAPTCHA, authentication gates, and search engine coverage can make results incomplete, stale, or limited to indexed metadata. <br>
Mitigation: Treat results as discovery leads, verify important content directly on Douyin, and retry with shorter or Chinese-language keywords when needed. <br>
Risk: The artifact README install command uses a different slug than the published release. <br>
Mitigation: Install the published ClawHub release using the slug douyin-quick-search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-quick-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the search keyword, result count, titles, descriptions when available, and links to discovered Douyin content.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
