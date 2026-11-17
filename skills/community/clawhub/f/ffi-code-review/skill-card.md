## Description:

Reviews Rust FFI code for type safety, memory layout compatibility, string handling, callback patterns, and unsafe boundary correctness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Rust FFI boundaries, including extern declarations, repr(C) layout, C string and pointer ownership, callback safety, bindgen output, and build/linkage configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-apply edition-specific Rust FFI rules if the reviewed crate edition is not checked first.

Mitigation: Follow Gate 1 by opening Cargo.toml and recording the crate edition before reporting edition-specific issues.

Risk: FFI findings can be inaccurate when based only on partial diffs or isolated snippets.

Mitigation: Follow Gate 3 by reading the full relevant function or block and citing a concrete file and line for each finding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/ffi-code-review)
- [Type Mapping](references/type-mapping.md)
- [Safety Patterns](references/safety-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with file-line citations and severity labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated on crate context, linkage and binding sources, and full code evidence before reporting.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
