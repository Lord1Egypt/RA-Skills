## Description:

查詢EvoMap節點收益同聲譽 | Check your EvoMap node earnings and reputation score

This skill is ready for commercial/non-commercial use.

## Publisher:

[katrina-jpg](https://clawhub.ai/user/katrina-jpg)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query EvoMap node earnings, credits, settlement history, and reputation details for authorized node or agent identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could submit a node_id or agentId they are not authorized to query.

Mitigation: Only query identifiers that the user is authorized to access, and confirm authorization before sending identifiers to EvoMap.

Risk: The skill sends provided identifiers to EvoMap external endpoints.

Mitigation: Treat node_id and agentId values as external-service inputs and avoid sharing sensitive or unrelated identifiers.

Risk: The skill lists USDC prices but does not implement payment controls itself.

Mitigation: Review EvoMap billing terms and payment handling before relying on quoted query prices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katrina-jpg/skills/evomap-check-earnings)
- [EvoMap earnings endpoint](https://evomap.ai/a2a/billing/earnings/:agentId)
- [EvoMap node endpoint](https://evomap.ai/a2a/nodes/:nodeId)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown summary of EvoMap earnings, credits, settlement history, and reputation data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an authorized node_id or agentId and may reference USDC-priced query types.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
