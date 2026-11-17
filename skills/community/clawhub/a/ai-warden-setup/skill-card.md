## Description:

Install, configure, and manage the AI-Warden prompt injection protection plugin for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-warden](https://clawhub.ai/user/ai-warden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install, configure, update, and troubleshoot the AI-Warden prompt injection protection plugin on OpenClaw instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate broad prompt-injection scanning for agent content and tool data.

Mitigation: Review the configuration before enabling the plugin, and keep the documented OpenClaw config backup available for rollback.

Risk: API mode may process scanned agent content externally without endpoint, redaction, retention, or logging details in the provided evidence.

Mitigation: Prefer offline mode unless external processing is acceptable, and require clear publisher documentation before setting AI_WARDEN_API_KEY.

Risk: The install flow fetches an npm package and writes OpenClaw extension and configuration files.

Mitigation: Install from a trusted environment, inspect the package before activation, verify package metadata and shasum, and restore the backup if startup or config checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-warden/skills/ai-warden-setup)
- [AI-Warden publisher site](https://ai-warden.io)
- [openclaw-ai-warden npm package](https://www.npmjs.com/package/openclaw-ai-warden)
- [Repository URL cited by artifact](https://github.com/ai-warden/openclaw-plugin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, update, verification, troubleshooting, and rollback steps for OpenClaw configuration.]

## Skill Version(s):

1.4.1 (source: ClawHub release evidence; artifact frontmatter lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
