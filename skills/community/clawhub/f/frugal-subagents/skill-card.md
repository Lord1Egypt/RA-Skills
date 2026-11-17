## Description:

Frugal Subagents is a Claude Code plugin that keeps delegated helpers on cheaper model tiers by default, blocks nested subagent spawns, caps per-session spawns, and provides bundled web-research and extraction workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikotelkin](https://clawhub.ai/user/ikotelkin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to control Claude Code subagent cost and fan-out while delegating web research, page scanning, listing comparison, extraction, and other volume-heavy helper work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin runs a local Node.js PreToolUse hook that can change missing subagent models or deny nested and over-budget subagent spawns.

Mitigation: Review the configured defaults before installation, run the documented hook verification, and tune the FRUGAL_SUBAGENTS_* environment settings when a different policy is required.

Risk: If Node.js is missing or the hook cannot run, subagent limits are not enforced even though the guidance remains available.

Mitigation: Install Node.js LTS with user consent and start a new Claude Code session; until then, follow the cheap-tier, no-nesting, file-first delegation rules manually.

Risk: Bundled workers can write research and extraction results to local files, which may include sensitive or personal data if delegated.

Mitigation: Specify explicit output paths and avoid delegating secrets or sensitive personal data unless local storage of those results is acceptable.

Risk: The guard stores small per-session state files in the operating system temporary directory to count spawns.

Mitigation: Treat the state as local operational data and clear the temporary frugal-subagents state directory if session accounting should be reset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ikotelkin/skills/frugal-subagents)
- [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, short worker digests, file outputs, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled workers write research or extraction results to files and return short digests; the local guard hook may update or deny Agent calls according to configured limits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
