## Description:

Answers questions about a developer's machine using AGASTHY data on repositories and uncommitted work, installed software, processes and ports, coding-agent sessions, token usage, and package removal impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers use the skill to answer questions about their own machine, projects, installed tools, running processes, coding-agent activity, token costs, and the impact of removing a package. It bases answers on AGASTHY data and can suggest commands when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested one-line installer downloads and immediately runs a script from a changeable GitHub branch.

Mitigation: Avoid the download-and-run command; inspect the installer and use a pinned release with verifiable provenance.

Risk: The security assessment is incomplete because some referenced paths were not present in the bundled artifact.

Mitigation: Review the complete release contents before deciding to install.

## Reference(s):

- [AGASTHY project](https://github.com/HMAKT99/Agasthy)
- [AGASTHY releases](https://github.com/HMAKT99/Agasthy/releases/latest)
- [Installer script (review before use)](https://raw.githubusercontent.com/HMAKT99/Agasthy/main/install.sh)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Concise natural-language answers based on AGASTHY JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested commands when requested; reports unavailable data as unknown.]

## Skill Version(s):

0.1.10 (source: artifact/SKILL.md frontmatter; release evidence agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
