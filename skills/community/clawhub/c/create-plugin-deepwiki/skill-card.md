## Description:

Create minimal, convention-matching plugins or extensions for an existing codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyharry](https://clawhub.ai/user/hyharry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add small plugins, extensions, custom modules, integrations, or add-ons to existing repositories while matching the host project's conventions. It guides the agent to inspect the repository and documentation first, plan a minimal implementation, add proportionate documentation, and state verification limits honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugin code or repository changes could be applied to a private, sensitive, or convention-heavy project without enough review.

Mitigation: Review generated code and proposed changes before applying them, limit repository access to what the task requires, and verify that the implementation follows the target project's documented extension patterns.

## Reference(s):

- [CAX plugin example: recrystallization grain growth](references/cax-recrystallization-example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, file edits, and concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated plugin files, minimal usage documentation, implementation plans, and review notes tailored to the target repository.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
