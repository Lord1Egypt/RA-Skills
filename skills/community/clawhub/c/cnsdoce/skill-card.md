## Description:

Chinese construction-costing skill for quota lookup, installation cost composition, fee calculations, price checks, indicator analysis, and quotation table generation for construction, municipal, landscaping, and Shandong/Jinan costing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoshun-sudo](https://clawhub.ai/user/caoshun-sudo)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and construction-cost engineers use this skill to query quota items, compare bill-of-quantities units with quota units, calculate Shandong/Jinan fee structures, run optional LLM-assisted quota matching, and prepare traceable quotation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-backed matching can send construction or project descriptions to third-party model providers.

Mitigation: Use the skill only with approved provider endpoints and avoid submitting confidential bid, supplier, or project data unless that processing is authorized.

Risk: Configurable model endpoints and API credentials can expose users to untrusted hosts or credential handling mistakes.

Mitigation: Restrict HUNYUAN_URL and related provider settings to trusted HTTPS hosts and manage API keys through the user's approved secret-handling process.

Risk: Some workflows can mutate local quota, pricing, or history databases.

Mitigation: Back up local databases before running import, indicator, or price-history workflows and review database changes before relying on them for formal costing.

Risk: Dependencies are not guaranteed to be pinned in the user's environment.

Mitigation: Review and pin dependencies before deployment in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoshun-sudo/skills/cnsdoce)
- [Cost composition and pricing procedure](references/cost_composition.md)
- [Fee standard](references/fee_standard.md)
- [Measure item calculation rules](references/measure_items.md)
- [Multi-quota mapping table](references/multi_quota_mapping.md)
- [Other item calculation rules](references/other_items.md)
- [Unit conversion table](references/unit_conversion.md)
- [Mechanical equipment installation quota reference](references/volume_01_mechanical.md)
- [Thermal equipment installation quota reference](references/volume_02_thermal.md)
- [Static equipment and metal structure quota reference](references/volume_03_static.md)
- [Electrical equipment installation quota reference](references/volume_04_electrical.md)
- [Intelligent building systems quota reference](references/volume_05_intelligent.md)
- [Automation instrumentation quota reference](references/volume_06_instrument.md)
- [HVAC quota reference](references/volume_07_hvac.md)
- [Industrial pipeline quota reference](references/volume_08_pipeline.md)
- [Fire protection quota reference](references/volume_09_fire.md)
- [Plumbing, heating, and gas quota reference](references/volume_10_plumbing.md)
- [Telecommunications installation quota reference](references/volume_11_telecom.md)
- [Coating, anticorrosion, and insulation quota reference](references/volume_12_coating.md)
- [Measure item quota reference](references/volume_13_measure.md)
- [Tencent TokenHub chat completions endpoint](https://tokenhub.tencentmaas.com/v1/chat/completions)
- [Volcengine Ark chat completions endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, calculation tables, and optional Excel-oriented quotation outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional API keys for LLM-backed matching and may read or update local quota, pricing, and history databases when users enable those workflows.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
