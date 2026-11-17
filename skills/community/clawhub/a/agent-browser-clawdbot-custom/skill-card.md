## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baikaishuixyz](https://clawhub.ai/user/baikaishuixyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive headless browser workflows through the agent-browser CLI, including navigation, ref-based element interaction, snapshots, state persistence, network control, screenshots, and PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser state files, cookies, and local storage can contain sensitive session material.

Mitigation: Treat saved auth files, cookies, and local storage output like passwords or API keys, and avoid committing or sharing them.

Risk: Global npm installation and browser dependency installation can expand the impact of a compromised or unexpected package.

Mitigation: Install only from the expected agent-browser package and repository, avoid running install steps as root, and prefer a pinned or project-local install.

## Reference(s):

- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or consume browser state files, screenshots, PDFs, cookies, local storage, and accessibility-tree snapshots.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
