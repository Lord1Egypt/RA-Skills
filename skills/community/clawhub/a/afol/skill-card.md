## Description: <br>
Use this orchestration skill to choose the right AFOL provider skill for catalog lookup, marketplace pricing, collection management, valuation, and cross-provider workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AFOL collectors and agents use this skill to route broad LEGO catalog, marketplace, collection, valuation, and cross-provider questions to the appropriate provider skill. It helps choose read-only lookup, valuation, marketplace comparison, or guarded collection workflows without calling provider APIs directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports broader authority than typical routing tasks need. <br>
Mitigation: Review the bundle before installation and avoid unrestricted nested agent execution unless that authority is acceptable. <br>
Risk: The skill relies on provider credentials for some workflows, and credentials can expose private collection, account, store, order, or sales-ledger data. <br>
Mitigation: Use credential-readiness checks without printing secret values, summarize private data, and require explicit user approval plus provider dry-run/yes guards before any write. <br>


## Reference(s): <br>
- [AFOL router prompt](references/prompts/afol-router.txt) <br>
- [AFOL OpenAPI placeholder](references/openapi/afol.yaml) <br>
- [ClawHub AFOL listing](https://clawhub.ai/musketyr/afol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON CLI output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local CLI returns deterministic JSON for routing and credential-readiness checks without printing secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
