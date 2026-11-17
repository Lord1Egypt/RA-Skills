## Description: <br>
Bookmark Smart Hub helps agents monitor bookmarks, analyze saved content with AI, send notifications, and search a local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and teams use this skill to automate bookmark monitoring, run AI-assisted content analysis, surface trends, send notifications, and build a searchable knowledge base from saved links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive social, AI, and notification credentials. <br>
Mitigation: Use test or least-privilege credentials, avoid browser session tokens where possible, and review credential storage before installation. <br>
Risk: Daemon mode and notification integrations can process bookmark content continuously and send information to external AI or messaging providers. <br>
Mitigation: Review the configured data flow and notification thresholds before enabling background execution or provider integrations. <br>
Risk: The release evidence flags broad command authority with unclear scoping and missing npm script/package source verification. <br>
Mitigation: Verify package contents and npm scripts before running setup, daemon, or PM2 commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local setup guidance, daemon management commands, AI analysis summaries, notification examples, and structured JSON-style results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
