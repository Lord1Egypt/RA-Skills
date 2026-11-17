## Description:

Brake guides an agent through collecting brake design parameters, calling the JXT mechanical-parts API, reviewing calculated CAD parameters, and creating a guest production sheet for generated drawings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineers use this skill to select a brake product, provide design inputs step by step in Chinese, review calculated parameters, and create a guest link for CAD drawing production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brake design parameters are sent to jixietools.com.

Mitigation: Install and use the skill only when sharing those design parameters with that third-party service is acceptable.

Risk: The workflow uses raw shell commands with user-supplied values.

Mitigation: Use a native HTTP client or safely constructed argument arrays, and avoid interpolating untrusted input into shell commands.

Risk: Generated guest links, guest codes, and filename handles can expose workflow state or generated output.

Mitigation: Treat those values as sensitive references and share them only with intended recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/brake)
- [Jixietools API base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese conversational guidance with Markdown tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guest production-sheet links and status updates; does not create local files itself.]

## Skill Version(s):

1.0.1 (source: release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
