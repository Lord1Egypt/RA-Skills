## Description:

Lightweight business rule engine supporting rule definition, execution, chain orchestration, and dynamic rule loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define, load, evaluate, and orchestrate business rules for application logic such as discounts, eligibility checks, and order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted JSON or DSL rule definitions can reach dynamic condition evaluation.

Mitigation: Accept rule definitions only from trusted administrators, or replace eval-based condition handling with a strict parser before exposing rule creation.

Risk: External or ordinary users could create rules that trigger unsafe or unintended business logic.

Mitigation: Gate rule creation behind validation, authorization, and review before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/business-rule-engine)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kaiyuelv)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-shaped rule definitions and rule evaluation examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
