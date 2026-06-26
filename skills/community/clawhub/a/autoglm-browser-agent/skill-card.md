## Description: <br>
Autoglm Browser Agent delegates browser-based tasks such as web search, social media interaction, form filling, screenshots, shopping comparison, news reading, and online document operations to an autonomous browser subagent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhenghu](https://clawhub.ai/user/mrhenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to delegate browser-only workflows that require opening websites, searching, clicking, scrolling, collecting page content, completing forms, or returning screenshots. It is most relevant when a task needs interactive browser automation rather than local file processing or offline computation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control browser sessions and interact with signed-in accounts, including sensitive actions such as posting, liking, commenting, and messaging. <br>
Mitigation: Keep trust mode disabled for normal use, require user confirmation for sensitive actions, and avoid using the skill with financial or highly sensitive accounts. <br>
Risk: The skill depends on a Chrome extension plus local relay and server binaries that can persist browser state and screenshots. <br>
Mitigation: Install only when the publisher, extension, and local binaries are trusted; stop the relay and clear ~/.openclaw-autoclaw state after sensitive tasks. <br>
Risk: Screenshots and Feishu or instant-message integrations can expose page contents or account context outside the browser session. <br>
Mitigation: Review any Feishu or messaging credential setup before use and confirm that screenshot sharing is appropriate for the task. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mrhenghu/autoglm-browser-agent) <br>
- [AutoClaw Chrome Web Store extension](https://chromewebstore.google.com/detail/jelniggicmclhfgnlapbkgfibmgelfnp) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with browser task results, screenshot markdown, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser results must include screenshot markdown; setup and runtime behavior depend on mcporter, a local MCP server, a relay process, and a Chromium extension.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
