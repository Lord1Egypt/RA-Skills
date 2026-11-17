## Description:

Re-apply custom patches to claw-lark plugin dist files after updates. Use when claw-lark plugin is updated/reinstalled and custom behaviors (requireMention filtering, reply_in_thread, thread-based replies) stop working. Also use when debugging Lark message routing issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengxiao-wang](https://clawhub.ai/user/pengxiao-wang)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to re-apply custom claw-lark plugin patches after plugin updates or reinstalls. It also helps debug Lark message routing, mention filtering, and thread-reply behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-apply script makes persistent changes to installed claw-lark dist files.

Mitigation: Review the patch script before use and keep a backup or versioned copy of the original dist files so the plugin can be restored.

Risk: BOT_OPEN_ID and BOT_NAME values are embedded into JavaScript source during patching.

Mitigation: Run the script only from a clean environment and set BOT_OPEN_ID and BOT_NAME to simple expected values before applying patches.

## Reference(s):

- [Patch Details](references/patch-details.md)
- [ClawHub skill page](https://clawhub.ai/pengxiao-wang/skills/claw-lark-patches)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash and JavaScript patch snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional shell script that modifies local claw-lark dist files when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
