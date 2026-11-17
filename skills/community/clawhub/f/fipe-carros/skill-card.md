## Description:

Looks up average vehicle prices for cars, motorcycles, and trucks using the Brazilian Tabela FIPE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

Agents can use this skill to help buyers, sellers, insurance workflows, financing workflows, and vehicle researchers retrieve FIPE brand, model, year, and price information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to the public FIPE API.

Mitigation: Permit network access only for expected FIPE lookup requests and review returned pricing before using it in financial or insurance decisions.

Risk: Portuguese trigger phrases for vehicle price lookups may activate the skill broadly.

Mitigation: Scope activation to explicit FIPE or vehicle-price requests when accidental activation matters.

Risk: The Node dependency set requires routine maintenance.

Mitigation: Install deterministically from the lockfile and keep dependencies updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runawaydevil/skills/fipe-carros)
- [Publisher profile](https://clawhub.ai/user/runawaydevil)
- [FIPE API base URL](https://parallelum.com.br/fipe/api/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with vehicle lookup results and example commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese output; performs outbound requests to the public FIPE API.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
