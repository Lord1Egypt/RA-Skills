## Description: <br>
Manages Cornell Method notes as Markdown files using a bundled CLI for creating, listing, viewing, searching, editing, and deleting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent can keep local Cornell-style study or meeting notes in a consistent Markdown format, then ask the agent to find, show, revise, or remove those notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates, searches, edits, and deletes local notes in ~/cornell-notes. <br>
Mitigation: Install it only when agent-accessible local notes are intended, and review edit or delete requests before allowing the command. <br>
Risk: Opening notes depends on the local editor selected by EDITOR or VISUAL, with a fallback editor if neither is set. <br>
Mitigation: Set EDITOR or VISUAL to a trusted editor and prefer running the bundled script from the skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/cornell-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown notes and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and manages local Markdown files in ~/cornell-notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
