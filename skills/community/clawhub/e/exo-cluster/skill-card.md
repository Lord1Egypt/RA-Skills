## Description:

Exo distributed AI cluster guidance for combining multiple Mac, PC, and WSL2 devices into a unified local GPU cluster for running large language models such as DeepSeek, Qwen, and LLaMA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and manage an Exo-based local AI inference cluster across Mac, PC, WSL2, Windows, and Linux systems. It provides installation, cluster startup, model deployment, API usage, dashboard, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run third-party installers and high-impact installation commands.

Mitigation: Review commands before execution, prefer pinned releases or reviewed commits, and run setup in a dedicated virtual environment or under an unprivileged account.

Risk: The skill starts dashboard and API services that may be reachable on a local network.

Mitigation: Restrict dashboard and API access to trusted hosts, use network isolation where possible, and avoid exposing service ports beyond the intended LAN.

Risk: Prompts and model traffic may contain sensitive information when sent to local API endpoints.

Mitigation: Avoid sending sensitive prompts unless authentication, network isolation, and transport protections are in place.

## Reference(s):

- [Exo official website](https://exolabs.net/)
- [Exo GitHub repository](https://github.com/exo-explore/exo)
- [Exo Windows community repository](https://github.com/tensorsofthewall/exo_windows)
- [ClawHub skill page](https://clawhub.ai/smseow001/skills/exo-cluster)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local cluster setup, model deployment, API usage, dashboard, and troubleshooting instructions.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
