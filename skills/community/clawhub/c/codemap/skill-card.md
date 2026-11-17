## Description:

Build a compact local SQLite index of every function, class, method, interface and type across your repos, so an agent finds a symbol's file:line and signature in one lookup instead of a tree-wide grep plus whole-file read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use codemap to build a local symbol index for selected repositories, then query function, class, method, interface, and type definitions by name instead of repeatedly scanning and reading source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source files from repository roots passed to codemap and stores symbol names, signatures, absolute paths, and line numbers in a local SQLite database.

Mitigation: Build indexes only for repositories the user intends the agent to inspect, and avoid unrelated private directories when that metadata should not be indexed.

Risk: Extraction is regex-based and can miss uncommon declarations, re-exports, dynamically assigned names, or call/reference relationships.

Mitigation: Treat codemap results as fast definition lookup hints and fall back to source inspection or broader search when a symbol is missing or ambiguous.

Risk: The local index is a snapshot and can become stale after substantial code edits.

Mitigation: Rebuild the index after large edits or before relying on lookup results in an active development session.

## Reference(s):

- [codemap ClawHub skill page](https://clawhub.ai/workloftai/skills/codemap)
- [Workloft Labs](https://workloft.ai/labs)
- [Workloft support](https://workloft.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local CLI instructions and compact file:line symbol lookup records; JSON output is available for find and file commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md and clawhub.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
