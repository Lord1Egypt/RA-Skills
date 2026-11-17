## Description:

AI phone agent for any business that answers inbound calls, captures leads, books appointments, and returns structured call data with transcripts, summaries, and sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanhall00](https://clawhub.ai/user/ryanhall00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add inbound phone handling, lead capture, appointment booking, and call analytics to agent workflows through the AgentIzzy API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses sensitive call recordings, transcripts, caller contact details, and lead data through AgentIzzy.

Mitigation: Install only where AgentIzzy is trusted for this data, protect AGENTIZZY_API_KEY, and confirm privacy or compliance requirements before use.

Risk: The skill can register accounts, configure webhooks, provision phone numbers, and start billing checkout flows.

Mitigation: Require explicit human approval before account creation, webhook configuration, phone-number provisioning, or checkout actions.

Risk: The security guidance warns against passing untrusted values into helper scripts until JSON and URL construction are hardened.

Mitigation: Use trusted inputs for script arguments or review and harden argument handling before exposing the scripts to untrusted values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanhall00/skills/agentizzy-phone-agent)
- [AgentIzzy API registration endpoint](https://api.agentizzy.com/api/v1/register)
- [AgentIzzy agents endpoint](https://api.agentizzy.com/api/v1/agents)

## Skill Output:

**Output Type(s):** [shell commands, configuration, json, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTIZZY_API_KEY for authenticated API calls and uses curl plus python3 in the bundled helper scripts.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
