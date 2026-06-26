## Description: <br>
Apple Mail Search Safe.Bak helps agents search local Apple Mail metadata and retrieve message bodies on macOS using the fruitmail CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellohushuai](https://clawhub.ai/user/hellohushuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to have an agent find Apple Mail messages by subject, sender, recipient, date, or unread status, open messages in Mail.app, and read message bodies when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searching and reading Apple Mail can expose sensitive local email content to the agent. <br>
Mitigation: Install only when local email access is intended, use narrow searches and result limits, and avoid requesting unnecessary message bodies. <br>
Risk: The reviewed skill artifact depends on an external npm CLI implementation. <br>
Mitigation: Verify the npm package and repository source before installation, and prefer copy mode when querying mail data. <br>


## Reference(s): <br>
- [Apple Mail Search Safe.Bak on ClawHub](https://clawhub.ai/hellohushuai/apple-mail-search-safe-bak) <br>
- [apple-mail-search-cli npm package](https://www.npmjs.com/package/apple-mail-search-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only Apple Mail search; supports read-only queries, optional database copy mode, and result limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
