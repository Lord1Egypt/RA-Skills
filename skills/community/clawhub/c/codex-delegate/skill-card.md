## Description: <br>
Decide when to delegate code-heavy, repo-heavy, multi-file, or environment-sensitive technical work to Codex while keeping final judgment and user-facing decisions with the main agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, and agent operators use this skill to decide whether Codex should handle focused technical execution, repository inspection, patch drafting, or static review while the main agent retains scope, risk, validation, and final communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegating broad or sensitive work could expose unnecessary secrets, credentials, or private repository context. <br>
Mitigation: Keep delegated tasks narrow and avoid sending secrets, credentials, or unnecessary private content to Codex. <br>
Risk: A delegated technical conclusion may be plausible but incomplete for the user's actual environment or acceptance criteria. <br>
Mitigation: Review Codex conclusions before acting and keep final validation, risk trade-offs, and user-facing decisions with the main agent. <br>


## Reference(s): <br>
- [Codex Delegate Routing Notes](references/routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Concise Markdown decision summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports whether to delegate, what Codex should handle, what the main agent must keep, and the validation level required before completion.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
