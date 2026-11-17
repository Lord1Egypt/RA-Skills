## Description:

Infer and refresh cspr user preference memory from browser-history evidence, notes, and feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happywalkers](https://clawhub.ai/user/happywalkers)

### License/Terms of Use:

MIT-0

## Use Case:

CSPR users and developers use this skill to refresh personalization by summarizing local browsing, notes, and feedback into durable preference memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan local browser history, notes, and feedback and write inferred preferences into persistent memory without default approval.

Mitigation: Require an explicit preview and approval step before applying profile updates.

Risk: Raw history artifacts and URL-derived records may expose sensitive personal browsing context.

Mitigation: Limit URL retention and delete raw history artifacts after profiling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happywalkers/skills/cspr-interest-profiler)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and YAML file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a run-folder profile.yaml for application with prefmem update.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
