## Description:

dotld helps agents search domain name availability and registration prices by running the dotld CLI against the Dynadot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedstonne](https://clawhub.ai/user/tedstonne)

### License/Terms of Use:

MIT

## Use Case:

Developers, founders, and naming teams use this skill to check exact domains, expand keywords across popular TLDs, compare USD registration prices, and prepare ranked domain options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation recommends installing dotld through an unverified remote installer.

Mitigation: Review before installing and prefer a pinned, verifiable dotld release instead of running the documented curl-to-bash command.

Risk: Using --dynadot-key can persist a Dynadot API key to local configuration with insufficiently restrictive permissions.

Mitigation: Prefer DYNADOT_API_PRODUCTION_KEY and avoid --dynadot-key until key storage uses restrictive permissions.

Risk: Domain searches are disclosed to Dynadot when the CLI queries availability and pricing.

Mitigation: Avoid searching confidential brands, product names, or unreleased project names unless disclosure to Dynadot is acceptable.

## Reference(s):

- [dotld CLI Reference](references/cli-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/tedstonne/skills/dotld)
- [Dynadot API Key Settings](https://www.dynadot.com/account/domain/setting/api.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and optional JSON result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Domain availability results can include USD prices, registration links, timestamps, and error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
