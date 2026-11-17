## Description:

Control a Mac through natural language - open apps, click buttons, read the screen, type text, manage windows, and automate multi-step tasks via Airpoint's AI computer-use agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durtydhiana](https://clawhub.ai/user/durtydhiana)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to delegate supervised macOS desktop tasks to Airpoint through natural-language CLI commands, including opening apps, clicking UI elements, reading on-screen text, typing, managing windows, and checking results with screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Airpoint can view the screen and control mouse and keyboard input on macOS.

Mitigation: Use it only in supervised sessions, hide sensitive windows before use, and avoid tasks involving passwords, private messages, financial data, or admin prompts.

Risk: Fire-and-forget tasks can continue without the agent waiting for completion feedback.

Mitigation: Prefer synchronous `airpoint ask` for sensitive workflows and reserve `--no-wait` for low-risk tasks.

Risk: A desktop-control task may become stuck or act outside the intended workflow.

Mitigation: Monitor execution and use `airpoint stop` to cancel unexpected or stalled tasks.

## Reference(s):

- [Airpoint homepage](https://airpoint.app)
- [ClawHub skill page](https://clawhub.ai/durtydhiana/skills/airpoint-1-3-16)
- [ClawHub publisher profile](https://clawhub.ai/user/durtydhiana)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and plain-language task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Airpoint CLI may return a task summary and screenshot file paths for visual confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json version 1.3.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
