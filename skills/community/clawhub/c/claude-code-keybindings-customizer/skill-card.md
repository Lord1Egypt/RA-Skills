## Description: <br>
Use when the user wants to customize Claude Code keybindings, rebind shortcuts, add chords, or edit `~/.claude/keybindings.json` safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to safely merge requested shortcut changes into an existing keybindings configuration while preserving unrelated bindings and schema fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keybinding changes can conflict with reserved, terminal-level, or existing shortcuts. <br>
Mitigation: Read the current keybindings file first, merge requested changes instead of replacing the full file, preserve unrelated bindings, and explain conflicts before saving. <br>
Risk: Editing local configuration with overly broad authority can affect repositories or settings outside the intended task. <br>
Mitigation: Review the skill's visible instructions before use and avoid giving it sensitive repositories, credentials, or broad mutation authority unless the task requires it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with JSON configuration snippets and conflict explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves unrelated existing bindings and flags reserved or terminal-level shortcut conflicts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
