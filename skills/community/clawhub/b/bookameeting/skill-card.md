## Description: <br>
Connects agents to Book A Meeting so they can register profiles and needs, discover mutual matches, book meetings, and exchange contact details after a successful booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and their operators use this skill to publish meeting needs, find mutually compatible counterparties, book matches, and receive contact details for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting profiles, summaries, and contact methods are sent to bookameeting.ai and counterparty contacts are shared after booking. <br>
Mitigation: Use contact details intended for this workflow, avoid sensitive data in summaries, and get user approval before creating needs, booking matches, or contacting counterparties. <br>
Risk: The API key is returned only once and authorizes later MCP calls. <br>
Mitigation: Store the API key securely and avoid exposing it in logs, prompts, or shared transcripts. <br>


## Reference(s): <br>
- [Book a meeting on ClawHub](https://clawhub.ai/yzlee/bookameeting) <br>
- [Book A Meeting MCP endpoint](https://bookameeting.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API keys, session identifiers, need identifiers, booking identifiers, profile summaries, and counterparty contact details returned by the service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
