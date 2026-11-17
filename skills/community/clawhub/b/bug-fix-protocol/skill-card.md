## Description:

Structured protocol for fixing bugs with AI agents. Prevents hallucinations and fix loops by enforcing step-by-step diagnosis before code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borodich](https://clawhub.ai/user/borodich)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when debugging errors, fixing broken code, recovering from fix loops, or auditing test coverage after an incident. It guides the agent to reproduce the bug with a failing test, find the root cause, make minimal code changes, update the test system, and document the fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill during debugging can lead an agent to read related code, change bug-related code, add or update tests, run tests, and document the fix.

Mitigation: Review proposed code and test changes before deployment, and run the relevant test suite before accepting the fix.

Risk: Most instructions are in Russian, which can make review harder for teams that do not read Russian.

Mitigation: Have a Russian-speaking reviewer or a trusted translation workflow confirm the checklist expectations before operational use.

## Reference(s):

- [BUG-FIX-PROTOCOL source](https://github.com/CodeAlive-AI/ai-driven-development/blob/main/BUG-FIX-PROTOCOL.md)
- [ClawHub skill page](https://clawhub.ai/borodich/skills/bug-fix-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with checklists, templates, code changes, tests, and shell commands as needed during debugging]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most instructions are in Russian; outputs depend on the target repository and bug report.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
