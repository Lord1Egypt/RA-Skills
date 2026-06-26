## Description: <br>
WebDriver automation CLI for AI-driven browser control. Provides session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yorelog](https://clawhub.ai/user/yorelog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use BrowseCTL to automate browser sessions from the terminal, including navigation, element interaction, screenshots, tab management, batch execution, and REPL-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BrowseCTL can give an agent real browser-control authority, including access to logged-in browser state when copied into automation sessions. <br>
Mitigation: Use a dedicated automation browser profile and prefer --no-copy-data unless logged-in sessions are intentionally required. <br>
Risk: Browser state, sessions, screenshots, REPL history, and WebDriver processes may persist on disk or remain active after use. <br>
Mitigation: Periodically clear sessions, profiles, screenshots, REPL history, and WebDriver processes. <br>
Risk: Batch files and REPL input can execute browser actions that interact with sensitive sites or data. <br>
Mitigation: Review batch files before running them and avoid entering secrets in the REPL. <br>


## Reference(s): <br>
- [ClawHub BrowseCTL release](https://clawhub.ai/yorelog/browserctl) <br>
- [Publisher profile](https://clawhub.ai/user/yorelog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, command examples, JSON examples, and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-control commands that operate on local sessions and files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
