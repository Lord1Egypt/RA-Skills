## Description:

Rewrite vague application, API, CLI, and support errors into diagnostic messages that explain what failed, why it likely failed, and the next safe action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Product engineers, platform teams, support leads, technical writers, and SaaS operators use this skill to turn technically correct but vague failure states into actionable user-facing messages, structured payloads, support notes, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly around debugging, support, validation, or troubleshooting language.

Mitigation: Use it for rewriting user-facing error messages and review outputs before applying them to production copy, API responses, CLI text, or support workflows.

Risk: Troubleshooting inputs can include secrets, stack traces, sensitive logs, or internal implementation details.

Mitigation: Share only the context required for the rewrite and remove unnecessary secrets, raw stack traces, and sensitive logs before invoking the skill.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with before-and-after rewrites, structured payload patterns, implementation notes, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rationale, telemetry or support fields, localization or tone constraints, and validation notes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
