## Description: <br>
Launch Claude Code async in background with automatic delivery to Telegram/WhatsApp. Use for coding, refactoring, codebase research, file generation, and complex multi-step automations. NOT for quick one-off questions or real-time interactive tasks. Includes strict thread-safe routing + E2E operator validation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VsevolodUstinov](https://clawhub.ai/user/VsevolodUstinov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to launch longer-running Claude Code work in the background, track sessions, and receive progress or completion updates through Telegram or WhatsApp. It is intended for coding, refactoring, codebase research, file generation, and complex multi-step automation rather than quick interactive questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Claude Code in the background with broad local authority. <br>
Mitigation: Use a disposable or tightly scoped project directory, avoid sensitive files and secrets, and set short timeouts for risky work. <br>
Risk: Progress and results may be sent to Telegram or WhatsApp destinations. <br>
Mitigation: Verify the destination chat or thread before launch and review routing validation output before sharing task content. <br>
Risk: Messaging credentials or output handling may need review on shared or sensitive machines. <br>
Mitigation: Patch or avoid the temporary bot-token helper and run-task.sh before use in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VsevolodUstinov/claude-code-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include launch acknowledgments, session identifiers, logs, progress updates, completion summaries, generated files, or error/timeout notices.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
