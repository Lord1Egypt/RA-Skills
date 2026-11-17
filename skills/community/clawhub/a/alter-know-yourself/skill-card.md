## Description:

Helps a person inspect and contest what ~alter has inferred about them, including trait history, evidence trails, attestation permissions, and identity setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to read their own ~alter identity record, understand the evidence behind inferred traits, manage who may attest to their competence, and contest readings they believe are wrong.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or act on sensitive personal identity information.

Mitigation: Use it only for your own ~alter record and review consent settings before connecting work streams or evidence sources.

Risk: The skill requires a member key for the declared ~alter MCP endpoint.

Mitigation: Configure only the declared endpoint and protect ALTER_API_KEY; do not paste invented or unnecessary credentials into agent output.

Risk: Third-party attestations may affect how competence claims are represented.

Mitigation: Review who may attest about you, revoke unwanted permissions, and contest readings you believe are incorrect.

## Reference(s):

- [~Alter MCP endpoint](https://mcp.truealter.com/api/v1/mcp)
- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-know-yourself)
- [ClawHub publisher profile](https://clawhub.ai/user/true-alter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with tool names, MCP endpoint details, and credential handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool use with ALTER_API_KEY authentication; no raw credentials should be printed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
