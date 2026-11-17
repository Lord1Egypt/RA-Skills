## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to track blogs and RSS/Atom feeds, scan for updates, list articles, and manage read or removal actions through documented blogwatcher CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Go install command uses a mutable latest upstream module, so installed code can change over time.

Mitigation: Prefer a pinned and reviewed blogwatcher version when available, and review the upstream module before installation.

Risk: Blog subscription data and article metadata can be sensitive if command output is sent to network services.

Mitigation: Keep blogwatcher output local unless the user intentionally handles external sharing outside the skill's guardrails.

Risk: Adding untrusted or internal feed URLs can cause unintended internal network fetches.

Mitigation: Confirm untrusted feed URLs before adding them and refuse localhost, private-address, link-local, .local, and .internal destinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/blogwatcher-hardened)
- [blogwatcher upstream project](https://github.com/Hyaxia/blogwatcher)
- [Faberlens blogwatcher safety evaluation](https://faberlens.ai/explore/blogwatcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the blogwatcher CLI; Go installation uses github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
