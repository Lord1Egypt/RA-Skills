## Description:

Switch Codex between buying from the asale market and using its own subscription, and see which running sessions are still on the old config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to switch Codex between asale market buying and a personal subscription, then identify running Codex sessions that have not picked up the new configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer is fetched from a remote URL and piped directly to the shell.

Mitigation: Prefer a signed, versioned installer with published checksums and review the installer before use.

Risk: The skill can route future Codex requests through asale by changing Codex provider and auth configuration.

Mitigation: Review the exact Codex config and auth changes, confirm rollback behavior, and enable the switch only after accepting that routing change.

Risk: Existing Codex sessions may continue using their startup configuration after the switch changes files on disk.

Mitigation: Check running Codex sessions and restart the sessions the user chooses so they pick up the new configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-codex)
- [Publisher profile](https://clawhub.ai/user/dlazyai)
- [asale homepage](https://asale.ai)
- [asale source metadata link](https://github.com/asale-ai/asale)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Codex and asale configuration paths and running process summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
