## Description:

Calls Fetch.ai Agentverse agents by address, searches the Agentverse marketplace, shows a curated agent catalog, and sends ChatMessages to selected agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steve-dusty](https://clawhub.ai/user/steve-dusty)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Fetch.ai Agentverse agents and route natural-language requests for search, translation, statistics, stock signals, image generation, GitHub metadata, or general AI chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts are sent to Fetch.ai Agentverse agents and may expose sensitive, private, or proprietary content.

Mitigation: Avoid submitting sensitive content and disclose that requests are routed to external Agentverse agents before use.

Risk: The skill uses AGENTVERSE_API_KEY for mailbox registration.

Mitigation: Store the key securely, prefer limited-use credentials where possible, and rotate or revoke the key if it may have been exposed.

Risk: The skill persists local identity and response state that may require cleanup on shared machines.

Mitigation: Run the skill in a limited environment and remove or protect local seed and temporary response files when appropriate.

## Reference(s):

- [Fetch Agents Setup](references/mailbox-setup.md)
- [Fetch Agents ClawHub listing](https://clawhub.ai/steve-dusty/skills/fetch-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language text or Markdown-formatted responses from selected Agentverse agents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may depend on third-party Agentverse agents, network availability, AGENTVERSE_API_KEY mailbox registration, and a 30-60 second response window.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
