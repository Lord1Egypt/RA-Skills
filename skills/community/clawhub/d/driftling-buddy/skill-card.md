## Description:

Driftling Buddy adds a bilingual, non-human companion system that reacts to a user's work, renders compact buddy cards, grows stats, and maintains a personalized collection over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taojinkai](https://clawhub.ai/user/taojinkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add a lightweight, persistent companion experience to normal agent sessions while keeping the underlying task work primary. It supports progress/status cards, collectible buddy unlocks, bilingual flavor text, and local collection state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep a local, behavior-derived companion history that may include sensitive task details.

Mitigation: Use explicit slash commands, avoid sensitive details in buddy names or context fields, set BUDDY_STATE_FILE to an isolated path when needed, and inspect or remove ~/.buddy_mode_state.json to clear saved data.

Risk: The security summary flags unsafe state and terminal handling that users should review before installation.

Mitigation: Review the skill before installing, run the included local checks, and treat generated companion text as status output rather than executable commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taojinkai/skills/driftling-buddy)
- [Publisher profile](https://clawhub.ai/user/taojinkai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with terminal-style companion cards and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local companion state in a default or user-selected state file.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
