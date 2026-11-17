## Description:

Provides agents with fast indexed local file and path search on Windows using voidtools Everything for path lookup, recent-file discovery, match counts, and structured search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamq96](https://clawhub.ai/user/williamq96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill on Windows to bootstrap and prefer an ev CLI for indexed local file lookup, recent-file discovery, counts, and direct es.exe passthrough when recursive scans are too slow or unsuitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the user PATH and leave persistent ev/everything-cli command shims and cached runtime files on disk.

Mitigation: Review the shim directory and cache location before installation, require explicit install consent, and document how to remove the shims and PATH entry.

Risk: The skill downloads and runs es.exe without a pinned hash or signature check.

Mitigation: Prefer a release that verifies the downloaded binary with a pinned hash or signature before execution, or preinstall a trusted es.exe in the expected vendor path.

Risk: The skill can trigger broadly for local file searches and can start Everything automatically.

Mitigation: Use it only in Windows environments where indexed local search is appropriate, scope queries with path or time filters when possible, and review broad searches before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamq96/skills/everything-cli)
- [PowerShell runtime wrapper](artifact/references/everything-cli.ps1.txt)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command execution returns JSON, text, paths, or counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search payloads can include query, count, offset, limit, scope, sort, descending, path, and results; raw passes arguments through to es.exe.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
