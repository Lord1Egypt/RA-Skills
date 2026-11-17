## Description:

Use when building C++ applications requiring modern C++20/23 features, template metaprogramming, or high-performance systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhwa8685](https://clawhub.ai/user/lhwa8685)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design, implement, test, and optimize modern C++20/23 systems, including template-heavy code, memory-sensitive components, concurrent algorithms, and CMake-based builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated build files may include dependency or workflow references that are not hardened for production use.

Mitigation: Pin dependency versions or action SHAs, use lockfiles where possible, and review generated build configuration before merging.

Risk: Concurrent or lock-free C++ examples may be unsafe if copied directly into production systems without a reviewed memory reclamation strategy.

Mitigation: Require review by an experienced C++ engineer and use a proven safe reclamation approach before production use.

Risk: Performance-oriented examples may compile but still be unsuitable for a target platform or workload.

Mitigation: Run sanitizers, static analysis, tests, and representative benchmarks before accepting generated code.

## Reference(s):

- [Cpp Pro ClawHub Page](https://clawhub.ai/lhwa8685/skills/cpp-pro)
- [Modern C++20/23 Features](references/modern-cpp.md)
- [Template Metaprogramming](references/templates.md)
- [Memory Management & Performance](references/memory-performance.md)
- [Concurrency and Parallel Programming](references/concurrency.md)
- [Build Systems and Tooling](references/build-tooling.md)
- [fmt Git Repository](https://github.com/fmtlib/fmt.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with C++, CMake, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include header and implementation files, CMakeLists.txt updates, tests, design rationale, and performance notes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
