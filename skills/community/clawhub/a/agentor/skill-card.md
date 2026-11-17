## Description:

Use agenTOR for Tor-routed browser sessions with receipts, HTML capture, screenshots, and compact research runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tor-routed or proxy-routed browser sessions, capture page evidence, and produce compact local research artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external agentor CLI that is not bundled or verified by the skill package.

Mitigation: Install or run the CLI only from a trusted source and verify the executable before use.

Risk: Tor or proxy routing improves path hygiene but does not guarantee identity separation.

Mitigation: Avoid authenticated browser state and sensitive accounts when separation matters.

Risk: Browser receipts, HTML captures, screenshots, and reports can contain sensitive page content.

Mitigation: Review the output directory before sharing artifacts and set an explicit output path when retention or access controls matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/builtbyecho/skills/agentor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce local receipt folders containing HTML, screenshots, summary text, receipt JSON, and report markdown.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
