## Description:

Detects pre-news ambient risk signals across human, legal, and operational systems and converts them into machine-readable, tradable risk primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieershafilone](https://clawhub.ai/user/sieershafilone)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and analysts use Blacksnow to collect legally accessible public signals, align them to a risk ontology, accumulate weak evidence, and package probabilistic risk primitives for finance, insurance, logistics, and policy workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live data fetching may run without verified TLS.

Mitigation: Restore certificate and hostname verification before using live public-data harvesters.

Risk: Harvested records and generated primitives can be retained locally without deletion controls.

Mitigation: Add retention enforcement and deletion procedures before relying on stored signals for business workflows.

Risk: Generated primitives can be sent to configured webhooks.

Mitigation: Restrict webhook destinations to approved HTTPS endpoints and review payload handling before enabling delivery.

Risk: Mock sources can be mixed with live collection behavior.

Mitigation: Disable or clearly label mock sources before using outputs for financial, operational, or policy analysis.

## Reference(s):

- [BlackSnow Agent Specifications](artifact/references/agent_specs.md)
- [BlackSnow Ontology](artifact/references/ontology.md)
- [BlackSnow ClawHub Listing](https://clawhub.ai/sieershafilone/skills/blacksnow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON risk primitive schemas and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces probabilistic risk intelligence and machine-readable risk primitives; outputs are not predictions, advice, or decision execution.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
