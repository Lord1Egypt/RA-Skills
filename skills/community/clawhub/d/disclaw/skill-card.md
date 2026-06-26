## Description: <br>
Manage Discord workspace structure and OpenClaw routing as code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ofan](https://clawhub.ai/user/ofan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace administrators use this skill to create, rename, delete, validate, import, and roll back Discord categories, channels, threads, and OpenClaw agent-to-channel bindings from a YAML configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates Discord workspace and OpenClaw routing administration to a privileged external CLI. <br>
Mitigation: Verify the @ofan/disclaw npm package and publisher before installation, and use least-privilege Discord and gateway credentials. <br>
Risk: Applying changes with --yes or --prune can make real channel, thread, category, and routing changes. <br>
Mitigation: Run validate and diff before apply, review dry-run output, and use --prune only when deletion of unmanaged resources is intended. <br>
Risk: Misconfigured Discord or gateway credentials can expose more workspace control than the workflow needs. <br>
Mitigation: Scope bot permissions to the required server administration actions and protect Discord and gateway tokens in OpenClaw configuration. <br>


## Reference(s): <br>
- [Disclaw Skill Page](https://clawhub.ai/ofan/disclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/ofan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML and JSON configuration snippets, and operational checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides validation, diff, dry-run, apply, import, rollback, and pruning workflows for Discord and OpenClaw routing changes.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
