## Description:

C Language Support Library for OpenClaw skills. Provides AST parsing, CMake analysis, Unity test generation, and security rule checking for C projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as shared C-language infrastructure for agent workflows that parse C source, analyze CMake projects, generate Unity test scaffolds, and check C code against security rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad tool authority and generated build or test files create review-worthy risk on untrusted C/CMake projects.

Mitigation: Install only when C/CMake project analysis and test/build generation are expected, and review generated C and CMake before building or executing them.

Risk: Dependency choices or build integration may introduce unreviewed code into downstream projects.

Mitigation: Pin Python dependencies and replace FetchContent tags with reviewed commits or vendored dependencies where applicable.

## Reference(s):

- [C Support Library on ClawHub](https://clawhub.ai/michealxie001/skills/c-support)
- [CWE-120: Buffer Copy without Checking Size of Input](https://cwe.mitre.org/data/definitions/120.html)
- [CWE-134: Use of Externally-Controlled Format String](https://cwe.mitre.org/data/definitions/134.html)
- [CWE-242: Use of Inherently Dangerous Function](https://cwe.mitre.org/data/definitions/242.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python usage examples and generated C, CMake, or Unity test code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read C/CMake project files and produce generated test or build artifacts for review before use]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
