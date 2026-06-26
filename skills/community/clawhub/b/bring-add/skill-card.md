## Description: <br>
Adds single, batch, stdin, file, or interactive items to Bring! shopping lists with dry-run preview and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darkdevelopers](https://clawhub.ai/user/darkdevelopers) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to add one or more items to Bring! shopping lists from a command-line workflow, including batch, stdin/file, interactive, dry-run, and JSON-output modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bring! account credentials are required to use the CLI. <br>
Mitigation: Treat BRING_EMAIL and BRING_PASSWORD as secrets; avoid shared shell history, CI logs, and committed files, and unset them after use. <br>
Risk: Items may be added to the wrong shopping list if the default or selected list is incorrect. <br>
Mitigation: Use the lists command to confirm available lists and use --dry-run before adding items when the target list is uncertain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/darkdevelopers/bring-add) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bring! account credentials in BRING_EMAIL and BRING_PASSWORD; supports dry-run mode before modifying a list.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
