## Description: <br>
Cnsdoce Publish V4 helps agents query Chinese engineering cost quotas, calculate item pricing and fees, and generate quotation tables for installation, building, municipal, and landscaping projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoshun-sudo](https://clawhub.ai/user/caoshun-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and cost engineers use the skill to search quota items, compare list and quota units, calculate composite prices and fees, and prepare traceable quotation outputs for China engineering cost workflows. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Engineering scope descriptions may be sent to Tencent or ByteDance LLM APIs during semantic matching. <br>
Mitigation: Use explicit invocation for sensitive projects, avoid sending confidential scope details, or use a local-only workflow when confidentiality matters. <br>
Risk: The database migration workflow may alter a real database if run without preparation. <br>
Mitigation: Back up databases and review migration inputs before running migration scripts. <br>
Risk: Dependency versions may change over time and affect behavior. <br>
Mitigation: Prefer pinned dependencies and scan the runtime environment before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoshun-sudo/cnsdoce) <br>
- [Cost composition and pricing procedure](references/cost_composition.md) <br>
- [Fee standard](references/fee_standard.md) <br>
- [Measure item rules](references/measure_items.md) <br>
- [Multi-quota mapping](references/multi_quota_mapping.md) <br>
- [Unit conversion rules](references/unit_conversion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON quota recommendations, shell command examples, and quotation-table content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional LLM semantic matching can use HUNYUAN_API_KEY, DOUBAO_API_KEY, and LLM_PROVIDER; ClawHub metadata lists Python and Windows support.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
