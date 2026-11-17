## Description:

Write safe C++ avoiding memory leaks, dangling pointers, undefined behavior, and ownership confusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a C++ safety reference when reviewing or drafting code that involves ownership, memory management, class design, STL usage, templates, concurrency, modern C++ features, and undefined behavior traps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inform generated C++ that still contains memory-management or ownership mistakes.

Mitigation: Review generated changes manually and validate them with compiler warnings, sanitizers, static analysis, and tests before use.

Risk: Concurrency guidance may be applied incorrectly, leaving data races, deadlocks, or undefined behavior.

Mitigation: Require project-specific concurrency review and runtime testing for code involving threads, mutexes, atomics, or condition variables.

## Reference(s):

- [Memory Traps](artifact/memory.md)
- [Pointer Traps](artifact/pointers.md)
- [Class Traps](artifact/classes.md)
- [STL Traps](artifact/stl.md)
- [Template Traps](artifact/templates.md)
- [Concurrency Traps](artifact/concurrency.md)
- [Modern C++ Traps](artifact/modern.md)
- [Undefined Behavior Traps](artifact/ub.md)
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/cpp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with C++ examples and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory reference output; users should review generated C++ changes with compiler diagnostics, sanitizers, and project-specific tests.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
