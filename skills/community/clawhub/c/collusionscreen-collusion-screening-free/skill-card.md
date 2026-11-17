## Description:

Locally screens multiple bid documents for objective, reproducible collusion clues by checking for shared contact details and overlapping project personnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement reviewers, bid agents, and compliance teams use this skill to locally screen multiple bidders' materials for repeated contact details and overlapping project personnel. The output is a lead-screening aid for human review, not a procurement or legal determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid materials can contain confidential business information and personal data.

Mitigation: Run the skill only in approved local environments and follow the organization's confidentiality and privacy rules for bid materials.

Risk: The output may be mistaken for a legal or procurement decision.

Mitigation: Treat findings as screening clues only and require review by the responsible evaluation committee, compliance team, or regulator before taking action.

Risk: The free version checks only shared contact details and overlapping project personnel, so missing findings do not prove the absence of collusion indicators.

Mitigation: Use additional review steps for omitted clue types such as text similarity, bid price patterns, mixed files, repeated errors, source of deposits, and formatting fingerprints.

Risk: Incomplete or malformed input can prevent meaningful cross-bidder comparison.

Mitigation: Provide at least two bidder records with usable document text and review insufficient-input messages before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/collusionscreen-collusion-screening-free)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable console text or structured JSON with screening findings, omitted checks, notes, and guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; findings mask contact details and natural-person names while preserving bidder organization names.]

## Skill Version(s):

1.0.52 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
