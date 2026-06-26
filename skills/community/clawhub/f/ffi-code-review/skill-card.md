## Description: <br>
Reviews Rust FFI code for type safety, memory layout compatibility, string handling, callback patterns, and unsafe boundary correctness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust FFI boundaries, including extern blocks, C-compatible layouts, bindgen output, callbacks, ownership transfer, and unsafe boundary documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce incorrect or misleading FFI review findings if it is used without reading the relevant crate context and source blocks. <br>
Mitigation: Follow the skill's gates before reporting findings: inspect Cargo.toml, linkage or binding sources, complete code evidence, and the pre-report verification protocol. <br>
Risk: Security scanning noted a false positive on a Rust safety-code example, so raw scanner output alone may overstate exploit behavior. <br>
Mitigation: Use the supplied security verdict and summary as authoritative, and review example code as instructional material rather than executable behavior. <br>


## Reference(s): <br>
- [Safety Patterns](references/safety-patterns.md) <br>
- [Type Mapping](references/type-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings with file-line references, severity labels, and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are gated by crate context, linkage review, code evidence, and a pre-report verification protocol.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
