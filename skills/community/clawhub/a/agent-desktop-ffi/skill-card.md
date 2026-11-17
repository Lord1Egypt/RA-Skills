## Description:

Guides developers in using C-ABI bindings to inspect and control desktop interfaces from host languages without spawning the agent-desktop CLI for each call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build language bindings and observe-act desktop automation with the agent-desktop FFI, including snapshots, element targeting, and actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop inspection and actions may expose or change sensitive on-screen content.

Mitigation: Install only when low-level desktop automation is intended; limit access to trusted applications and review actions before execution.

Risk: Snapshots, screenshots, clipboard reads, typed text, results, logs, and errors may contain sensitive information.

Mitigation: Treat these outputs as sensitive and avoid sending them to shared logs or untrusted recipients.

Risk: Optional tracing writes local diagnostic files that may persist after the session.

Mitigation: Enable tracing only when needed and plan how to protect and remove diagnostic files.

## Reference(s):

- [ClawHub release: agent-desktop-ffi](https://clawhub.ai/lahfir/skills/agent-desktop-ffi)
- [Build and link](artifact/references/build-and-link.md)
- [Pointer ownership](artifact/references/ownership.md)
- [Error handling](artifact/references/error-handling.md)
- [Threading](artifact/references/threading.md)
- [Apple Accessibility API](https://developer.apple.com/documentation/applicationservices/axuielement)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with C, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers ABI compatibility, pointer ownership, error handling, and threading.]

## Skill Version(s):

1.0.8 (source: server-resolved ClawHub release; skill frontmatter lists 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
