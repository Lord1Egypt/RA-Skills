## Description:

Run ACT WebAssembly component tools via `act call` for sandboxed .wasm, OCI, or URL-based tools without system dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actcore](https://clawhub.ai/user/actcore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover ACT component tool schemas and run sandboxed WebAssembly tools through the `act` CLI with JSON inputs, metadata, and optional scoped filesystem access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote ACT components can be downloaded and cached before execution.

Mitigation: Use pinned, trusted OCI component references and avoid arbitrary HTTP component URLs.

Risk: Filesystem permissions can expose host paths to a component when granted too broadly.

Mitigation: Avoid `--allow-fs` for remote or untrusted components and grant only narrowly scoped `--allow-dir` access after checking the exact host path and purpose.

Risk: The skill depends on the local `act` CLI.

Mitigation: Install only when ACT component execution is intended and the ACT CLI source is trusted.

## Reference(s):

- [ACT Runtime on ClawHub](https://clawhub.ai/actcore/skills/act-cli)
- [actcore publisher profile](https://clawhub.ai/user/actcore)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [ACT command output is JSON on stdout; logs go to stderr when commands run.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
