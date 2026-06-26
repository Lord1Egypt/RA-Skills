## Description: <br>
Manages a Notion-based agency dispatch board with slash commands for suggestions, discussions, task execution, recurring work, and corpus guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ratamaha-git](https://clawhub.ai/user/ratamaha-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and agent developers use this skill to run a Notion-backed work board: capture suggestions, clarify scope, launch approved agent work, track recurring tasks, and close work with result links. It is intended for teams that want Notion task state to stay authoritative while agents use local skill guidance and templates for execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a live Notion task board from loose chat phrases. <br>
Mitigation: Install only for the intended workspace, prefer slash commands for changes, and require explicit task IDs or confirmations for approve, done, kill, move, and run --go. <br>
Risk: The skill requires OAuth or sensitive Notion credentials. <br>
Mitigation: Keep the Notion integration limited to the intended workspace and share it only with the intended Tasks database. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ratamaha-git/agency-os) <br>
- [Public Notion template](https://www.notion.so/35dd01a02a8081dea01cd8d42617f0c8) <br>
- [general-guidance.md](references/general-guidance.md) <br>
- [task-page-template.md](references/task-page-template.md) <br>
- [corpus-template.md](references/corpus-template.md) <br>
- [config-template.json](references/config-template.json) <br>
- [notion-pointers.json](references/notion-pointers.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with slash commands, Notion links, JSON configuration, and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can mutate Notion task state through configured Notion tools and API access when the user invokes write commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
