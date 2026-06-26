## Description: <br>
Manage Things 3 on macOS through the `things` CLI, including reading local task views and adding or updating todos via the Things URL scheme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers on macOS use this skill to have an agent inspect Things 3 lists, search local tasks, and prepare `things` CLI commands to add or update todos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help read and change local Things 3 tasks when the generated commands are executed. <br>
Mitigation: Review commands before execution and use `--dry-run` before important task changes. <br>
Risk: Local database reads may require Full Disk Access for the calling app. <br>
Mitigation: Grant Full Disk Access only when needed and only to trusted applications. <br>
Risk: `THINGS_AUTH_TOKEN` or an auth token passed on the command line enables update operations. <br>
Mitigation: Treat the token as sensitive and avoid exposing it in shared logs or transcripts. <br>
Risk: The skill depends on the upstream `things3-cli` project. <br>
Mitigation: Install only if the upstream project is trusted. <br>


## Reference(s): <br>
- [Chen Things Mac on ClawHub](https://clawhub.ai/cs995279497-byte/chen-things-mac) <br>
- [things3-cli upstream project](https://github.com/ossianhempel/things3-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; commands may read local Things data or open Things URL-scheme actions when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
