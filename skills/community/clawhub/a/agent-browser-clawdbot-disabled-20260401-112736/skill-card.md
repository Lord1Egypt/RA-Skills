## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmundi3210](https://clawhub.ai/user/tmundi3210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows through the agent-browser CLI, especially when deterministic element selection, session isolation, state persistence, and scripted interactions are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent authenticated browser state can expose cookies, storage, or privileged sessions if files are committed, logged, or reused broadly.

Mitigation: Store browser state files like secrets, keep them out of repositories and logs, delete them after use, and prefer isolated test accounts or containers.

Risk: Automated browser actions can operate against live accounts or sensitive applications with unintended effects.

Mitigation: Review workflows before execution and use trusted, scoped sessions for authenticated automation.

## Reference(s):

- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the agent-browser command-line tool and may produce browser state files, screenshots, PDFs, and JSON snapshots when used by an agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
