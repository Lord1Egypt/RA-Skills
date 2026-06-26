## Description: <br>
Guides an agent through planning and writing a complete Chinese novel with user-selected genre, protagonist, conflict, chapter count, outlines, character files, chapter drafts, revision checks, and word-count validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckrissun](https://clawhub.ai/user/ckrissun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and writers use this skill to create long-form Chinese fiction by answering setup questions, reviewing an outline and character plan, then letting the agent draft and revise chapters in sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local novel project files. <br>
Mitigation: Use a dedicated workspace, choose a simple novel name, and check for existing files before starting. <br>
Risk: The workflow runs a bundled Python word-count checker. <br>
Mitigation: Review the helper script before use and run it only in the intended novel workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckrissun/chinese-novelist-skill) <br>
- [README](README.md) <br>
- [Chapter guide](references/chapter-guide.md) <br>
- [Chapter template](references/chapter-template.md) <br>
- [Character building](references/character-building.md) <br>
- [Character template](references/character-template.md) <br>
- [Consistency guide](references/consistency.md) <br>
- [Content expansion](references/content-expansion.md) <br>
- [Dialogue writing](references/dialogue-writing.md) <br>
- [Hook techniques](references/hook-techniques.md) <br>
- [Outline template](references/outline-template.md) <br>
- [Plot structures](references/plot-structures.md) <br>
- [Quality checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown story files, outline and character profile files, planning summaries, and Python word-count check commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local novels folder after user confirmation and checks chapter length with the bundled Python helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
