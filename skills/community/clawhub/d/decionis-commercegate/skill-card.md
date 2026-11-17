## Description:

Check commerce actions such as price, stock, order, refund, or return changes against merchant margin, stock, and refund policy before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocularminds](https://clawhub.ai/user/ocularminds)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce operators and developers use this skill before marketplace, storefront, or ERP commerce actions to receive PROCEED, HOLD, BLOCK, ALLOW, or BLOCK policy guidance with supporting margin, stock, refund, or transaction rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party npm MCP server and Decionis API credentials.

Mitigation: Verify that @decionis/commerce@0.1.3 is the intended package from the expected publisher, run it in a constrained environment, and provide only the Decionis API key and organization ID needed for the workflow.

Risk: Commerce facts and Decision Dossiers may be sent to or stored by the Decionis service during evaluation.

Mitigation: Confirm the merchant's data-handling requirements before use and submit only the commerce facts needed for the policy decision.

Risk: A PROCEED policy result could be mistaken for direct permission to complete a commerce action.

Mitigation: Keep the merchant's own tool or a human operator as the actor that performs the action, and stop on HOLD, BLOCK, errors, or ambiguous answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ocularminds/skills/decionis-commercegate)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP setup snippets and commerce policy results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DECIONIS_API_KEY and DECIONIS_ORG_ID for evaluation workflows; capability discovery works without credentials.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
