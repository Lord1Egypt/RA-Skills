## Description:

Install, update, run, and verify the public ClawStatus dashboard from GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverchenx](https://clawhub.ai/user/neverchenx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or refresh a local or LAN-accessible ClawStatus dashboard, start or restart it, and verify that it responds on port 8900.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install workflow retrieves mutable remote Python code before installation.

Mitigation: Review the source before installing and use a trusted, pinned ClawStatus revision when possible.

Risk: The installer uses pip with --break-system-packages, which can affect the user's Python environment.

Mitigation: Prefer installation inside a virtual environment or another isolated Python environment.

Risk: The REPO_URL override can redirect installation to an untrusted repository.

Mitigation: Avoid REPO_URL overrides unless the repository source is explicitly trusted.

Risk: The documented run command binds the dashboard to 0.0.0.0 for LAN access.

Mitigation: Bind to 127.0.0.1 by default, or use firewall and authentication controls when LAN exposure is intentional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neverchenx/skills/clawstatus-dashboard)
- [ClawStatus Commands](references/commands.md)
- [ClawStatus GitHub Repository](https://github.com/NeverChenX/ClawStatus.git)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, run, restart, and HTTP verification commands for a dashboard service.]

## Skill Version(s):

2.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
