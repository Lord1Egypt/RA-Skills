## Description:

Real-time companion monitor for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luccast](https://clawhub.ai/user/luccast)

### License/Terms of Use:


## Use Case:

Developers and operators use Crabwalk to install and run a companion monitor for OpenClaw agents, including monitor and workspace views for real-time inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party binary can read OpenClaw configuration and related credentials.

Mitigation: Install only when the publisher is trusted, review the downloaded release before use, and avoid running it with credentials beyond what the monitor needs.

Risk: The monitor and workspace views may be exposed over the network.

Mitigation: Prefer binding to localhost; share a LAN URL only on trusted networks and only with intended viewers.

Risk: The install and update flow can persist software locally and may attempt optional dependency installation with sudo.

Mitigation: Confirm updates before running them, and allow sudo or optional dependency installation only when that system change is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luccast/skills/crabwalk)
- [Crabwalk Homepage](https://crabwalk.app)
- [Crabwalk Repository](https://github.com/luccast/crabwalk)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash command blocks and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, verification, start, update, and feedback-handling guidance for the Crabwalk CLI.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter reports 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
