## Description: <br>
Monitor, control, and orchestrate background Codex sessions. Use this skill to track progress, handle interruptions, and ensure task completion for long-running coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Microcarft](https://clawhub.ai/user/Microcarft) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to supervise long-running Codex coding sessions, inspect progress, respond to prompts, resume interrupted work, and stop unresponsive sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad unattended control over Codex sessions and may allow an agent to continue work without enough review gates. <br>
Mitigation: Use it only when intentionally supervising autonomous Codex runs, keep work in a sandboxed repo or disposable branch, and review session logs before submitting input. <br>
Risk: Prompt responses such as generic approvals or blank submissions can approve unintended actions in an interactive Codex session. <br>
Mitigation: Avoid generic `y` or Enter approvals; inspect the prompt and provide specific input only when the requested action is understood. <br>
Risk: Background sessions may continue after the intended work is complete. <br>
Mitigation: Track session IDs and stop background sessions when work is finished or when a session becomes unresponsive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs, log excerpts, status summaries, and recommended control actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
