## Description:

Drive a native GUI app (macOS, Windows, Linux) via the cua-driver CLI (default) or MCP server; snapshot its accessibility tree, click/type/scroll by element_index or pixel coordinates, and verify via re-snapshot without bringing the target to the foreground.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cua](https://clawhub.ai/user/cua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate native GUI applications across macOS, Windows, and Linux through Cua Driver while preserving snapshot-action-verify checks and explicit escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables powerful control of real desktop applications.

Mitigation: Install only when an agent is expected to operate host GUI apps, require explicit intent for destructive steps, and keep snapshot-action-verify checks in the workflow.

Risk: Installer commands fetch and execute remote installation scripts.

Mitigation: Review or replace the remote installer flow with a verified package before deployment.

Risk: Recording can capture screenshots, action metadata, and video that may include sensitive information.

Mitigation: Do not enable recording around secrets, and opt out of video capture when visual evidence is unnecessary.

Risk: Browser automation can interact with authenticated browser profiles.

Mitigation: Prefer isolated browser profiles and require explicit approval before attaching to existing authenticated profiles.

Risk: Autostart and unrestricted embedded mode can broaden local exposure.

Mitigation: Disable autostart or unrestricted embedded mode unless there is a specific need and the exposure has been reviewed.

## Reference(s):

- [Cua Driver documentation](https://cua.ai/docs/cua-driver)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline CLI and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific operating constraints and verification steps.]

## Skill Version(s):

0.11.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
