## Description: <br>
Generator economic dispatch and cost optimization for power systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-system engineers use this skill to formulate economic dispatch problems, minimize generation cost, compute generator setpoints, co-optimize reserves, and summarize operating margins from MATPOWER-style data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Numerical optimization guidance can produce misleading dispatch results when applied to untrusted data, incomplete constraints, or real operational and financial decisions without review. <br>
Mitigation: Use trusted datasets, review dependency installation separately, and have qualified power-system reviewers validate assumptions, constraints, solver results, and downstream decisions. <br>


## Reference(s): <br>
- [Generator Cost Functions Reference](references/cost-functions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python code snippets and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to numerical optimization patterns for generator dispatch; no runtime tool execution is included.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
