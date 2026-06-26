## Description: <br>
Audit the project's audio layer as UX feedback: UI sounds, success/failure signals, danger cues, layering, and semantic sound priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Game developers and designers use this skill to audit whether UI sounds, reward cues, failure cues, danger signals, and audio layering improve player understanding rather than adding noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to read relevant game code and assets and write or update audit files. <br>
Mitigation: Run it only in projects where that read/write access is acceptable, and review generated audit files before relying on them. <br>
Risk: Findings may be inferred when runtime behavior is unclear. <br>
Mitigation: Keep confidence and evidence labels with each important finding so weak evidence is visible to reviewers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mike007jd/game-audio-feedback-audit) <br>
- [Audio Feedback Audit Checklist](artifact/shared/checklists/audio-feedback-audit-checklist.md) <br>
- [Audit Confidence and Evidence](artifact/shared/reference/audit-confidence-and-evidence.md) <br>
- [Usage Examples](artifact/examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, JSON, Guidance] <br>
**Output Format:** [Markdown audit notes and JSON scorecard updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs are project audit files under docs/game-studio/audit/ when write access is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
