## Description:

Use this skill when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovemymobilewebsite-dotcom](https://clawhub.ai/user/lovemymobilewebsite-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to split unrelated debugging or implementation work across parallel subagents. It helps them define independent scopes, write focused prompts, review agent outputs, and integrate non-conflicting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel agents may produce conflicting or incorrect recommendations if tasks are not genuinely independent.

Mitigation: Use the skill only for independent workstreams and check returned summaries for overlapping files, shared state, or incompatible assumptions before integrating changes.

Risk: Agent outputs may introduce incorrect code or misleading guidance if accepted without review.

Mitigation: Review all agent outputs, scan relevant changes, and run the full applicable test suite before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovemymobilewebsite-dotcom/skills/dispatching-parallel-agents-2)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with prompt examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before integrating changes from parallel agents.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
