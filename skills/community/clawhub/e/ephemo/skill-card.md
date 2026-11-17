## Description:

Publish files and folders to the web instantly. Static hosting for HTML sites and UI assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandrakottos](https://clawhub.ai/user/sandrakottos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish static web directories, prototypes, HTML sites, and UI assets to a live shareable URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to a public Ephemo URL.

Mitigation: Confirm the exact deployment directory first, remove secrets and dotfiles, avoid broad project roots, and prefer a clean build output folder.

Risk: Deployments run through mutable npm CLI code.

Mitigation: Review the proposed command and package before execution, and run it only in an environment where network access and publication are intended.

Risk: Cached Ephemo credentials can make deployments permanent.

Mitigation: Check whether the deployment reports authenticated permanence, and clearly tell the user when a URL is permanent or when an anonymous claim code expires.

## Reference(s):

- [Ephemo homepage](https://ephemo.online)
- [ClawHub skill listing](https://clawhub.ai/sandrakottos/skills/ephemo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and deployment URL handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a live URL handoff and may include claim-code or authentication-status guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
