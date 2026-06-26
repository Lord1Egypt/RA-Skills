## Description: <br>
Manage Craft notes, documents, and tasks through a CLI for creating, searching, updating, and organizing Craft content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Noah-Ribaudo](https://clawhub.ai/user/Noah-Ribaudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Craft users use this skill to let an agent manage Craft documents, blocks, tasks, collections, and daily notes through Craft's CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and delete commands can change or remove Craft documents, blocks, and tasks. <br>
Mitigation: Preview targets and require user confirmation before deleting or changing important notes or tasks. <br>
Risk: The skill depends on a user-provided Craft Connect API URL. <br>
Mitigation: Have the user configure the Craft API URL explicitly and avoid exposing it in shared logs or transcripts. <br>


## Reference(s): <br>
- [Craft Notes on ClawHub](https://clawhub.ai/Noah-Ribaudo/craft) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Craft Connect API URL and can propose actions that create, update, complete, or delete Craft content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
