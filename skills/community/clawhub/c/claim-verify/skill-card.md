## Description: <br>
Verifies factual claims such as rates, prices, dates, and statistics against live data before an agent relies on them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to check current factual claims before using them in responses, calculations, reports, or recommendations. It is intended for public, non-sensitive claims where live verification improves accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claim text may be sent to an external verification service. <br>
Mitigation: Use only for public factual claims; do not submit confidential business facts, personal data, regulated information, secrets, or internal claims unless that data sharing has been separately approved. <br>


## Reference(s): <br>
- [Verify Agent Homepage](https://verify.agentutil.net) <br>
- [Verify Agent Card](https://verify.agentutil.net/.well-known/agent.json) <br>
- [Verify Agent Service Metadata](https://verify.agentutil.net/.well-known/agent-service.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with JSON verdict examples and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an MCP verifier or an external HTTP verification service; the documented free tier is limited to 25 queries per day.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
