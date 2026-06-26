## Description: <br>
Run project quality checks and security reviews, fixing all errors by priority until all pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run project linting, type checks, tests, security audits, formatting, and build checks, then fix reported issues until the checks pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project check commands, tests, builds, and audit tools may run repository code, consume time, or access the network. <br>
Mitigation: Review configured commands in unfamiliar repositories before execution and run only the checks needed for the task. <br>
Risk: Automated fixes may alter code beyond the user's intended scope if check output is broad or ambiguous. <br>
Mitigation: Keep changes scoped to reported check failures, rerun checks after each fix, and review the final diff before accepting the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/code-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit project files while resolving reported check failures; the skill instructs the agent not to commit code or change version numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
