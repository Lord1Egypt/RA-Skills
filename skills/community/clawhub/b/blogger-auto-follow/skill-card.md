## Description:

Blogger Auto-Follow turns a user-supplied creator list into explicitly approved, single-platform visible-browser follow batches of up to 30 accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloyxs](https://clawhub.ai/user/helloyxs)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to prepare, preview, and run controlled creator-follow batches on one selected social platform after reviewing the fixed list and confirming each batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can follow accounts from a logged-in platform session after confirmation.

Mitigation: Review every batch preview before entering the count-bound confirmation phrase and use the dedicated browser profile intentionally.

Risk: Platform login state and followed-account history can remain in local browser profile, result, and archive files.

Mitigation: Delete data/browser_profiles and local result or archive files when retained login state or followed-account history is no longer desired.

Risk: The manager can bulk-open stored profile links in the local browser.

Mitigation: Use the bulk-open function only with trusted stored profile URLs.

## Reference(s):

- [Supported Platforms](references/supported_platforms.md)
- [Industry Categories Guide](references/industry_categories_guide.md)
- [ClawHub skill page](https://clawhub.ai/helloyxs/skills/blogger-auto-follow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces visible-browser execution guidance, dry-run previews, batch result records, and local followed-account archive updates.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
