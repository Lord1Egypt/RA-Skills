## Description: <br>
Converts ICS calendar files to structured JSON for Feishu calendar integration, including merged event exports or per-file JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to convert locally synced ICS calendar files into JSON for Feishu calendar workflows, event import or export, and downstream calendar processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar exports may contain private event details such as titles, organizers, times, and reminders. <br>
Mitigation: Run the converter only on intended local calendar folders and review generated JSON before sharing or importing it. <br>
Risk: Split output writes JSON files beside matching ICS files, which can place generated calendar data in the source directory tree. <br>
Mitigation: Use a narrow input directory and confirm generated files are stored only where calendar data is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/feishu-candy) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON files with Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can merge all parsed events into one JSON file or split output into one JSON file per ICS file.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
