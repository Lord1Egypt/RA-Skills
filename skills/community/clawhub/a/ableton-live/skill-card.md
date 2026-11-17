## Description:

Connect and operate the Loophole Bridge, an Ableton Live MCP server, to check bridge prerequisites, emit MCP client setup guidance, and run guided Live editing recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music producers use this skill to check Loophole Bridge readiness, generate merge-safe MCP client configuration, and run Ableton Live editing recipes through registered bridge tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge bearer token in bridge.json is sensitive.

Mitigation: Treat the token as a secret and review generated MCP client configuration before merging it into a local client config.

Risk: Recipe write actions can change the open Ableton Live set one bridge tool call at a time.

Mitigation: Preview mappings or plans before writes, state the mutation count before execution, and ask the user to inspect Live undo history after changes.

Risk: The skill inherits bridge beta limits such as MIDI-only note edits and no direct Arrangement timeline writes.

Mitigation: Keep operations within the documented bridge capabilities and use read-only planning when a requested edit is outside those limits.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/OthmanAdi/loophole/tree/main/skills/ableton-live)
- [ClawHub skill page](https://clawhub.ai/othmanadi/skills/ableton-live)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/FIX diagnostics, merge-safe client config snippets, read-only Live summaries, and user-approved Live mutation plans.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
