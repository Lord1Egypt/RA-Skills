## Description: <br>
Self-review quality gate that uses Claude CLI to independently review an agent's completed work, check skill requirements and past lessons, and return severity-rated findings with a PASS/FAIL verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaperBoardOfficial](https://clawhub.ai/user/PaperBoardOfficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to run an independent Claude CLI review of generated or modified files before handing work to a user. It helps catch missed requirements, quality issues, and repeated mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review context can be sent to an external Claude-based review step and may include secrets or unrelated private data if paths are too broad. <br>
Mitigation: Keep review context paths narrow and avoid folders containing secrets or unrelated private data. <br>
Risk: Failed reviews can persist task details and issue notes locally in LESSONS.md. <br>
Mitigation: Inspect, constrain, or clear LESSONS.md when task details should not persist, and use LESSONS_FILE to choose an appropriate location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PaperBoardOfficial/claude-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain-text review report with severity-rated findings and a PASS/FAIL verdict, plus shell command invocation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append critical and major failure notes to LESSONS.md when a review fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact metadata declares 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
