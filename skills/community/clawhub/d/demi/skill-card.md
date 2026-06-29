## Description: <br>
Use before implementing, scaffolding, prototyping, or adding a feature when the work should start with the smallest useful code path, avoid speculative architecture, or prevent overbuilding before reduce would be needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill before implementation or prototyping to choose the smallest useful code path, follow existing repository patterns, avoid speculative architecture, and verify the resulting slice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged maintenance workflows may affect production users, content, packages, email, or Convex data if applied to the wrong target. <br>
Mitigation: Use the skill only in a maintainer or developer context, confirm targets, review dry-run output when available, and approve write operations deliberately. <br>
Risk: Generated guidance can lead to incorrect or misleading implementation choices if followed without review. <br>
Mitigation: Review the proposed scope and run the smallest meaningful check before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/escoffier-labs/demi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with optional plans, code references, commands, and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance for scope control before code changes] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
