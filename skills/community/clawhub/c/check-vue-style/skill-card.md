## Description:

Checks CSS style conventions in Vue single-file components and reports warnings for issues such as missing scoped styles, excessive !important usage, ID selectors, deep selectors, non-kebab-case class names, and overly deep nesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueguangshun123](https://clawhub.ai/user/yueguangshun123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Vue single-file components for common CSS style convention issues and to get file-and-line warnings with suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the checker from the wrong directory may scan more local Vue files than intended.

Mitigation: Run it from the intended project root so it only reads the workspace meant for inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yueguangshun123/skills/check-vue-style)
- [Bundled Vue style checker script](artifact/scripts/check-vue-style.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and line-based warning output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Warnings use file path, line number, and Chinese issue text; a nonzero script exit indicates style findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
