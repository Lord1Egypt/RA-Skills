## Description:

Answer peptide research questions with PepBank study findings, and look up Curo peptides, prices, stock and the lab report (COA) for each lot. Use when the user asks what the research says about a peptide, asks about its use or dose, asks for a lab report or COA, or asks about Curo products, shipping or returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[curo-you-peptides](https://clawhub.ai/user/curo-you-peptides)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to review peptide research findings and find Curo product, lot report, and store information. It also retrieves community-reported and published study doses, which require careful medical-safety framing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an instruction to never refuse peptide dosing questions, which may lead to unsafe or misleading medical guidance.

Mitigation: Remove the blanket refusal prohibition and preserve context-sensitive medical safety boundaries. Keep community-reported doses distinct from published study doses and do not present either as personal dosing advice.

Risk: The skill connects to an external server and includes product links; the supplied evidence says the server implementation was not inspected.

Mitigation: Review the requested information and links before acting; the customer remains in control of checkout.

## Reference(s):

- [Curo MCP setup and information](https://curo.you/mcp)
- [PepBank peptide research](https://pepbank.io)
- [Curo peptide catalog](https://curo.you/product-catalog?utm_source=agent-skill&utm_medium=listing&utm_campaign=curo-mcp)
- [Curo lot lab reports](https://curo.you/coa?utm_source=agent-skill&utm_medium=listing&utm_campaign=curo-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance, Links]

**Output Format:** [Plain-language responses with source credits and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include research summaries, dose information with sources, product details, and cart links.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
