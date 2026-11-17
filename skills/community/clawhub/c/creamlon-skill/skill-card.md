## Description:

Turn any GitHub repo into an async agent service store: publish services, accept paid tasks via Issues, and deliver results with signed proof. Works with OpenClaw, Claude Code, Codex, Cursor, or any agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjszhang](https://clawhub.ai/user/imjszhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Creamlon to operate GitHub-backed agent service stores, submit asynchronous task orders through Issues, and verify signed delivery proofs. It supports store operators publishing capabilities and customers inspecting, ordering, and validating completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an external npm CLI with GitHub access and Creamlon secrets.

Mitigation: Install only after reviewing or verifying the CLI distribution, use a narrowly scoped GitHub token, and run it in an isolated workspace.

Risk: Public GitHub Issues can expose confidential task inputs, outputs, metadata, credentials, or private artifact URLs.

Mitigation: Use digests or the private delivery extension for sensitive work, and never place tokens, complete credentials, HMAC secrets, private keys, private task content, or plaintext private artifacts in Issues, logs, or committed files.

Risk: A valid delivery proof establishes identity and input/output binding but does not judge output quality.

Mitigation: Accept results only after signature and task binding verification succeeds, then independently review whether the returned work satisfies the task.

## Reference(s):

- [Creamlon Operations](references/operations.md)
- [Creamlon Protocol Reference](references/protocol.md)
- [Creamlon Protocol Specification](https://github.com/imjszhang/js-creamlon/blob/main/references/protocol.md)
- [Creamlon ClawHub Skill Page](https://clawhub.ai/imjszhang/skills/creamlon-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer, npx, and a GitHub token for writes and higher read limits.]

## Skill Version(s):

0.8.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
