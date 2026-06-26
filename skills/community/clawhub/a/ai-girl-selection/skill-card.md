## Description: <br>
Selects three local AI-generated girl portrait images for review, lets the user choose one, and saves the selected image as the current OpenClaw avatar while recording the preference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FrankChi2022](https://clawhub.ai/user/FrankChi2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users with a local image library use this skill to preview three random AI portrait images, choose a preferred image, update the daily avatar, and keep a lightweight preference record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the release suspicious because scripts read from hard-coded local image paths and overwrite avatar and preference files with limited user control. <br>
Mitigation: Review and adjust the configured source, workspace, avatar, and preference paths before installation or execution, then run the scripts only in a workspace where overwriting those files is acceptable. <br>
Risk: The security guidance notes that the numeric selection mapping should be fixed before relying on the workflow. <br>
Mitigation: Validate that each displayed candidate maps to the selected file before using the skill to update an avatar. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FrankChi2022/ai-girl-selection) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Terminal text plus a generated HTML preview page, copied image files, and a local Markdown preference file containing structured status data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 according to metadata; scripts use Bash/macOS commands, hard-coded local paths, and local image files.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
