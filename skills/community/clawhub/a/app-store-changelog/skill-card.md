## Description: <br>
Create user-facing App Store release notes by collecting and summarizing user-impacting changes since the last git tag or a specified ref. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dimillian](https://clawhub.ai/user/Dimillian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release managers use this skill to turn local git history into concise App Store changelog bullets that focus on user-visible additions, improvements, and fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collecting changes from a private repository can expose commit subjects and touched file names from the selected git range. <br>
Mitigation: Run the collection script only in the intended repository and pass a specific starting tag or ref when limiting history is important. <br>
Risk: Generated App Store notes may include internal-only or overstated changes when commit history is ambiguous. <br>
Mitigation: Review each bullet against the collected commits and files, and ask for clarification before including uncertain changes. <br>


## Reference(s): <br>
- [App Store Release Notes Guidelines](artifact/references/release-notes-guidelines.md) <br>
- [collect_release_changes.sh](artifact/scripts/collect_release_changes.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown bullet list with optional title and supporting shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Release-note bullets should map to real changes in the selected git range and avoid internal-only details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
