## Description: <br>
Clawd Modifier helps users customize the Claude Code mascot by changing colors, adding arms or accessories, applying ASCII art variants, inspecting the current mascot state, and restoring the original appearance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masonc15](https://clawhub.ai/user/masonc15) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to personalize Clawd in their local Claude Code CLI through guided color, ASCII art, extraction, and restore workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite installed Claude Code CLI files, including byte-level modification of an executable script or binary. <br>
Mitigation: Run dry-run and list modes first, use explicit --cli-path or --binary targets, keep backups, and restore the original appearance when needed. <br>
Risk: Claude Code updates or integrity checks may overwrite, undo, or conflict with local mascot patches. <br>
Mitigation: Expect updates to require reapplication or restoration, and test the CLI after changes with the documented version check. <br>
Risk: Pattern-based replacements may fail or target unexpected matches when the installed Claude Code version differs from the documented patterns. <br>
Mitigation: Inspect replacement counts and patch details, target a known local file, and stop when patterns are missing or the script reports no matches. <br>


## Reference(s): <br>
- [Clawd Anatomy](references/clawd-anatomy.md) <br>
- [Unicode Block Drawing Characters](references/unicode-blocks.md) <br>
- [Clawd Variant Gallery](assets/clawd-variants.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/masonc15/clawd-modifier) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, file paths, and short procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct dry-run, backup, restore, and explicit target-path workflows before modifying local Claude Code files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
