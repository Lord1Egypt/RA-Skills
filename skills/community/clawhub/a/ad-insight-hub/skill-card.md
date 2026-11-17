## Description: <br>
广告洞察中枢 helps agents translate advertising intelligence requests into AdMapix API calls, orchestrate dependent endpoints, cache reusable results, and label estimated download or revenue data with confidence levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advertising, user acquisition, and market analysis teams use this skill to retrieve structured AdMapix data for competitor creative monitoring, app and developer profiling, store rankings, SDK review, and regional strategy comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses curl/exec access and an ADMAPIX_API_KEY environment variable to call a remote advertising intelligence API. <br>
Mitigation: Install only when AdMapix access is intended, keep the key in the environment, avoid echoing or storing the value, and send it only as the X-API-Key request header. <br>
Risk: Local caches under ~/.admapix-cache may retain advertising intelligence data that could be sensitive. <br>
Mitigation: Review cache contents periodically, use explicit export paths, and delete retained cache data when it is no longer needed. <br>
Risk: Download and revenue data are third-party estimates and may be unsuitable for precise financial decisions. <br>
Mitigation: Use the skill's A/B/C confidence labels and treat lower-confidence or long-tail estimates as directional signals only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ad-insight-hub) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [AdMapix website](https://www.admapix.com) <br>
- [AdMapix API base](https://api.admapix.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include raw structured AdMapix JSON, endpoint orchestration steps, cache guidance, and confidence labels for third-party estimates.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
