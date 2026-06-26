## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmundi3210](https://clawhub.ai/user/tmundi3210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to drive deterministic browser automation workflows, including navigation, form interaction, session isolation, state persistence, screenshots, PDFs, network control, cookies, storage, tabs, and frames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can access authenticated pages, cookies, local storage, and saved session files. <br>
Mitigation: Use isolated sessions, avoid using a real Chrome profile for routine automation, and treat auth.json or saved state files like passwords. <br>
Risk: Persisted browser state can expose credentials or private browsing context if shared or committed. <br>
Mitigation: Keep session files out of source control, store them in protected locations, and delete persisted sessions when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tmundi3210/agent-browser-clawdbot-disabled-20260401-112736) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing command guidance for the external agent-browser CLI; browser state files may contain sensitive session data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
