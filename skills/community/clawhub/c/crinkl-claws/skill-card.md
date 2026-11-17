## Description:

Crinkl Claws helps agents scan Gmail or AgentMail billing emails, submit raw messages for DKIM-based receipt verification through Crinkl, and record Bitcoin Lightning receipt rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvintanpoco](https://clawhub.ai/user/alvintanpoco)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to pair with a Crinkl wallet, find recent billing emails through Gmail or AgentMail, submit receipts for verification, and track earned sats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read recent billing emails and upload full raw message contents to Crinkl for DKIM verification.

Mitigation: Prefer a dedicated AgentMail receipt inbox where possible, keep Gmail access read-only and vendor-scoped, and confirm Crinkl's retention model before use.

Risk: The skill stores a Crinkl API key and receipt submission history in agent memory.

Mitigation: Store the key only after human-approved pairing, limit access to agent memory, and revoke the key if the agent or workspace is no longer trusted.

Risk: Recurring or unattended runs may continue submitting eligible receipts after setup.

Mitigation: Run on an operator-approved cadence, review logs for each cycle, and avoid broad automated scans unless recurring submission is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvintanpoco/skills/crinkl-claws)
- [Crinkl website](https://crinkl.xyz)
- [Crinkl MCP tool list](https://mcp.crinkl.xyz)
- [DomainKeys Identified Mail (DKIM)](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail)
- [Crinkl protocol specification](https://github.com/crinkl-protocol/crinkl-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell commands, and API-call steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Crinkl MCP server, CRINKL_API_KEY, and either Gmail access through gog or an AgentMail receipt inbox.]

## Skill Version(s):

1.3.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
