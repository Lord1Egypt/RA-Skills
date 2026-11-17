## Description:

Run local agent-first SEO scoring, search-intent classification, and opportunity prioritization before content changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SEO practitioners use this skill to install, configure, and troubleshoot Agent SEO Engine for local SEO scoring, search-intent classification, opportunity ranking, privacy audit, and safety-boundary checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs mutable remote code from a GitHub repository that was not included in the reviewed artifact.

Mitigation: Review the repository before installing, prefer a pinned commit or signed release, and run setup commands only in trusted environments.

Risk: SEO content, Google Search Console exports, OAuth tokens, API keys, service-account JSON, local token files, or customer data could be exposed during troubleshooting.

Mitigation: Use doctor, connection-status, manifest, privacy-audit, or dry-run checks first, and avoid running commands in directories or environments containing sensitive data unless the package version is trusted.

## Reference(s):

- [Agent SEO Engine repository](https://github.com/davidmosiah/agent-seo-engine)
- [Agent SEO Engine ClawHub page](https://clawhub.ai/davidmosiah/skills/agent-seo-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup checks, privacy-audit guidance, troubleshooting steps, and explicit handling boundaries for private data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
