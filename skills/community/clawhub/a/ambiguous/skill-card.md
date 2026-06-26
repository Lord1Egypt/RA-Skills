## Description: <br>
Control an Ambiguous Workspace through the `ambiguous` CLI for tasks, docs, wiki, drive, calendar, CRM, mail, chat, authenticated API calls, and runtime command discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ambiguous](https://clawhub.ai/user/ambiguous) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to let an agent manage Ambiguous Workspace data through the `ambiguous` CLI. It is suited for authenticated workspace operations and command discovery across tasks, docs, wiki, drive, calendar, CRM, mail, and chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad authenticated workspace access can affect mail, docs, drive, calendar, CRM, and other workspace data. <br>
Mitigation: Use a dedicated low-privilege agent account and require human approval before deletes, mail sends, CRM or account changes, drive modifications, and other irreversible actions. <br>
Risk: The local API key is sensitive because it enables authenticated workspace operations. <br>
Mitigation: Protect ~/.ambi/config.json, avoid shared agent credentials, and rotate the key if the file is exposed. <br>
Risk: The CLI discovers live server operations, so available commands can change without a CLI upgrade. <br>
Mitigation: Check `--help` before unfamiliar operations and review newly exposed destructive or account-changing commands before execution. <br>


## Reference(s): <br>
- [Ambiguous homepage](https://ambi.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ambiguous/ambiguous) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npx; authenticated commands use the local Ambiguous config at ~/.ambi/config.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
