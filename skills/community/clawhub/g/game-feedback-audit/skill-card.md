## Description: <br>
Audit interaction feedback quality: input acknowledgment, hit/collect/reward/failure signaling, danger telegraphing, and state-transition clarity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game developers and reviewers use this skill to audit whether a game clearly responds to player actions and communicates consequences. It focuses findings on input acknowledgment, rewards, failures, danger telegraphing, state transitions, and evidence-backed confidence levels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write audit documents into the target repository when the agent has filesystem access. <br>
Mitigation: Keep access scoped to the intended game project and review changes under docs/game-studio/audit/ before committing them. <br>
Risk: Audit findings may be incomplete or misleading if runtime behavior cannot be observed directly. <br>
Mitigation: Require each important finding to include confidence and evidence, and prefer explicit uncertainty when proof is limited. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mike007jd/game-feedback-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/mike007jd) <br>
- [Feedback Audit Checklist](shared/checklists/feedback-audit-checklist.md) <br>
- [Game Feel Pillars](shared/checklists/game-feel-pillars.md) <br>
- [Audit Confidence and Evidence](shared/reference/audit-confidence-and-evidence.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown audit documents and JSON scorecard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audit-summary.md, ux-findings.md, and scorecard.json when the agent has repository write access.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
