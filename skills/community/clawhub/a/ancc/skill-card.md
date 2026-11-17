## Description:

Grow limbs - discover, validate, and integrate ANCC-compliant CLI tools into your OpenClaw agent for tool setup, environment security audits, token budget checks, and agent-native CLI scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and run the ANCC CLI for validating agent-native tools, auditing agent environments, measuring skill context cost, comparing configurations, and scaffolding new compliant tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions use latest release or mutable package sources for an external CLI.

Mitigation: Pin a reviewed ANCC version and verify checksums or signatures before installation.

Risk: Audit commands can inspect credential, history, and sensitive configuration locations.

Mitigation: Run audit commands deliberately as a normal user, avoid sudo and shared or secret-bearing CI contexts, and treat audit output as sensitive.

## Reference(s):

- [ANCC documentation](https://ancc.dev)
- [ANCC repository](https://github.com/ppiankov/ancc)
- [ClawHub ANCC skill page](https://clawhub.ai/ppiankov/skills/ancc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML snippets, and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ancc CLI binary; audit output may reference sensitive local configuration paths.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
