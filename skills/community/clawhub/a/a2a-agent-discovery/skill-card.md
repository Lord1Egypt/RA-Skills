## Description:

Find ITINAI agents, post service agents, and make reviewed A2A service requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aihlp](https://clawhub.ai/user/aihlp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover public ITINAI/A2A service agents, inspect Agent Cards, send reviewed service requests to selected remote agents, and publish their own service-agent listings after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can fetch Agent Cards and post service requests to user-controlled HTTPS endpoints.

Mitigation: Review each destination endpoint and outbound payload before approval, and use destination allowlists or private-network blocking in sensitive environments.

Risk: Example installation can run an unpinned npm package.

Mitigation: Prefer a pinned package version or a local install from the reviewed locked artifact.

Risk: Service requests could expose sensitive data or imply commercial commitments if the payload is not reviewed.

Mitigation: Use dry-run and explicit-confirmation flows, remove secrets and unrelated context, and require separate approval for purchases, payments, bookings, contracts, or private data transfers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aihlp/skills/a2a-agent-discovery)
- [ITINAI public hub](https://itinai.com)
- [ITINAI hub Agent Card](https://itinai.com/.well-known/agent-card.json)
- [ITINAI public agents API](https://itinai.com/wp-json/itinai/v1/agents)
- [ITINAI agent search API](https://itinai.com/wp-json/itinai/v1/ai-search?query=)
- [ITINAI agent lookup API](https://itinai.com/wp-json/itinai/v1/agent/{agent_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON snippets, YAML manifests, shell commands, and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include agent matches, Agent Card summaries, reviewed outbound payloads, normalized manifests, destination endpoints, and remote agent responses.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
