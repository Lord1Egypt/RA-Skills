## Description: <br>
Extracts the repeatable player action-feedback-reward-motivation loop from a game, feature set, or pitch and identifies where the loop is weak, bloated, or incomplete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game designers, product teams, and developers use this skill to clarify the real repeatable loop behind a game concept, feature set, prototype, or pitch. It produces a structured diagnosis of loop steps, motivational drivers, weak points, and practical design implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may produce an incorrect or misleading core-loop diagnosis if the user provides incomplete game, prototype, or playtest evidence. <br>
Mitigation: Require outputs to state assumptions, tie conclusions to provided design evidence, and be reviewed by the design team before product changes are made. <br>
Risk: Recommendations may over-simplify a design by treating progression, economy, retention, or social loops as secondary when they are important to the product goal. <br>
Mitigation: Review the extracted top-level loop against supporting loops and business goals before cutting or de-prioritizing systems. <br>


## Reference(s): <br>
- [Family Conventions](artifact/references/family-conventions.md) <br>
- [Output Patterns](artifact/references/output-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stanestane/game-design-core-loop-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown with structured diagnostic sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default sections cover extraction target, extracted core loop, loop step breakdown, loop drivers, loop breaks, design implications, and a minimal loop fix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
