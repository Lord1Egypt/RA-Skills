## Description: <br>
Helps agents answer Chinese government-service and public-policy questions by retrieving traceable policy files, service items, government website results, Q&A knowledge, and knowledge-base links through Dknowc trusted search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanzhangzx](https://clawhub.ai/user/dylanzhangzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer government-service, public-benefit, social-security, housing-fund, certificate, subsidy, policy-applicability, procedure, material-list, online-entry, and official-basis questions. It retrieves source materials first, then guides the agent to produce concise, actionable answers with fielded references. <br>

### Deployment Geography for Use: <br>
China; defaults to Shenzhen when the user does not specify a location, and uses the user's stated city or province when provided. <br>

## Known Risks and Mitigations: <br>
Risk: A configured or command-line endpoint can receive the user's API key and query. <br>
Mitigation: Keep the endpoint set to the official Dknowc URL unless the user controls and trusts the replacement server. <br>
Risk: Government-service answers can use the default Shenzhen area when a user intends another location but does not state it. <br>
Mitigation: Ask for or explicitly include the city or province for policy questions outside Shenzhen. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dylanzhangzx/dknowc-gov-zhicha-public) <br>
- [Dknowc API key platform](https://platform.dknowc.cn) <br>
- [Dknowc trusted search endpoint](https://open.dknowc.cn/dependable/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text or JSON materials package, with final answers as Markdown-compatible text and fielded source references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a user-provided Dknowc API key; default area is Shenzhen.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, artifact _meta.json, CHANGE_log.md released 2026-06-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
