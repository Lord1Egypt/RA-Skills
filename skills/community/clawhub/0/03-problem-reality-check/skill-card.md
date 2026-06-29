## Description: <br>
Stress-tests whether one selected Research Question Card's problem is real, evidence-backed, externally grounded, safely motivated, and worth keeping as a research motivation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snake-fan](https://clawhub.ai/user/snake-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to interrogate one selected Research Question Card against local evidence, capture challenge-question responses, and decide whether the problem motivation is defensible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads linked local research artifacts and creates or updates markdown review files in the selected workspace. <br>
Mitigation: Confirm the workspace root before use and review generated files under research-question-checks before relying on them. <br>
Risk: Problem-reality conclusions can be incomplete or misleading if local evidence is missing, stale, or interpreted too broadly. <br>
Mitigation: Check the cited local evidence and interrogation transcript before accepting the final verdict or using it in a paper motivation. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/03-problem-reality-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational guidance with scoped Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates research-question-checks artifacts for one selected card and asks one challenge question at a time.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
