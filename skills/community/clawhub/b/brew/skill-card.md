## Description:

Manage Homebrew end-to-end on macOS, including detecting whether Homebrew is installed, understanding formula vs cask, updating metadata and packages, installing/uninstalling software, searching/listing package state, cleanup/autoremove, diagnostics, and Brewfile workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weichengwu](https://clawhub.ai/user/weichengwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to manage Homebrew package lifecycle tasks, diagnose brew environment issues, and export or sync package state with Brewfile workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to run the live Homebrew remote installer script in Bash without integrity verification.

Mitigation: Review the official installer source or run the official Homebrew install flow yourself before allowing installation.

Risk: The skill manages Homebrew packages and Brewfile workflows that can install, uninstall, clean up, or sync software on a Mac.

Mitigation: Confirm package names and Brewfile paths before install, uninstall, cleanup, autoremove, or bundle commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weichengwu/skills/brew)
- [Publisher Profile](https://clawhub.ai/user/weichengwu)
- [Homebrew Installer Script](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise command reports, verification steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
