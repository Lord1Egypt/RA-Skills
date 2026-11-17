## Description:

Expert Dust Language Architect grounded in the full Dust ecosystem, with the Dust Programming Language Specification as canon and all dustlang organization repositories treated as supporting corpus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litecreator](https://clawhub.ai/user/litecreator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation writers, and language-design reviewers use this skill to interpret the Dust programming language from the packaged Dust ecosystem repositories, with the Dust specification treated as canon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to read all files packaged under the Dust skill directory, which could expose unrelated sensitive material if such files are included.

Mitigation: Package only intended Dust reference repositories and exclude secrets, tokens, private environment files, and unrelated repositories before deployment.

Risk: Repository-grounded language guidance can become misleading if the packaged corpus is stale, incomplete, or internally inconsistent.

Mitigation: Review outputs against the canonical Dust specification and current packaged repositories, especially when using the skill for implementation or documentation decisions.

## Reference(s):

- [Dust Language Architect on ClawHub](https://clawhub.ai/litecreator/skills/dust-language-architect)
- [Dust Programming Language Specification](https://github.com/dustlang/dustlang)
- [Dust Compiler Repository](https://github.com/dustlang/dust)
- [Dust Website Repository](https://github.com/dustlang/dustlang.github.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text with optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-grounded responses should separate canonical specification facts from implementation, examples, public documentation, and unresolved ambiguity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
