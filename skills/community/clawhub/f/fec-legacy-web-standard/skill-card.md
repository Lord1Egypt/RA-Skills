## Description:

Guides developers in safely maintaining vanilla JavaScript, jQuery, HTML/CSS, and server-rendered frontend projects without changing their technology stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers maintaining legacy frontend applications use this skill for incremental changes to events, DOM updates, Ajax, accessibility, and input handling while preserving the existing stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad legacy frontend guidance may be mistaken for a migration, comprehensive security review, or validation workflow.

Mitigation: Use dedicated migration, security review, or validation workflows when those tasks are required.

Risk: Unsafe rendering of user input in legacy DOM updates can introduce XSS.

Mitigation: Escape untrusted input and avoid inserting it directly through innerHTML or jQuery .html().

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-legacy-web-standard)
- [Legacy maintenance patterns](references/legacy-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incremental changes that preserve existing frontend behavior and conventions.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
