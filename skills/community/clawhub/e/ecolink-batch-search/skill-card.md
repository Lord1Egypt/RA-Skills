## Description:

EcoLink batch-searches local carbon-footprint datasets, helps an agent match product or material names across ecoinvent, CPCD, and GHG factor data, and exports selected results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakahilda](https://clawhub.ai/user/kakahilda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to batch search carbon-footprint factors for product or material lists, review candidate matches, and export selected records for lifecycle-assessment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM mode can send product queries to a remote LLM provider and requires an API key.

Mitigation: Use the documented --no-llm mode unless remote LLM processing is intended, and avoid passing valuable API keys on the command line.

Risk: Generated HTML, CSV, and Excel outputs can contain content derived from untrusted product names or uploaded input files.

Mitigation: Treat generated preview and export files as untrusted, review them before sharing, and open them only in appropriate local tools.

Risk: Fuzzy matches, LLM translations, decompositions, and alternative recommendations can be approximate.

Mitigation: Review candidate matches in the preview workflow and verify selected factors before relying on them for reporting or lifecycle assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kakahilda/skills/ecolink-batch-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance plus generated CSV or Excel result files and an optional interactive HTML preview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use can run in --no-llm mode; optional LLM mode sends queries to a configured compatible remote API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
