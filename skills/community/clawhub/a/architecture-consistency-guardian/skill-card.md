## Description: <br>
Enforce system-wide consistency before code changes by guiding agents through source-of-truth discovery, global reference scans, grouped modifications, residue audits, and regression verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upsightx](https://clawhub.ai/user/upsightx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when code changes touch shared architecture contracts such as names, states, paths, configs, schemas, entry points, fallbacks, or documentation. It helps an agent scan globally, identify the single source of truth, plan coordinated edits, audit residue, and produce a structured consistency report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scanners can inspect repository contents beyond the intended task scope if pointed at broad directories. <br>
Mitigation: Keep scan roots limited to the repository you intend to inspect and avoid scanning home directories or unrelated private code. <br>
Risk: The workflow can lead to broad cross-file changes that affect shared contracts. <br>
Mitigation: Review the proposed modification plan before edits, then run residue searches and focused regression checks after changes. <br>


## Reference(s): <br>
- [Detailed workflow](references/workflow.md) <br>
- [Structured report template](references/output_template.md) <br>
- [Common consistency risk patterns](references/risk_patterns.md) <br>
- [Architecture contract template](references/contract_template.md) <br>
- [ClawHub skill page](https://clawhub.ai/upsightx/architecture-consistency-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured report sections; bundled scanners may also emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include modification plans, source-of-truth summaries, residue audit results, regression checks, and architecture contract templates.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
