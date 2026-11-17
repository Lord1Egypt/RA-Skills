## Description:

Clipboard Memory helps agents recover text, commands, URLs, file paths, images, PDFs, and other items previously copied on a Mac from the local clipmem archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users on macOS use this skill when they need an agent to recover or inspect clipboard history from the local clipmem archive. It supports exact text recall, URL and file-path recovery, chronological timelines, targeted search, binary export, and setup diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive clipboard data stored in a persistent local archive.

Mitigation: Install only from a trusted publisher, prefer narrow read-only recall/search/timeline/get workflows, and avoid broad searches when clipboard history may include passwords, tokens, private documents, or other sensitive data.

Risk: The skill documents export, restore, delete, purge, setup, service, settings, launch-at-login, update-check, and install/uninstall commands that can change local state.

Mitigation: Require explicit user confirmation before state-changing commands and use candidate, detail, or dry-run commands where available before broad mutations.

Risk: Stale capture services or inaccessible archives can cause misleading empty or weak recall results.

Mitigation: Run the setup check, doctor, service status, or agent context workflow before concluding that requested clipboard content is unavailable.

## Reference(s):

- [Clipboard Memory Skill Page](https://clawhub.ai/tristanmanchester/skills/clipboard-memory)
- [Clipboard Memory Commands Reference](artifact/references/commands.md)
- [Clipboard Memory JSON Schema](artifact/references/json-schema.md)
- [Clipboard Memory Worked Examples](artifact/references/examples.md)
- [Clipboard Memory Setup Check](artifact/references/setup-check.md)
- [Clipboard Memory Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-oriented command examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes JSON or toon output parsing, pagination checks, setup checks, and explicit confirmation for state-changing clipmem commands.]

## Skill Version(s):

1.3.9 (source: server release metadata and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
