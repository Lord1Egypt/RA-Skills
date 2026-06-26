## Description: <br>
Helps agents design, review, or convert multi-step tasks into bounded ARG Action Chains with step contracts, progressive disclosure, validation gates, and file-level deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhgd3250905](https://clawhub.ai/user/mhgd3250905) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn recurring or high-drift workflows into structured ARG action chains. It is especially useful when tasks need step contracts, validation gates, constrained LLM judgment, or optional file-level skill packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ARG workflows may include target paths, scripts, or validation commands that affect local files or operational systems. <br>
Mitigation: Review generated paths and scripts before running them, especially outside a disposable workspace. <br>
Risk: A generated workflow may include external sending, publishing, deletion, production access, or other irreversible actions. <br>
Mitigation: Require a human or external gate before irreversible or production-affecting steps are executed. <br>
Risk: ARG step validation reduces drift but does not by itself prevent a capable agent from skipping steps or self-attesting completion. <br>
Mitigation: Use the skill's Level 2 external-gate pattern when jump prevention, anti-forgery, or independent acceptance is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mhgd3250905/arg-action-chain-designer) <br>
- [Output Modes](references/output-modes.md) <br>
- [ARG Reliability Levels](references/reliability-levels.md) <br>
- [Runtime Skill Template](references/runtime-template.md) <br>
- [Step Contract Standard](references/step-contract-standard.md) <br>
- [Validation Gates and LLM Judgment](references/validation-and-judgment.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with optional file contents, scripts, and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SKILL.md runtimes, plans/ step contracts, scripts/ drafts, and output/ structure when the user requests file-level deliverables.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
