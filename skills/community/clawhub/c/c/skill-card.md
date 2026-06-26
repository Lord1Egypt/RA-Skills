## Description: <br>
Write safe C avoiding memory corruption, buffer overflows, and undefined behavior traps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this reference skill when asking agents for C guidance that avoids memory-management, pointer, string, integer, macro, and undefined-behavior mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated C guidance can still include unsafe string handling or memory-management mistakes if applied without review. <br>
Mitigation: Review generated C carefully, especially string handling, and prefer size-aware patterns with explicit null termination. <br>
Risk: This skill is a compact reference and may not cover project-specific compiler, platform, or coding-standard requirements. <br>
Mitigation: Validate recommendations against the target codebase, compiler diagnostics, tests, and applicable C standards before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/c) <br>
- [Memory Management Traps](memory.md) <br>
- [Pointer Traps](pointers.md) <br>
- [String Traps](strings.md) <br>
- [Type Traps](types.md) <br>
- [Preprocessor Traps](preprocessor.md) <br>
- [Undefined Behavior Traps](undefined.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with inline C examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference guidance; no hidden execution, data access, or persistence was found in security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
