## Description: <br>
Provides Chinese web and AI search through the Bocha API via the Whalecloud gateway for fact checking, source-backed answers, and current Chinese internet information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littlewangupup](https://clawhub.ai/user/littlewangupup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Chinese-language web or AI search from an agent, gather source-backed results, and support current-information answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the Whalecloud/Bocha search service. <br>
Mitigation: Avoid confidential queries unless that provider relationship is acceptable for the user or organization. <br>
Risk: The skill requires a Whalecloud token for search access. <br>
Mitigation: Use a scoped or dedicated token when available and do not print, log, or share WHALECLOUD_API_KEY. <br>


## Reference(s): <br>
- [Bocha API detailed specification](references/api-spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/littlewangupup/bocha-web-search-whalecloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results and Markdown guidance with citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHALECLOUD_API_KEY and sends search queries to the Whalecloud/Bocha search service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
