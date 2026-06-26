## Description: <br>
AI Orchestrator lets agents send prompts to DeepSeek through Puppeteer browser automation with session support, fast daemon startup, health checks, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to request DeepSeek assistance for code analysis, review, generation, text analysis, summarization, and translation through an authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, pasted code, and stdin content are sent to DeepSeek through an automated logged-in browser. <br>
Mitigation: Review content before sending, avoid secrets or regulated data, and use a dedicated DeepSeek account and browser profile. <br>
Risk: Persistent browser profile, session, and diagnostic artifacts may contain sensitive local state or captured page content. <br>
Mitigation: Keep the skill directory private and clear `.profile/`, `.sessions/`, and `.diagnostics/` when the session is no longer needed. <br>
Risk: Daemon management and recovery commands may restart browser automation or affect related local processes. <br>
Mitigation: Prefer manual daemon startup unless persistence is needed, and review broad recovery commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ciklopentan/ai-orchestrator) <br>
- [Operator manual](REFERENCE.md) <br>
- [Phase 1 manual](PHASE1-MANUAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses from DeepSeek, with optional CLI diagnostics and local diagnostic files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports named sessions, daemon-backed execution, dry-run checks, and diagnostic traces.] <br>

## Skill Version(s): <br>
2.0.11 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
