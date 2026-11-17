## Description:

Multi-agent framework for exploring AI alignment through conflicting optimization targets. Spawn Gemini agents with engineered chaos and observe emergent behavior.

This skill is for research and development only.

## Publisher:

[jbbottoms](https://clawhub.ai/user/jbbottoms)

### License/Terms of Use:


## Use Case:

Developers, prompt engineers, educators, and AI safety researchers use this skill to run Gemini-based multi-agent experiments that show how conflicting optimization targets can produce incompatible recommendations and emergent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The experiment scripts can send the contents of /tmp/chaos-sandbox to Google Gemini without filtering, preview, or explicit runtime confirmation.

Mitigation: Use synthetic data only, keep secrets and private configuration out of the sandbox, and add an allowlist, redaction, file-size limits, and a confirmation preview before API calls.

Risk: The skill depends on a Gemini API key and the requests package.

Mitigation: Store the Gemini key carefully and run experiments in an isolated virtual environment with pinned dependencies.

Risk: The advanced tool-access path could turn model recommendations into file operations.

Mitigation: Keep tool access disabled unless intentionally testing execution; if enabled, restrict paths to /tmp/chaos-sandbox, require confirmation, log actions, keep rollback snapshots, and use a kill switch.

## Reference(s):

- [Chaos Lab ClawHub Skill Page](https://clawhub.ai/jbbottoms/skills/chaos-lab)
- [Tool Access](artifact/docs/tool-access.md)
- [Flash Results](artifact/examples/flash-results.md)
- [Pro Results](artifact/examples/pro-results.md)
- [Trio Results](artifact/examples/trio-results.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown experiment logs, terminal summaries, and setup or run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Gemini API key and reads files from /tmp/chaos-sandbox when running the bundled experiment scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
