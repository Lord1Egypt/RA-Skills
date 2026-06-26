## Description: <br>
Coordinate multiple OpenClaw instances in a shared GitHub repository under a half-trust model with secrecy boundaries, approval gates, structured tasks, claims, handoffs, risks, and decision records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtual-ny](https://clawhub.ai/user/virtual-ny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use ClawColab to coordinate multiple OpenClaw instances through shared GitHub artifacts while preserving secrecy boundaries, approval gates, task ownership, handoffs, and decision records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared repositories are visible to collaborators and can expose secrets, private memory, or sensitive context if users over-share. <br>
Mitigation: Classify content before sharing, keep secrets and private memory out of repository artifacts unless explicitly approved, and prefer summary-only sealed references when exact details are unnecessary. <br>
Risk: Bundled CI validation depends on repository workflow paths and policy files being reviewed for the target repository. <br>
Mitigation: Review workflow path assumptions and policy templates before enabling CI validation in a shared repository. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/virtual-ny/clawcolab) <br>
- [Approval Model](references/approval-model.md) <br>
- [Classification Guide](references/classification-guide.md) <br>
- [GitHub Workflow](references/github-workflow.md) <br>
- [Governance Modes](references/governance-modes.md) <br>
- [Pre-share Checks](references/pre-share-checks.md) <br>
- [Privacy Review](references/privacy-review.md) <br>
- [Role Model](references/role-model.md) <br>
- [Security Model](references/security-model.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, YAML and Markdown templates, and Python validation or generation scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes repository artifact templates and local validation helpers for collaboration payloads, policies, task state, and claim conflicts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
