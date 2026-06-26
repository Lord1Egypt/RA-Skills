## Description: <br>
Run a complete security audit on any OpenClaw SKILL.md in one call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Skillguard to audit OpenClaw SKILL.md content with a combined malware scan, permission scope check, and prompt injection check before installing or publishing a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local HTTP service and installs common Python web dependencies. <br>
Mitigation: Run it in a trusted local environment, bind it only where needed, and install dependencies from trusted package indexes. <br>
Risk: Audit coverage depends on SkillScan, ScopeCheck, and PromptGuard detector modules being available in the runtime environment. <br>
Mitigation: Confirm the detector modules are installed before relying on the combined verdict, and treat missing-module setup failures as an incomplete audit. <br>
Risk: Submitted SKILL.md content is processed by the local audit endpoint. <br>
Mitigation: Submit only skill files intended for analysis and avoid sending unrelated sensitive content. <br>


## Reference(s): <br>
- [ClawHub Skillguard release](https://clawhub.ai/mirni/gh-skillguard) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON security audit report with a SAFE, CAUTION, or DANGEROUS verdict and scan, scope, and injection sub-reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input is raw SKILL.md text; output includes total findings, safety and risk scores, declared access, undeclared access, and detected injection patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
