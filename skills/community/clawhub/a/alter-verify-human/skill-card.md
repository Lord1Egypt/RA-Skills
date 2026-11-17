## Description:

Helps an agent confirm that a specific person is a known, verified ~alter identity and test verification tier, archetype, engagement level, or trait-range claims by handle, member ID, or email before taking consequential action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and operators use this skill for user-directed identity checks before transactions, access grants, credential relays, or other decisions where a false identity claim would matter. It is not intended for speculative lookup, broad profiling, or treating unavailable trait data as a failed claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a hosted ~alter MCP service and requires storing an ALTER_API_KEY.

Mitigation: Install only in environments approved to use that hosted service, store the key as a secret, and send it only to the documented ~alter MCP endpoint.

Risk: Identity checks could be misused for broad lookups, profiling, or decisions based on unavailable trait data.

Mitigation: Use the skill only for specific, user-directed verification cases, read has_data before acting on trait verdicts, and avoid gating decisions on engagement level.

## Reference(s):

- [~alter hosted MCP server](https://mcp.truealter.com/api/v1/mcp)
- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-verify-human)
- [Publisher profile](https://clawhub.ai/user/true-alter)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls]

**Output Format:** [Markdown instructions with JSON MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ALTER_API_KEY and the hosted ~alter MCP server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
