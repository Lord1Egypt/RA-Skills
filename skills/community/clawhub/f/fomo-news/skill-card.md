## Description: <br>
Real-time news aggregation skill that fetches trending GitHub repos, social posts from key tech/AI figures, and breaking news from major outlets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yealexchen](https://clawhub.ai/user/yealexchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CLI users use this skill to fetch current GitHub trends, technology and AI updates, economics and politics headlines, and social or blog updates without leaving the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public news, RSS, blog, Google News, and GitHub endpoints during normal use. <br>
Mitigation: Install only where those outbound requests are acceptable and review the configured sources for the intended environment. <br>
Risk: A GitHub token may be provided for higher rate limits. <br>
Mitigation: Use a low-scope token because public repository search does not require broad permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yealexchen/fomo-news) <br>
- [GitHub Trending](references/github.md) <br>
- [Breaking News](references/news.md) <br>
- [Social Posts](references/social.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands] <br>
**Output Format:** [Markdown summaries with clickable links, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; optional GITHUB_TOKEN can increase GitHub API rate limits.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
