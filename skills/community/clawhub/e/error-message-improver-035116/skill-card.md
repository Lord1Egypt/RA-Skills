## Description:

Helps application developers, support teams, SaaS operators, and users turn vague error messages into clearer explanations of what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and end users use this skill to rewrite or structure error messages so they explain the failure, likely cause, next action, assumptions, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation uses broad debugging and support keywords, so the skill may activate for general troubleshooting prompts.

Mitigation: Confirm the user wants error-message improvement before relying on the workflow, and review generated text before applying it to production user-facing copy.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-035116)
- [Dart SDK issue: `unawaited` should support `FutureOr`](https://github.com/dart-lang/sdk/issues/63818)
- [Dart language issue: const constructor initializer inference](https://github.com/dart-lang/language/issues/4728)
- [SegmentFault error-messages topic](https://segmentfault.com/t/error-messages)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise explanations, checklists, validation notes, and optional code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled; outputs should be reviewed before applying to production user-facing copy.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
