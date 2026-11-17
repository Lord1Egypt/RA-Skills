## Description: <br>
Build and deploy applications to Alibaba Cloud ECS through local build, script injection, and asynchronous InstallApplication deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to package applications, prepare Alibaba Cloud ECS deployment scripts, run guarded InstallApplication deployments, and troubleshoot failed ECS deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad Alibaba Cloud deployment authority against ECS resources. <br>
Mitigation: Use a least-privilege RAM role and provide explicit region and instance IDs before any deployment action. <br>
Risk: Generated start and stop scripts, deployment artifacts, and command payloads may affect running services. <br>
Mitigation: Review scripts, artifacts, and the install checklist before confirming deployment. <br>
Risk: The security guidance flags EcsSendFile shell-escaping concerns for sensitive file transfer. <br>
Mitigation: Avoid sending sensitive files through EcsSendFile until that issue is fixed. <br>
Risk: The security guidance notes missing ops or step files as a production readiness concern. <br>
Mitigation: Verify all required ops and step files are present before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cadt-deploy-on-aliyun) <br>
- [Build Pipeline (Local Build)](references/build-pipeline/README.md) <br>
- [Build Commands](references/build-pipeline/build-commands.md) <br>
- [CLI Development](references/cli-development.md) <br>
- [Deploy Modes](references/deploy-modes.md) <br>
- [Failure Codex](references/failure-codex.md) <br>
- [Quality Gates](references/quality-gates.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Execution Order & State Machine](references/state-machine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON payloads, and generated script or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local deployment artifacts and Alibaba Cloud CLI operation payloads that require user review before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
