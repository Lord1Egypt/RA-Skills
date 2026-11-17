## Description:

Manages Codex CLI API key setup, background task execution, PID locking, task status, result summaries, and worker orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alukardo](https://clawhub.ai/user/alukardo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to launch and monitor Codex CLI tasks asynchronously while managing local API key setup, single-task locking, status checks, and result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local API key handling can expose credentials if the skill directory or generated files are mishandled.

Mitigation: Review before installing, avoid plaintext skill-local secrets for real use, and remove bundled task history before deployment.

Risk: Crafted task text or a modified credential file may become command execution because of shell parsing flaws.

Mitigation: Fix shell quoting and command construction before running the launcher on a real machine.

Risk: Background Codex execution can make changes outside the user's immediate attention.

Mitigation: Use the status and lock workflow, review completed task summaries, and inspect generated changes before accepting them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/alukardo/skills/codex-cli-guardian)
- [README.md](artifact/README.md)
- [CLI.md](artifact/CLI.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)
- [REFERENCES.md](artifact/REFERENCES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell command snippets, JSON task metadata, and text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local credential, lock, task status, task history, and summary files when installed and run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
