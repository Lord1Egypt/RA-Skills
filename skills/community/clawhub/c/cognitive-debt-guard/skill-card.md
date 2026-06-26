## Description: <br>
Cognitive Debt Guard helps developers reduce cognitive debt in AI-generated code with comprehension gates, review frameworks, AI-free zones, and maintenance checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill when reviewing or accepting AI-generated code to preserve comprehension, limit risky changes, and identify hidden maintainability issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides opinionated process guidance rather than technical enforcement, so teams may apply rules such as MEMORY.md, AI-free zones, or strict PR limits in contexts where they do not fit. <br>
Mitigation: Review the practices against the team's workflow before adoption and adjust automatic invocation or process rules when they become noisy. <br>
Risk: Review guidance can be mistaken for proof that AI-generated code is safe or correct. <br>
Mitigation: Use the comprehension gate and review layers as a supplement to normal testing, security review, and human code ownership. <br>


## Reference(s): <br>
- [Cognitive Debt Guard on ClawHub](https://clawhub.ai/aptratcn/cognitive-debt-guard) <br>
- [README.md](artifact/README.md) <br>
- [DEBT_INDICATORS.md](artifact/DEBT_INDICATORS.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Prompt Guard](https://github.com/aptratcn/prompt-guard) <br>
- [Error Recovery](https://github.com/aptratcn/skill-error-recovery) <br>
- [EVR Framework](https://github.com/aptratcn/evr-framework) <br>
- [Systematic Debugging](https://github.com/aptratcn/systematic-debugging) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with checklists, review questions, and inline shell commands for optional installation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no executable code or credential use is included in the artifact.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
