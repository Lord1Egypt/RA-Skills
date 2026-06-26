## Description: <br>
Novel Writer helps an agent continue a rebirth/transmigration web novel by reading story outlines, prior chapters, style samples, and memory files before drafting new chapters and updating continuity notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yisihenji1972](https://clawhub.ai/user/yisihenji1972) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers and agents can use this skill to draft long-form Chinese web novel chapters, preserve continuity across characters and plot lines, and keep local memory files current during ongoing story development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for recurring hourly writing, memory updates, and Desktop copies without clear opt-in or stop controls. <br>
Mitigation: Require explicit user opt-in before scheduled execution, constrain file access to the intended novel workspace, and provide a clear way to pause or stop recurring runs. <br>
Risk: Chapter generation and memory maintenance can overwrite or drift local story state. <br>
Mitigation: Review diffs before accepting file changes and keep backups of outlines, character notes, plot lines, settings, and generated chapters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain text with chapter drafts, outlines, continuity notes, and file-update guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local novel memory files and copy generated chapters to the Desktop when the agent is allowed to write files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
