## Description: <br>
Dual-Mode Reasoner is a risk-aware reasoning skill that helps an agent choose between quick and deliberate reasoning modes and produce a fixed decision-support output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarkchenkai](https://clawhub.ai/user/clarkchenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill when a task needs visible reasoning-depth selection, assumption exposure, counterexample testing, and a clear stop condition for decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation may make the assistant use the six-section reasoning format automatically. <br>
Mitigation: Disable implicit invocation or call the skill explicitly only when structured risk-aware decision support is desired. <br>
Risk: Users may mistake the reasoning protocol for regulated-domain expertise. <br>
Mitigation: Use the skill as a decision-support scaffold and consult qualified experts for legal, medical, financial, or other regulated decisions. <br>
Risk: The skill can surface assumptions and counterexamples but cannot verify external facts on its own. <br>
Mitigation: Check material evidence independently before acting on high-impact or hard-to-reverse recommendations. <br>


## Reference(s): <br>
- [Kahneman Reference](references/kahneman.md) <br>
- [Mode Triggers](references/mode-triggers.md) <br>
- [Deliberation Patterns](references/deliberation-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clarkchenkai/dual-mode-reasoner-clarkchenkai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with six named sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fixed output contract ending with mode selection, risk signals, working assumptions, counterexamples, recommendation, and stop condition.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
