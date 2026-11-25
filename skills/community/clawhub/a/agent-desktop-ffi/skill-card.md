## Description:

Provides C-ABI bindings to agent-desktop's PlatformAdapter so language runtimes can call desktop automation operations through a shared library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Python, Swift, Node, Go, C++, or Ruby can link the shared library and call its C ABI to observe desktop applications and dispatch UI actions without starting a CLI process for each call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, leaving some referenced material unreviewed.

Mitigation: Review the referenced material before relying on the skill in a deployment.

Risk: UI actions can affect the focused desktop application, and targets may change after observation.

Mitigation: Check the current snapshot and qualified target before dispatching each action.

Risk: Diagnostic details can include names, values, or window titles from the user's screen.

Mitigation: Keep error details out of shared logs and redact them before sharing.

## Reference(s):

- [Build and link guide](artifact/references/build-and-link.md)
- [Error handling guide](artifact/references/error-handling.md)
- [Pointer ownership guide](artifact/references/ownership.md)
- [Threading guide](artifact/references/threading.md)
- [Apple Thread Safety Summary](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/ThreadSafetySummary/ThreadSafetySummary.html)
- [ClawHub release page](https://clawhub.ai/lahfir/skills/agent-desktop-ffi)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with C, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API usage guidance and examples; no fixed output size.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
