## Description: <br>
Apply DriveMind, the calm reliability layer for AI agents. Use when a task needs steady follow-through, clearer progress, stronger persistence without recklessness, explicit safety boundaries, human-in-the-loop collaboration, post-task review, reusable memory, or when the user says things like 'keep pushing', 'don’t stop too early', 'be steady', 'if risk is unclear ask me', 'review this after', or 'write down the lesson'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuzc-001](https://clawhub.ai/user/Yuzc-001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use DriveMind to make AI agents more persistent, structured, safety-aware, and review-oriented during important or blocked tasks. It is suited for workflows that need bounded follow-through, clearer progress updates, explicit escalation boundaries, and reusable post-task lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language may make ordinary agent tasks more persistent, structured, or review-oriented than an operator expects. <br>
Mitigation: Use explicit invocation or disable broad auto-activation when default agent behavior is preferred. <br>
Risk: Some safety and boundary reference files are written in Chinese, which may limit operator auditability for non-Chinese readers. <br>
Mitigation: Review the Chinese reference files directly or translate them before relying on the skill's safety rules in audited workflows. <br>


## Reference(s): <br>
- [DriveMind ClawHub Page](https://clawhub.ai/Yuzc-001/drivemind) <br>
- [DriveMind Skill Definition](artifact/SKILL.md) <br>
- [Decision Gates](artifact/references/decision-gates.md) <br>
- [Escalation Rules](artifact/references/escalation-rules.md) <br>
- [Mode Guide](artifact/references/mode-guide.md) <br>
- [Persistence Protocol](artifact/references/persistence-protocol.md) <br>
- [Review Style Guide](artifact/references/review-style-guide.md) <br>
- [Stuck Resolution](artifact/references/stuck-resolution.md) <br>
- [Task Typing](artifact/references/task-typing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, concise progress updates, escalation summaries, retrospectives, diary entries, and reusable lesson templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only workflow guidance; it changes collaboration style and does not provide tools, scripts, API calls, or direct system access.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
