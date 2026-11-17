## Description:

Low-friction food tracking - a pattern cache of the user's usual meals, a local-first journal, and Garmin Connect Nutrition as a sync target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weirdei](https://clawhub.ai/user/weirdei)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to help an agent log meals, maintain a local nutrition journal, reuse cached dish and product patterns, and optionally sync approved meal entries to Garmin Connect Nutrition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nutrition entries can be uploaded to Garmin's cloud when the user approves a Garmin sync.

Mitigation: Use --no-garmin for a strictly local journal and review the dry-run output before adding --yes.

Risk: Delete and correction commands can remove entries from the user's Garmin food log.

Mitigation: Review dry-run output and require an explicit --yes before deletes or corrections are applied.

Risk: The skill reads the user's existing Garmin OAuth session to access Garmin Connect.

Mitigation: Install only when that access is acceptable; the skill uses existing cached tokens and does not ask for or store a Garmin password.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weirdei/skills/garmin-nutrition)
- [Garmin Nutrition homepage](https://github.com/weirdei/garmin-nutrition)
- [uv documentation](https://docs.astral.sh/uv/)
- [garmin-pulse companion skill](https://github.com/weirdei/garmin-pulse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI writes local JSON and Markdown journal files; Garmin reads, writes, and deletes require explicit user commands and writes are dry-run unless --yes is used.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
