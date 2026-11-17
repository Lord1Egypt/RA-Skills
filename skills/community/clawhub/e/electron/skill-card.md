## Description:

Build Electron desktop apps with secure architecture and common pitfall avoidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Electron desktop applications while avoiding common security, packaging, native module, platform, debugging, memory, and performance pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance may affect security-sensitive Electron settings such as IPC exposure, renderer isolation, and production logging.

Mitigation: Review suggested settings in the target app context, explicitly whitelist IPC channels, validate IPC message content, and scan the skill before deployment.

Risk: Packaging guidance may be misapplied to production signing, update, installer, or platform-specific release requirements.

Mitigation: Validate packaging, code signing, updater, and platform choices against the app's release requirements before shipping.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with inline code identifiers and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable artifact; npm availability is listed as a runtime prerequisite for Electron workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
