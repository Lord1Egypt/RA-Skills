## Description: <br>
AgentZero helps an agent use a local real estate listing tracker to add or refresh property listings, scan opted-in Redfin alert emails, triage listings with Claude, and log outcomes for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzhong52](https://clawhub.ai/user/yzhong52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate AgentZero as a local property-search assistant: it adds listing URLs, scans opted-in Redfin emails, tracks listing status, and surfaces matched properties for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Gmail-assisted browsing and email metadata during the opted-in Redfin alert workflow. <br>
Mitigation: Use only with explicit user consent, confirm the himalaya Gmail configuration, and verify that scanning stays scoped to Redfin alert emails. <br>
Risk: The skill controls local services and may stop processes on ports 8000 or 5173 when starting its backend or frontend. <br>
Mitigation: Review the start scripts before running them and avoid using the skill where unrelated services are bound to those ports. <br>
Risk: The skill keeps persistent local listing data, processed email state, HTML snapshots, and service logs. <br>
Mitigation: Run it in an appropriate local workspace, review retention expectations, and remove local artifacts when they are no longer needed. <br>
Risk: The security summary flags under-disclosed live anti-bot browser fetching behavior for some real estate sites. <br>
Mitigation: Treat Zillow and Realtor.ca behavior as live browser fetching, confirm it is acceptable for the deployment, and monitor use against site and organizational policies. <br>


## Reference(s): <br>
- [AgentZero ClawHub page](https://clawhub.ai/yzhong52/agent-zero) <br>
- [Publisher profile](https://clawhub.ai/user/yzhong52) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Anthropic Console](https://console.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON API payloads, and local log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local daily logs, processed email state, listing data, HTML snapshots, and service logs.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
