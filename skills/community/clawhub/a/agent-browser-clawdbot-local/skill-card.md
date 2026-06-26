## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reknottycat](https://clawhub.ai/user/reknottycat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive headless browser workflows through deterministic accessibility-tree snapshots, ref-based element selection, session isolation, and browser state inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser login state, cookies, localStorage values, and saved state files can contain sensitive credentials or session material. <br>
Mitigation: Use test accounts or intentionally created automation sessions, treat saved state files as credentials, avoid sharing or committing them, and delete them after use. <br>
Risk: Attaching automation to a personal logged-in browser can allow the agent to operate in that session. <br>
Mitigation: Attach only to sessions where agent operation is intended, and prefer isolated browser sessions for workflows that involve authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reknottycat/agent-browser-clawdbot-local) <br>
- [agent-browser project](https://github.com/vercel-labs/agent-browser) <br>
- [Publisher profile](https://clawhub.ai/user/reknottycat) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent-browser command-line tool and may produce browser snapshots, extracted page content, screenshots, PDFs, cookies, storage values, and saved browser state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
