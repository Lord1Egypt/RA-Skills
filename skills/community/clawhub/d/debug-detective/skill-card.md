## Description:

Provides systematic debugging, diagnosis, and profiling workflows across application, system, network, database, and production issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure bug investigations, isolate regressions, profile performance, inspect frontend and backend behavior, and prepare targeted fixes with verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example commands may expose sensitive data if copied into real debugging sessions.

Mitigation: Review each command before running it, avoid real tokens in curl examples, and redact sensitive values from logs and shared outputs.

Risk: Packet captures, tracing, and diagnostic logs can contain credentials, personal data, or internal network details.

Mitigation: Protect and redact packet captures and logs before storing or sharing them.

Risk: Some examples install or run external debugging tools without pinning versions.

Mitigation: Prefer pinned versions and isolated environments when installing profiling or debugging utilities.

Risk: The scaffold script writes VS Code settings and helper scripts into a target project.

Mitigation: Inspect scaffold.sh and run it only in an intended project or disposable copy.

## Reference(s):

- [Debugging Workflow Checklist](examples/debug-checklist.md)
- [Chrome DevTools Cheatsheet](references/devtools-cheatsheet.md)
- [Profiling Tools Guide](references/profiling-tools-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/royhk920/skills/debug-detective)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic checklists, debugger commands, profiling steps, configuration snippets, and scaffolded helper script guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
