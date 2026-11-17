## Description:

Modifies the Claude Code Clawd mascot by changing colors, adding arms or accessories, extracting current art, and restoring cosmetic variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masonc15](https://clawhub.ai/user/masonc15)

### License/Terms of Use:


## Use Case:

Developers who use Claude Code can use this skill to personalize the terminal mascot with color and ASCII-art variants while following backup, dry-run, restore, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits installed Claude Code program files and can break or alter the CLI beyond a cosmetic mascot change.

Mitigation: Use dry-run first, keep backups enabled, prefer a user-local Claude Code install, and be prepared to restore or reinstall Claude Code if a patch corrupts the CLI.

Risk: Pattern-based art and binary patches may fail or apply incorrectly when the installed Claude Code version differs from the expected layout.

Mitigation: Verify the target path before patching, test Claude Code after changes, and use the restore option or reinstall Claude Code if the mascot patch does not behave as expected.

## Reference(s):

- [Clawd Anatomy](references/clawd-anatomy.md)
- [Unicode Block Drawing Characters](references/unicode-blocks.md)
- [Clawd Variant Gallery](assets/clawd-variants.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, script arguments, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file patch instructions, dry-run usage, backup paths, restore steps, and terminal compatibility notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
