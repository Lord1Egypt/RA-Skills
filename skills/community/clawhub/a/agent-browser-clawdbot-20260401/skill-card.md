## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dahai520520520](https://clawhub.ai/user/dahai520520520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to drive the agent-browser CLI for deterministic browser navigation, interaction, extraction, session isolation, and state persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state, cookies, and storage can contain sensitive credentials. <br>
Mitigation: Keep saved auth JSON files out of repositories and shared folders, and avoid printing or logging cookie or storage values. <br>
Risk: Browser automation commands can mutate sessions, cookies, storage, and network behavior. <br>
Mitigation: Use mutation and network-control commands only for sites and accounts the operator is authorized to automate or test. <br>
Risk: The skill depends on the upstream agent-browser npm package and Chromium download. <br>
Mitigation: Install only when the upstream package and browser runtime are trusted for the target environment. <br>


## Reference(s): <br>
- [Agent Browser project](https://github.com/vercel-labs/agent-browser) <br>
- [ClawHub skill page](https://clawhub.ai/dahai520520520/agent-browser-clawdbot-20260401) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on the agent-browser command, including snapshots, browser interaction commands, session handling, state files, screenshots, PDFs, and network controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
