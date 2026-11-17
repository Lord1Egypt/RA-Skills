## Description:

Guides agents in modern C++ development and review, including resource ownership, error handling, API and ABI boundaries, and CMake tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

C++ developers and engineers use this skill to write, review, refactor, and debug C++ code while respecting project conventions, ownership and lifetime rules, and API compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested C++ changes may introduce lifetime errors or break existing APIs and ABI.

Mitigation: Review changes against local project conventions and public interfaces; run relevant builds, tests, and sanitizers before adoption.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/iliaal/skills/compound-eng-cpp-systems)
- [Value and interface design](references/value-and-interface-design.md)
- [Concurrency and verification](references/concurrency-and-verification.md)
- [C++ API and ABI boundaries](references/api-and-abi.md)
- [CMake and C++ tooling](references/cmake-and-tooling.md)
- [C++ legibility](references/legibility-standard.md)
- [write-legible-c (attribution for legibility reference, not release provenance)](https://github.com/7etsuo/write-legible-c)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with C++ and shell snippets as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations follow the project's language standard and repository conventions.]

## Skill Version(s):

5.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
