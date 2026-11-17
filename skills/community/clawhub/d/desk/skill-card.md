## Description:

Optimized desktop automation with mouse, keyboard, screen, window, clipboard, and optional AI task-planning control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niveroviero](https://clawhub.ai/user/niveroviero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to script desktop workflows such as clicking, typing, screenshot capture, image matching, window activation, clipboard operations, and simple autonomous task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the live desktop through mouse, keyboard, window, and clipboard operations.

Mitigation: Run it in a disposable or low-privilege desktop session and enable failsafe and approval or confirmation modes for sensitive workflows.

Risk: Screenshots and clipboard contents may expose passwords, private documents, chats, or financial and account data.

Mitigation: Avoid using the skill while sensitive content is visible or copied, and clear or isolate the clipboard before automation.

Risk: Optional LLM planning can send screenshots and task text to the configured LLM client and can turn generated plans into desktop actions.

Mitigation: Connect an LLM client only when that data sharing and execution model is acceptable, and require human confirmation for LLM-derived steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niveroviero/skills/desk)
- [AI Agent Guide](artifact/AI_AGENT_GUIDE.md)
- [Quick Reference](artifact/QUICK_REFERENCE.md)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate desktop action plans and task status summaries when the optional AI agent layer is used.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
