## Description:

Deploy frontend and full-stack projects to EdgeOne Pages (Tencent EdgeOne), including CLI setup, login selection, deployment commands, and deployment URL reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentism](https://clawhub.ai/user/vincentism)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy frontend or full-stack projects to Tencent EdgeOne Pages, choosing the correct China or Global site, authenticating with browser or token flows, and returning complete deployment and console URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle account-level EdgeOne API tokens during token-based deployments.

Mitigation: Prefer browser login when available, provide tokens only when needed, and rotate any token exposed to an agent session.

Risk: Saved tokens in `.edgeone/.token` can be exposed if committed, synced, or shared with the project.

Mitigation: Avoid saving tokens unless necessary, verify `.edgeone/.token` is ignored by version control, and check that token files are not copied to shared environments.

Risk: Deployment URLs may include credentialized `eo_token` and `eo_time` query parameters.

Mitigation: Treat complete deployment URLs as sensitive links and share them only with intended recipients.

## Reference(s):

- [EdgeOne Pages China console settings](https://console.cloud.tencent.com/edgeone/pages?tab=settings)
- [EdgeOne Pages Global console settings](https://console.intl.cloud.tencent.com/edgeone/pages?tab=settings)
- [ClawHub skill page](https://clawhub.ai/vincentism/skills/edgeone-pages-deploy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks and deployment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local EdgeOne configuration files when the user chooses token persistence.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
