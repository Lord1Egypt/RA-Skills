## Description: <br>
Guides Solidity auditors through a three-level finding verification pipeline using Foundry self-tests, GitHub CI, and auditor review before submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzengbaao](https://clawhub.ai/user/yuzengbaao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security auditors and developers assessing Solidity projects use this skill to verify vulnerability findings with a staged process: local Foundry PoC tests, GitHub CI, and independent review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PoC tests or GitHub Actions workflow changes may be incorrect for a target Solidity repository. <br>
Mitigation: Review generated tests and workflow files before committing them, then run Foundry tests locally and in CI. <br>
Risk: Running tests against untrusted audit targets can execute untrusted code in the development environment. <br>
Mitigation: Run tests for untrusted code in an isolated development environment. <br>
Risk: A passing PoC can still be misleading if it does not prove the claimed attack effect. <br>
Mitigation: Confirm the exploit impact directly, quantify severity, and require independent auditor review before submission. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Solidity, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checklists, decision flows, PoC patterns, CI workflow examples, and severity assessment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
