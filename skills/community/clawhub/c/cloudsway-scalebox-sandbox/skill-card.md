## Description:

Create and manage isolated ScaleBox cloud sandboxes for secure code execution, browser automation, and temporary development workflows using CLI commands, REST API calls, or the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloriathepenguin](https://clawhub.ai/user/gloriathepenguin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to create remote ScaleBox sandboxes, run commands, transfer files, expose sandbox ports, and clean up temporary environments. It is useful when work should run away from the local machine, including untrusted code tests and browser automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an agent to use a ScaleBox API key.

Mitigation: Use a limited, revocable API key and avoid sharing credentials outside the intended environment.

Risk: Sandbox file uploads may send local files to a cloud execution environment.

Mitigation: Upload only files intentionally selected for sandbox processing and avoid unnecessary sensitive data.

Risk: The workflow depends on ScaleBox CLI and SDK tooling installed from external sources.

Mitigation: Install the CLI from official ScaleBox documentation, verify checksums when available, and prefer a pinned SDK version.

## Reference(s):

- [ScaleBox Official Website](https://www.scalebox.dev)
- [ScaleBox Documentation](https://www.scalebox.dev/docs)
- [ScaleBox CLI Installation](https://www.scalebox.dev/docs/en/cli/installation)
- [ScaleBox API Reference](https://www.scalebox.dev/docs/en/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, curl, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ScaleBox API key and network access to ScaleBox services.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
