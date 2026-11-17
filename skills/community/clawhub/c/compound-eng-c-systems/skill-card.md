## Description:

C patterns for systems code, libraries, and native extensions: module layout, function decomposition, status-enum errors, memory safety, undefined behavior, and performance measurement. Use when writing, reviewing, refactoring, or debugging C, working with malloc lifetimes, buffer overflows, sanitizers, or Valgrind, or building native extensions. For C++, see ia-cpp-systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing, reviewing, refactoring, or debugging C11 and later systems code, libraries, and native extensions. It provides repository-aware guidance on code structure, errors, memory safety, undefined behavior, and build and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign result with medium confidence and a partial scan because two local references could not be resolved.

Mitigation: Review the unresolved references and decide whether the additional skill evaluation commands suit your environment before installing.

## Reference(s):

- [Build and measurement](artifact/references/build-and-measurement.md)
- [Correctness traps](artifact/references/correctness-traps.md)
- [Implementation structure](artifact/references/implementation-structure.md)
- [Legibility standard](artifact/references/legibility-standard.md)
- [Memory safety](artifact/references/memory-safety.md)
- [PHP extension C guidance](artifact/references/php-extension-c.md)
- [Runtime safety](artifact/references/runtime-safety.md)
- [write-legible-c reference](https://github.com/7etsuo/write-legible-c)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with C snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapted to the repository's conventions and the requested C task.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
