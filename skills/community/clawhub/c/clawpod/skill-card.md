## Description: <br>
Read any website or search Google, even when sites block bots or are geo-restricted. Handles CAPTCHAs, JavaScript rendering, and anti-bot protection server-side via residential proxies. Returns HTML or structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Clawpod to fetch rendered page content or Google search results when standard fetch or search tools are blocked, incomplete, geo-restricted, or require JavaScript rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may send URLs, search terms, and fetched content to Massive's Unblocker service. <br>
Mitigation: Avoid secrets, private or internal URLs, credential-bearing links, and regulated data unless the provider's terms, logging, and retention practices are acceptable. <br>
Risk: The skill can be used to bypass anti-bot protections, CAPTCHAs, paywalls, or geo-restrictions. <br>
Mitigation: Use it only where authorized and consistent with applicable site terms, laws, and organizational scraping policies. <br>


## Reference(s): <br>
- [Clawpod homepage](https://clawpod.joinmassive.com) <br>
- [ClawHub skill page](https://clawhub.ai/codeninja23/clawpod) <br>
- [README](README.md) <br>
- [OpenClaw skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and returned HTML or JSON from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MASSIVE_UNBLOCKER_TOKEN; search output can be HTML or structured JSON.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
