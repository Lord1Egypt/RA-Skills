## Description: <br>
Stress-test high-risk changes with fresh-context skepticism before implementation or release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to stress-test high-risk software changes before implementation or release. It helps structure skeptical review around falsifiable claims, failure modes, disconfirming evidence, and a proceed, patch first, or stop decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fresh-context review can expose sensitive files, logs, secrets, private user data, or machine-specific paths if too much context is shared. <br>
Mitigation: Share only the minimum files or logs needed for review and redact secrets, tokens, private user data, and machine-specific paths. <br>
Risk: The skill is an advisory review aid and can miss release-blocking correctness, test, or security issues. <br>
Mitigation: Treat the output as review guidance; verify direct evidence such as tests, CI, release metadata, package contents, and rollback paths before shipping. <br>
Risk: Permission or sandbox review can be misused to justify broad boundary weakening. <br>
Mitigation: Prefer narrow writable roots, exact command prefixes, and workflow-specific exceptions; do not treat auto-review as permission expansion. <br>


## Reference(s): <br>
- [Risk Checklist](references/risk-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/doubt-driven-development) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Terse Markdown or plain-text review summary with claim, main risk, evidence checked, decision, and reason fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The decision is one of proceed, patch first, or stop, with the next concrete action named when risk remains.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
