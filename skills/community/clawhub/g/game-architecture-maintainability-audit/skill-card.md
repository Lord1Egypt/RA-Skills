## Description: <br>
Audit architecture, state management, boundaries, coupling, and maintainability risks that will make future AI or human iteration harder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game developers and engineering teams use this skill to audit game project architecture, state management, module boundaries, coupling, and maintainability risks before future human or AI-assisted iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit files may be incomplete or misleading if the agent cannot inspect enough project files or local evidence. <br>
Mitigation: Grant appropriate file access for the audit and review the generated Markdown and JSON outputs against project evidence before relying on them. <br>
Risk: The skill is intended to modify files under docs/game-studio/audit/. <br>
Mitigation: Run it on a branch or review the generated audit documents before committing them. <br>


## Reference(s): <br>
- [Architecture Maintainability Audit Checklist](shared/checklists/architecture-maintainability-audit-checklist.md) <br>
- [Game-dev abstractions](shared/reference/game-dev-abstractions.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mike007jd/game-architecture-maintainability-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown audit documents and a JSON scorecard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended outputs are docs/game-studio/audit/audit-summary.md, docs/game-studio/audit/scorecard.json, and docs/game-studio/audit/risk-register.md when file access is granted.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
