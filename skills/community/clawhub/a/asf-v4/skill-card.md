## Description: <br>
AI Native Full-Stack Software Factory V1.5.6 provides OpenClaw governance, requirement refinement, memory, optimization, and audit-oriented tools for software delivery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alshowse-tech](https://clawhub.ai/user/alshowse-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to refine complex requirements, check governance vetoes, generate ownership proofs, score role assignments, estimate rework risk, and coordinate OpenClaw automation. It is intended for normal ClawHub use, with caution around commands and data handling noted by the security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports broad control-plane authority and overstated or unenforced safety features. <br>
Mitigation: Install only in a constrained environment and do not rely on advertised sandbox, rollback, safety, or audit gates as real enforcement. <br>
Risk: CLI, deploy, and load-skill commands may affect the agent environment or workflow state. <br>
Mitigation: Review or disable those commands before installation in sensitive workspaces. <br>
Risk: Memory and logging behavior may expose private prompts or task data. <br>
Mitigation: Prefer local embeddings for private memory and treat logs as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alshowse-tech/asf-v4) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Release 1.5.6 Notes](artifact/RELEASE-1.5.6.md) <br>
- [Package Manifest](artifact/package.json) <br>
- [Skill Manifest](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like tool results, TypeScript examples, shell commands, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit governance decisions, proofs, risk scores, optimization recommendations, diagnostics, and command/configuration snippets.] <br>

## Skill Version(s): <br>
1.5.6 (source: server release metadata, package.json, skill.yaml, RELEASE-1.5.6.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
