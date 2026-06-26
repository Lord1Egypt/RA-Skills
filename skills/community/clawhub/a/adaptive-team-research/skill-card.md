## Description: <br>
Adaptive multi-agent team for software project reviews that selects a collaboration mode and runs facts, debate, and consensus rounds to produce actionable plans with cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joe-rq](https://clawhub.ai/user/Joe-rq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run multi-perspective software project reviews, architecture assessments, code audits, and design reviews. It helps select a review mode, coordinate role-based analysis, and converge findings into prioritized action plans with cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review workflow has multiple agents read the target repository and writes a local review report that may include sensitive project details. <br>
Mitigation: Run it only on repositories whose contents can be included in a local review canvas, and review the generated report before sharing it. <br>
Risk: The skill produces recommendations and action plans rather than code changes, so findings may be incomplete or context-dependent. <br>
Mitigation: Treat the output as review guidance, validate recommendations with project owners, and confirm costs and priorities before implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Joe-rq/adaptive-team-research) <br>
- [Mode selection guide](references/mode-selection.md) <br>
- [Round protocols](references/round-protocols.md) <br>
- [Round 1 role prompts](references/role-prompts-r1.md) <br>
- [Round 2 role prompts](references/role-prompts-r2.md) <br>
- [Review canvas template](assets/canvas-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown review canvas plus concise summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local reviews/{project-name}-review.md canvas and requires user confirmation after mode selection before starting research rounds.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
