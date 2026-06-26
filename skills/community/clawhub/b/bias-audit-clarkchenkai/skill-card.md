## Description: <br>
Bias Audit helps agents surface biased or loaded decision framing, rewrite the question neutrally, and define explicit decision criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarkchenkai](https://clawhub.ai/user/clarkchenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agent builders can use this skill to audit emotionally loaded or poorly framed decisions before acting on them. It produces a neutral reframe, missing-evidence prompts, decision criteria, and a recommended next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation can reframe user wording when the user did not explicitly request a bias audit. <br>
Mitigation: Disable implicit invocation or call the skill only by name when tighter control is needed. <br>
Risk: A framing audit can overemphasize bias concerns if it is used without domain evidence. <br>
Mitigation: Preserve the original concern and ask for missing counterevidence, baselines, or comparison points before recommending action. <br>


## Reference(s): <br>
- [Audit Rules](references/audit-rules.md) <br>
- [Bias Patterns](references/bias-patterns.md) <br>
- [Kahneman Reference](references/kahneman.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with six fixed sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code execution, credential requests, network access, or local data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
