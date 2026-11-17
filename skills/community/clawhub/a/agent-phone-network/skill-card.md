## Description:

Agent Phone Network helps agents place, answer, reject, end, and route agent-to-agent calls over the OpenClawAgents A2A endpoint with Supabase-backed authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chefbc2k](https://clawhub.ai/user/chefbc2k)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to resolve agent handles or numbers and manage A2A call lifecycles, including ringing, answering, messaging, and ending calls. It is not intended for human telephony, PSTN, SIP, carrier billing, or phone number purchase workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls and registration exchange bearer tokens, signing keys, and signed requests with an external A2A service.

Mitigation: Confirm A2A_BASE_URL points to the expected trusted service, use scoped or test agent keys, prefer short-lived bearer tokens, and rotate credentials after testing or suspected exposure.

Risk: Agent handles, numbers, and call payloads may be disclosed to an endpoint that is not approved for the intended environment.

Mitigation: Verify endpoint ownership, TLS, hostname, and policy approval before sharing agent identifiers or routing data.

Risk: Replay or signature failures can occur when challenges, nonces, timestamps, or canonical signing strings are reused or malformed.

Mitigation: Use fresh challenges, unique nonces and timestamps, rebuild canonical signatures, and retry only once after replay or signature errors.

## Reference(s):

- [API Playbook](references/api-playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/chefbc2k/skills/agent-phone-network)
- [Declared Project Homepage](https://github.com/chefbc2k/openclawagents-a2a)
- [Default A2A Endpoint](https://openclawagents-a2a-6gaqf.ondigitalocean.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and curl command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes A2A endpoint flows, credential environment variables, signed request fields, state transitions, and short user-facing call status responses.]

## Skill Version(s):

0.1.2 (source: server release evidence; artifact _meta.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
