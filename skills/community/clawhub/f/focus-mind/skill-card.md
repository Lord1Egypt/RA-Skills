## Description: <br>
FocusMind helps agents analyze long or messy conversation context, estimate context health, extract active goals, and generate summaries or cleanup recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiaoni](https://clawhub.ai/user/hongjiaoni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to inspect conversation or project context, identify when context is becoming unclear, and produce summaries, goal lists, and cleanup guidance for long-running agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation or project context may be analyzed, saved, exported, or sent through webhook notifications. <br>
Mitigation: Use the skill only with context you are comfortable processing or saving, review export paths before use, and enable webhook notifications only for trusted endpoints. <br>
Risk: Interactive load, save, and export commands can read from or overwrite files accessible to the running process. <br>
Mitigation: Run the skill with least-privilege filesystem access and verify file paths before using REPL load/save or report export features. <br>


## Reference(s): <br>
- [FocusMind design patterns](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/hongjiaoni/focus-mind) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Guidance] <br>
**Output Format:** [Console text, Markdown reports, JSON data, or HTML exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are rule-based context health assessments, summaries, extracted goals, recommendations, and optional exported report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
