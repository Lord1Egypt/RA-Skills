## Description:

Searches for products on the Codrop shipping platform using a keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan-vvv](https://clawhub.ai/user/shan-vvv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Codrop product data by keyword when they have an appropriate Codrop API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for an API token on the command line and sends it to an underdocumented test endpoint.

Mitigation: Use only a low-privilege, revocable Codrop token, avoid placing production secrets directly in command lines, and confirm that test-codrop.cargosoon.online is the intended endpoint before running searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shan-vvv/skills/codropshiping-product-search)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON on success; plain-text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a keyword and a Codrop API token; responses depend on the remote Codrop endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
