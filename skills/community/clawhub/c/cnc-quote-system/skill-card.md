## Description:

CNC Quote System helps agents estimate CNC part prices, retrieve manufacturing material and case information, and flag quoting risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT

## Use Case:

Developers, manufacturing engineers, and quoting teams use this skill to draft CNC part quotations from material, dimension, surface-treatment, and quantity inputs. Outputs should support review workflows rather than replace validated production pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates its RAG, accuracy, material coverage, and risk-control capabilities relative to the included prototype files.

Mitigation: Treat quotes and risk labels as decision support only; validate material data, pricing formulas, case coverage, and advertised performance before using it for real orders.

Risk: Dependency ranges are not pinned, which can make installed behavior vary across environments.

Mitigation: Install in an isolated environment with pinned dependency versions and test the exact dependency set before deployment.

Risk: Malformed or out-of-scope material, dimension, surface, and quantity inputs can produce misleading estimates.

Mitigation: Add input validation and clear documentation of supported materials, surfaces, units, and quantity ranges before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/cnc-quote-system)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples and structured quoting results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated prices, lead times, retrieval matches, and risk warnings; results require human validation before operational use.]

## Skill Version(s):

1.0.0 (source: server release and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
