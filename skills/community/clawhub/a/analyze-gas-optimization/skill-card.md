## Description: <br>
Analyze and optimize Aptos Move contracts for gas efficiency, identifying expensive operations and suggesting optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Aptos Move contracts before deployment or high-frequency use, identify gas-heavy storage and computation patterns, and generate optimization recommendations and measurement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optimization advice could introduce functional or security regressions if applied mechanically. <br>
Mitigation: Review suggested contract changes, preserve access control and input validation, and rerun tests and security review before deployment. <br>
Risk: Aptos CLI simulation commands may be adapted incorrectly for real projects. <br>
Mitigation: Inspect command arguments and use simulation or test environments before applying changes to production workflows. <br>
Risk: The publisher is third party and server-resolved source provenance is unavailable. <br>
Mitigation: Verify the publisher profile and release source before relying on the advice for production contracts. <br>


## Reference(s): <br>
- [Aptos Gas Schedule](https://github.com/aptos-labs/aptos-core/blob/main/aptos-move/aptos-gas-schedule) <br>
- [Move VM Gas Metering](https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/aptos-vm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Move and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides recommendations, checklists, report templates, and Aptos CLI simulation commands; does not execute code itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
