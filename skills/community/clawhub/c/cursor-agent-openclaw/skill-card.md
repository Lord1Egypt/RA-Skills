## Description: <br>
Run Cursor Agent CLI for coding tasks such as writing, editing, refactoring, reviewing, and planning code without spending OpenClaw API credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albinati](https://clawhub.ai/user/albinati) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route non-trivial coding work to Cursor Agent CLI, starting with read-only ask or plan mode and applying changes only after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit code after approval. <br>
Mitigation: Confirm each run, start in ask or plan mode, and review diffs before write mode or git push. <br>
Risk: Cloud/background mode can send repository contents to Cursor. <br>
Mitigation: Avoid cloud/background mode for private repositories unless sending code to Cursor is acceptable. <br>


## Reference(s): <br>
- [Cursor CLI documentation](https://cursor.com/docs/cli/overview) <br>
- [Cursor Agent models reference](references/models.md) <br>
- [Cursor Agent slash commands reference](references/slash-commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/albinati/cursor-agent-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Cursor Agent CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Cursor Agent CLI binary named agent; write mode and cloud/background mode require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
