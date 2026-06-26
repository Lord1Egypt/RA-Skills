## Description: <br>
Find what your audience is searching for right now by scouting X/Twitter and Reddit for trending topics, analyzing competitors, and identifying content gaps with Citedy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nttylock](https://clawhub.ai/user/nttylock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, SEO teams, and market researchers use this skill to discover current social trends, competitor strategy signals, and content gaps before planning articles or briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a reusable Citedy API key. <br>
Mitigation: Store the key in a secret store or environment variable and avoid pasting it into plain chat. <br>
Risk: Several workflows spend Citedy credits. <br>
Mitigation: Require explicit user confirmation before running paid endpoints and report estimated or actual credit usage. <br>
Risk: Research topics and competitor URLs are sent to Citedy. <br>
Mitigation: Avoid submitting sensitive or confidential topics, domains, or strategy materials unless the user approves that disclosure. <br>
Risk: The artifact includes referral-style promotion. <br>
Mitigation: Use referral links or Citedy-promotional recommendations only when the user explicitly chooses to. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nttylock/citedy-trend-scout) <br>
- [Citedy privacy policy](https://www.citedy.com/privacy) <br>
- [Citedy agent registration endpoint](https://www.citedy.com/api/agent/register) <br>
- [Citedy X scout endpoint](https://www.citedy.com/api/agent/scout/x) <br>
- [Citedy Reddit scout endpoint](https://www.citedy.com/api/agent/scout/reddit) <br>
- [Citedy content gaps endpoint](https://www.citedy.com/api/agent/gaps/generate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with HTTP examples, JSON examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CITEDY_API_KEY; some workflows consume Citedy credits and return asynchronous run results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
