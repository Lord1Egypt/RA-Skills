## Description:

Install the Deacon support widget on a website or web app: place one script tag on every page, tell Deacon who is signed in, and confirm from the command line that a real page has loaded it. Use when asked to install Deacon, add its snippet or embed code, or set it up on a site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewcathcart](https://clawhub.ai/user/andrewcathcart)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and web app teams use this skill to add the Deacon support widget to a site, connect signed-in user and app context where appropriate, and verify that the installation is live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can share signed-in customer identity, app context, and website telemetry with Deacon.

Mitigation: Only send fields needed for support, use the app's existing authenticated session, and preserve safe escaping and sign-out handling.

Risk: The widget uses browser storage, and installation may require Content Security Policy changes.

Mitigation: Disclose the storage used by the widget and review any CSP changes before deployment.

## Reference(s):

- [Deacon](https://heydeacon.com)
- [ClawHub skill release](https://clawhub.ai/andrewcathcart/skills/deacon-install)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with framework-specific code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts installation guidance to the site's framework, authentication, and deployment setup.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
