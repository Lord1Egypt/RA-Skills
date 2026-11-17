## Description:

Configure development environments for Chinese developers by guiding agents to set up package mirrors, proxies, GitHub acceleration, Google service alternatives, and China-friendly project templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure development tooling for China-region network conditions, including package registries, Docker mirrors, GitHub access patterns, and service replacements.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Persistent global or system-wide routing changes can send future package installs, Git clones, Docker pulls, or CI builds through third-party infrastructure.

Mitigation: Review commands before execution, prefer per-project settings where possible, back up existing configuration, and apply global rewrites only when the operator intentionally wants China-region mirror or proxy behavior.

Risk: Mirror and proxy services can lag upstream registries or expose builds to unexpected package or image sources.

Mitigation: Pin package and image versions for CI or deployment use, verify the selected mirror source, and fall back to official registries when freshness or provenance is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/china-dev-environment)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with shell, XML, TOML, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent package-manager, Git, Docker, proxy, or CI configuration changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
