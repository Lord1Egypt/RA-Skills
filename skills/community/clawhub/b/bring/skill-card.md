## Description: <br>
Manage Bring! shopping lists - view, add, and remove grocery items from shared shopping lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GrewingM](https://clawhub.ai/user/GrewingM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to view, add, remove, and organize items in shared Bring! shopping lists, including multilingual household lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Bring login credentials in a local configuration file. <br>
Mitigation: Use only on trusted machines, protect or remove ~/.openclaw/bring/config.json when no longer needed, and change the Bring password if the file or shell history may have been exposed. <br>
Risk: The skill can access and change shared Bring! shopping lists. <br>
Mitigation: Install only when the user is comfortable granting access to the Bring account and shared lists, and review list-changing actions before execution. <br>
Risk: The skill depends on the globally installed bring-shopping npm package. <br>
Mitigation: Verify the package before installing it globally and keep the runtime environment limited to trusted agent sessions. <br>


## Reference(s): <br>
- [Bring API Reference](references/api.md) <br>
- [bring-shopping npm package source](https://github.com/foxriver76/node-bring-api) <br>
- [ClawHub skill page](https://clawhub.ai/GrewingM/bring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or modify Bring! shopping lists after the user configures Bring credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
