## Description: <br>
Diagnose failures using reproduce, isolate, fix, and verify workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose failing tests, runtime errors, performance regressions, or unexpected behavior with a structured reproduce, isolate, fix, and verify process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs, stack traces, or environment details used for debugging can contain secrets. <br>
Mitigation: Redact secrets from logs and environment details before using the skill. <br>
Risk: Suggested fixes may be incomplete or affect unrelated behavior. <br>
Mitigation: Review proposed changes before applying them and verify with the original reproduction plus related tests. <br>
Risk: Activation metadata is malformed in this release. <br>
Mitigation: Prefer an updated release with explicit trigger phrases when trigger reliability matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzfshark/axodus-debugging) <br>
- [Publisher Profile](https://clawhub.ai/user/mzfshark) <br>
- [Debugging Skill Instructions](artifact/debugging.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown with YAML-formatted debugging summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs root cause, fix, verification commands or tests, and optional follow-ups.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill.yml, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
