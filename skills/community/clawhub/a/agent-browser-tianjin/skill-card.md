## Description: <br>
A browser automation skill that helps agents navigate pages, inspect interactive elements, click, type, fill forms, capture page state, and manage browser sessions through the agent-browser CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate web workflows such as navigation, form filling, UI testing, structured data extraction, screenshots, recordings, and session reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can control authenticated browser sessions and perform actions such as submissions, uploads, purchases, posts, deletions, or account changes. <br>
Mitigation: Use isolated browser sessions and require explicit confirmation before high-impact actions. <br>
Risk: Saved state files, screenshots, PDFs, traces, and recordings can contain cookies, credentials, or private page data. <br>
Mitigation: Treat saved state and captured media as secrets, store them only in trusted locations, and delete them after use. <br>
Risk: The skill depends on the external agent-browser package for browser automation behavior. <br>
Mitigation: Install only when that dependency is trusted and keep the package reviewed and updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianjin-ren/agent-browser-tianjin) <br>
- [Publisher profile](https://clawhub.ai/user/tianjin-ren) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-oriented command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser session state and captured media may be written by the underlying CLI.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
