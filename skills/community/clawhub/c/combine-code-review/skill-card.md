## Description:

Reviews Combine framework code for memory leaks, operator misuse, and error handling. Use when reviewing code with import Combine, AnyPublisher, @Published, PassthroughSubject, or CurrentValueSubject.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift Combine code for subscription retention, retain-cycle risks, operator misuse, threading issues, and error-handling mistakes. It is intended for focused code review of repositories or snippets that use Combine APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect repository snippets and surrounding Combine subscription storage.

Mitigation: Provide only repositories or snippets that are intended to be reviewed.

Risk: Review findings can overstate memory leaks or subscription safety when surrounding retention and capture-chain context is missing.

Mitigation: Require named files or types, explicit AnyCancellable retention checks, capture-chain confirmation for leak claims, and an unknown status with a request for more context when evidence is incomplete.

## Reference(s):

- [Combine Publishers](references/publishers.md)
- [Combine Operators](references/operators.md)
- [Combine Memory Management](references/memory.md)
- [Combine Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with file:line references and concise remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for surrounding Combine subscription storage when evidence is insufficient.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
