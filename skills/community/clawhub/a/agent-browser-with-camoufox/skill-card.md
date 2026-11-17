## Description:

One-click deployment of camoufox anti-detection browser with modified agent-browser. Patches agent-browser to auto-detect camoufox/firefox from executable path instead of defaulting to chromium. Includes SkillsI integration for seamless browser automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adastraabyssoque](https://clawhub.ai/user/adastraabyssoque)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to install Camoufox and configure agent-browser so browser automation can launch a Firefox/Camoufox executable instead of defaulting to Chromium.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can permanently alter a development environment by installing global packages and replacing agent-browser.

Mitigation: Run it only in a disposable VM or container, or rewrite it to use project-local installs and require confirmation before replacing existing tools.

Risk: The installer uses remote installers and mutable dependencies.

Mitigation: Pin versions and checksums, avoid curl-to-shell installation paths, and review downloaded scripts before execution.

Risk: The installer backs up and replaces existing agent-browser files without a validated rollback workflow.

Mitigation: Show diffs before modification and provide a tested rollback path that restores the exact prior package state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adastraabyssoque/skills/agent-browser-with-camoufox)
- [Camoufox GitHub repository](https://github.com/daijro/camoufox)
- [agent-browser GitHub repository](https://github.com/browser-use/agent-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, verification, troubleshooting, and executable-path configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
