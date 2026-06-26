## Description: <br>
Add text to today's daily note in FocusNote as a new bullet point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trongnguyen29](https://clawhub.ai/user/trongnguyen29) <br>

### License/Terms of Use: <br>


## Use Case: <br>
FocusNote users and coding agents use this skill to append user-provided text as a bullet in today's local FocusNote daily note, creating the note if needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script writes to local FocusNote daily note files. <br>
Mitigation: Confirm the exact text and that it should be appended to today's FocusNote daily note before running the script. <br>
Risk: FocusNote must be running and its local documents path must be available. <br>
Mitigation: Check that FocusNote is running and that the documents-path file exists before attempting the write. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/trongnguyen29/focusnoteapp) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to append user-provided text to the user's local FocusNote daily note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
