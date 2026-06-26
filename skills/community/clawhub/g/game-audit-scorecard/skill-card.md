## Description: <br>
Summarize audit findings into a structured multi-dimensional scorecard for UI/UX, feedback, mechanics, scope completeness, maintainability, and live risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game teams use this skill to turn game audit findings into consistent, evidence-based scorecards and audit summaries for browser or project-local games. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update project-local audit documentation, including existing scorecard or audit summary files. <br>
Mitigation: Use it only in game projects where file reads and writes are acceptable, and review generated diffs before committing. <br>


## Reference(s): <br>
- [Game Audit Scorecard on ClawHub](https://clawhub.ai/mike007jd/game-audit-scorecard) <br>
- [Audit confidence and evidence reference](shared/reference/audit-confidence-and-evidence.md) <br>
- [Audit scorecard template](shared/templates/audit-scorecard.md) <br>
- [Audit scorecard schema](schemas/audit-scorecard.schema.json) <br>
- [Usage examples](examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown audit summary and JSON scorecard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local audit outputs under docs/game-studio/audit/ when file access is available.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and MANIFEST.yaml; release metadata version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
