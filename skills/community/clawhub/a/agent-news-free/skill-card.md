## Description: <br>
A free AI-enriched global news stream for agents, provided by agentnewsapi.com and powered by $ANA on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentnewsdev](https://clawhub.ai/user/agentnewsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to fetch delayed, structured global news signals for monitoring events, categories, and sentiment. It is suited for workflows that can tolerate free-tier limits and independently verify returned news content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to agentnewsapi.com and returned news data may be incomplete, delayed, or unsuitable as authoritative advice. <br>
Mitigation: Use non-sensitive queries and corroborate returned stories before relying on them for financial, operational, or news decisions. <br>
Risk: Free-tier access is delayed and rate-limited, which can affect time-sensitive agent workflows. <br>
Mitigation: Design workflows to tolerate the 20-minute delay, 1 request per minute rate limit, and 100-story maximum. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/agentnewsdev/agent-news-free) <br>
- [Agent News API homepage](https://agentnewsapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON emitted by a Node.js CLI, with usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free-tier responses are delayed by 20 minutes, rate-limited to 1 request per minute, and capped at 100 stories per request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and package.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
