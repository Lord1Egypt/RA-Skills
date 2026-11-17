## Description:

Installs ClawHub skills through fallback paths when the ClawHub CLI is rate-limited or fails, including GitHub search and clone, ClawHub zip download, and manual guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shensiglea-collab](https://clawhub.ai/user/shensiglea-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when a normal ClawHub CLI install is rate-limited or fails and they need fallback instructions or commands to install a ClawHub skill. It helps attempt GitHub clone, ClawHub zip download, and manual installation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may trust unverified search or download results.

Mitigation: Use only verified skill names and trusted sources, and prefer official or pinned installs where the repository owner, commit, and package integrity can be checked.

Risk: Skill names or paths may be handled unsafely by the installation flow.

Mitigation: Do not pass names or paths containing slashes or '..', and avoid running the installer with administrator privileges.

Risk: The skill downloads and installs other skills into the local skills directory.

Mitigation: Review the target skill and its security scan results before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shensiglea-collab/skills/fly-install)
- [Publisher Profile](https://clawhub.ai/user/shensiglea-collab)
- [ClawHub Skills Directory](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose downloads, Git clone operations, zip extraction, and writes to the configured skills directory.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
