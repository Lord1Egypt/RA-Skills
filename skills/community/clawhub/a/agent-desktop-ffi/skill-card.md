## Description: <br>
C-ABI bindings over agent-desktop's PlatformAdapter let Python ctypes, Swift, Node ffi-napi, Go cgo, C++, and Ruby fiddle consumers link libagent_desktop_ffi and call ad_* functions directly instead of spawning the CLI binary per call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lahfir](https://clawhub.ai/user/lahfir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to integrate agent-desktop desktop automation through C ABI bindings while following build, threading, ownership, and error-handling constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Native desktop automation can expose screen content, clipboard text, action diagnostics, and accessibility permissions. <br>
Mitigation: Install only when native desktop FFI access is intentionally needed, keep calls user-directed, and keep screen-derived details out of shared logs. <br>
Risk: Host-process trust can broaden accessibility permission for interpreters or other processes that load the FFI library. <br>
Mitigation: Require explicit opt-in permission handling in host applications and document which executable receives desktop automation trust. <br>
Risk: Incorrect FFI threading or pointer ownership can cause failed calls, undefined behavior, or host instability. <br>
Mitigation: Follow the main-thread rules, pair every returned pointer or handle with its documented release function, and use the release-ffi build profile. <br>


## Reference(s): <br>
- [Build and link](references/build-and-link.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Pointer ownership](references/ownership.md) <br>
- [Threading](references/threading.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and C/Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes FFI safety constraints for main-thread access, memory ownership, error handling, and privacy-sensitive diagnostics.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter: 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
