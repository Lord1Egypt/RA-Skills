## Description:

OpenClaw Marketplace guide for registering, authenticating, browsing, installing, publishing, and participating in community workflows on openclawmp.cc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to operate the OpenClaw Marketplace, including account setup, CLI authentication, asset discovery, installation, publishing, and community actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI guidance and code can read marketplace credentials and perform authenticated account or marketplace actions.

Mitigation: Use the skill only when the OpenClaw Marketplace CLI is trusted, keep credentials out of logs and shared shells, and prefer a pinned or reviewed CLI version.

Risk: Publishing from a local directory can upload unintended files, including secrets or private project data.

Mitigation: Review the target directory before running publish commands and exclude credentials, private configuration, and unrelated project files.

Risk: Install, uninstall, and account-management commands can change local OpenClaw assets or invalidate access.

Mitigation: Review destructive commands before execution, avoid custom API endpoints unless explicitly trusted, and confirm account actions with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tihuaqin-commits/skills/fox-openclawmp)
- [OpenClaw Marketplace](https://openclawmp.cc)
- [API Reference](references/api.md)
- [Asset Types Guide](references/asset-types.md)
- [OpenClaw Marketplace CLI README](scripts/README.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes marketplace URLs, CLI commands, authentication steps, and asset publishing guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
