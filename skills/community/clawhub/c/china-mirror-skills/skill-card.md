## Description:

Configures and diagnoses mirror settings for common development tools in China's network environment, including Python, Node.js, Docker, APT, Conda, Rust, Go, Flutter, Homebrew, and GitHub workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loredunk](https://clawhub.ai/user/loredunk)

### License/Terms of Use:


## Use Case:

Developers and engineers working in China or constrained network environments use this skill to diagnose slow package downloads, compare mirror connectivity, and apply mirror configuration for installed development tools.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Persistent package source, Git routing, shell profile, and trust-setting changes can affect future development workflows.

Mitigation: Run diagnostics and dry-run modes first, avoid automatic confirmation, and review sudo or global Git changes before applying them.

Risk: Backups can include sensitive configuration files such as .npmrc.

Mitigation: Store backups carefully, avoid sharing backup directories, and remove unneeded backups from ~/.china-mirror-backup/.

Risk: Combining mirrors with proxies can cause conflicts or route downloads through unintended third-party services.

Mitigation: Review proxy environment variables and avoid --proxy-clone unless future HTTPS GitHub Git operations should use the selected proxy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loredunk/skills/china-mirror-skills)
- [Publisher profile](https://clawhub.ai/user/loredunk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run mode, backups, restore commands, and manual review before applying persistent configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
