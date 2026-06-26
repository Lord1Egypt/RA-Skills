## Description: <br>
File Drop Organizer reviews a downloads or temporary folder and proposes categories, naming suggestions, duplicate risks, and a move plan before any action is taken. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and employees can use this skill to audit download or temporary directories and prepare a reviewable organization plan. It is suited for local file triage where the user wants categories, rename suggestions, duplicate-risk notes, and manual confirmation before any move. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads filenames and limited text content from the folder selected by the user. <br>
Mitigation: Run it first on Downloads or temporary folders, avoid broad or sensitive directories unless intentional, and review the generated report before acting. <br>
Risk: Generated move plans or naming suggestions may be incomplete or unsuitable for the user's files. <br>
Mitigation: Keep the default dry-run posture and require manual confirmation before moving, renaming, or otherwise changing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/file-drop-organizer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report by default, with optional JSON wrapping from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs directory overviews, suggested categories, duplicate-risk notes, naming recommendations, move plans, and manual confirmation items.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
