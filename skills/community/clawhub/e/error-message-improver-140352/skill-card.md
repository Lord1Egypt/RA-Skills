## Description:

Helps developers, support teams, SaaS operators, and users create clearer error messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to turn vague troubleshooting failures into actionable error-message wording, workflows, checklists, analysis, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation may route general debugging or support requests to this skill when the user did not specifically ask to improve error messages.

Mitigation: Use explicit invocation or route the skill only when the request is about error-message wording, troubleshooting feedback, support guidance, or related workflow artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-140352)
- [Requirement Plan](references/requirement-plan.md)
- [Provide better error messages for invalid assignment shorthands](https://github.com/gleam-lang/gleam/issues/5915)
- [Developer Onboarding Funnel Metrics with Dropoff Analysis](https://github.com/sethdford/shipwright/issues/746)
- [Clojure 1.13 adds support for checked keys](https://news.ycombinator.com/item?id=48806658)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with optional code, checklist, workflow, analysis, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce tailored artifacts and reusable workflows; no tool calls, credentials, or external services are required by the skill itself.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
