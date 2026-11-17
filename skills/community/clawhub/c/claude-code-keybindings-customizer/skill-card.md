## Description:

Helps customize Claude Code keybindings, rebind shortcuts, add chords, and safely edit ~/.claude/keybindings.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to merge requested keybinding changes into existing configuration while preserving schema fields and surfacing reserved or terminal-level shortcut conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keybinding changes persist across future Claude Code sessions and may alter expected shortcut behavior.

Mitigation: Review the proposed merged keybinding diff before saving and preserve unrelated existing bindings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/claude-code-keybindings-customizer)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON keybinding configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conflict explanations and a proposed merged keybindings diff for review before saving.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
