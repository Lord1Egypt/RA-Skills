## Description:

Generate and play bingo cards with number calling and verification. Use when running bingo games.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate bingo cards, call numbers, reset a local game, inspect call history, check supplied numbers, and view simple call counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete gameplay behavior may make verification or call history inaccurate.

Mitigation: Use it only as a lightweight local helper and manually confirm bingo results or call history before relying on them.

Risk: The new-game command clears the skill's stored calls file.

Mitigation: Run new-game only when intentionally resetting state, and preserve the calls file separately if prior calls must be retained.

Risk: The skill writes local state under ~/.local/share/bingo/.

Mitigation: Install and run it only in environments where this local file write behavior is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/bingo)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local bingo state under ~/.local/share/bingo/.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
