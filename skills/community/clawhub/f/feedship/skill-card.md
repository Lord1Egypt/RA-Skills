## Description:

Feedship helps agents manage RSS/Atom feeds, subscribe to websites, fetch articles, and search or read saved content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanpeipan](https://clawhub.ai/user/yanpeipan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Feedship to add and manage RSS, Atom, and GitHub release feeds, fetch new articles, and search or read stored articles from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable or unpinned remote Python installation and upgrade paths can change what code is installed over time.

Mitigation: Install from a trusted, pinned Feedship release whenever possible and avoid latest-commit upgrade paths unless the supply-chain tradeoff is understood.

Risk: Restricted-network mirror and trusted-host installation paths shift trust to the configured mirror.

Mitigation: Use only mirrors that are trusted for the deployment environment and avoid trusted-host options when standard package sources are available.

Risk: Scheduled fetching performs recurring network access and creates persistent local article and embedding storage.

Mitigation: Enable scheduled fetching only after confirming that periodic network access and local storage of fetched content are acceptable.

## Reference(s):

- [Feedship ClawHub Skill Page](https://clawhub.ai/yanpeipan/skills/feedship)
- [yanpeipan ClawHub Publisher Profile](https://clawhub.ai/user/yanpeipan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with command examples; Feedship commands may return Rich tables, panels, progress output, or JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv. OpenClaw metadata defines an optional default scheduled fetch every 30 minutes.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
