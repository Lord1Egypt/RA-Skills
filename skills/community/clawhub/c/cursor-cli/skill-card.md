## Description: <br>
Use Cursor editor and Cursor agent for coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyavchik](https://clawhub.ai/user/pyavchik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to open files in Cursor, compare files, and ask Cursor Agent coding questions from a project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor Agent prompts or reviewed code may include sensitive private information. <br>
Mitigation: Avoid sending secrets or sensitive private code unless Cursor's data handling is acceptable for the project. <br>
Risk: Filenames and prompts are passed through shell commands. <br>
Mitigation: Use normal shell quoting hygiene for filenames and prompts. <br>
Risk: The agent can provide advice when the user only wants analysis. <br>
Mitigation: Prefer explicit ask mode when requesting guidance without changes. <br>


## Reference(s): <br>
- [Cursor CLI documentation](https://cursor.com/docs/cli/overview) <br>
- [ClawHub skill page](https://clawhub.ai/pyavchik/cursor-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cursor and cursor-agent command-line tools.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
