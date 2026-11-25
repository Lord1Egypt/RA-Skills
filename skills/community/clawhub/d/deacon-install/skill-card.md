## Description:

Install the Deacon support widget on a website or web app: place one script tag on every page, tell Deacon who is signed in, and confirm from the command line that a real page has loaded it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewcathcart](https://clawhub.ai/user/andrewcathcart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Deacon's support widget to a website or web app, pass appropriate signed-in user context, and confirm that a real page has loaded the widget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete: static analysis was limited and many local path-like references could not be resolved.

Mitigation: Review the referenced source files and proposed changes before applying the installation.

Risk: Identity and context values placed in page scripts are readable by visitors.

Mitigation: Include only appropriate support context; keep passwords, tokens, and API keys out, and safely serialize user-provided values.

## Reference(s):

- [Deacon](https://heydeacon.com)
- [Deacon account registration](https://heydeacon.com/register)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, and framework-specific code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover common web frameworks and installation verification; user and context values should come from the site's existing session.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
