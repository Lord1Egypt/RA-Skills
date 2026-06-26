## Description: <br>
Fast Apple Mail search via SQLite on macOS for finding messages by subject, sender, date, body, threads, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhlsthrm](https://clawhub.ai/user/rhlsthrm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to install and invoke a local Apple Mail search CLI for finding messages, threads, attachments, and body text without slow AppleScript enumeration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private local Apple Mail content to an agent session that invokes the installed command. <br>
Mitigation: Install only in trusted environments, grant Full Disk Access only to a trusted terminal, and use explicit prompts that limit searches to necessary messages. <br>
Risk: Broad exports or body reads can disclose more email content than intended. <br>
Mitigation: Prefer narrow search terms and result limits, avoid body reads unless needed, and review generated commands before execution. <br>


## Reference(s): <br>
- [Installation](references/install.md) <br>
- [ClawHub skill page](https://clawhub.ai/rhlsthrm/fruitmail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Text] <br>
**Output Format:** [Markdown guidance with bash command examples; the installed CLI can emit table text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Apple Mail data, sqlite3, python3, and Full Disk Access for the invoking terminal environment.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
