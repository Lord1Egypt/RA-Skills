## Description:

Download 4K mobile wallpapers specifically from pic.netbian.com, including WeChat QR login, token-based original image download, rate-limit spacing, 4K validation, and cleanup of non-4K files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guitu917](https://clawhub.ai/user/guitu917)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly want to batch download and verify 4K mobile wallpapers from pic.netbian.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a logged-in pic.netbian.com session cookie, which can expose account access if pasted into shell history, logs, or shared transcripts.

Mitigation: Provide the cookie only in a private execution context, avoid placing real session cookies directly in shared commands or logs, and refresh the cookie after completing any manual verification.

Risk: The verification script can permanently remove non-matching JPG files when run with --delete.

Mitigation: Run verification without --delete first, inspect the target directory, and use --delete only on a directory dedicated to this download workflow.

Risk: Automated retries around slider or captcha checks may create account or site-access issues.

Mitigation: Pause for manual completion by default, use only cautious assisted attempts when explicitly approved, and continue only after reading a fresh browser cookie.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guitu917/skills/bian16-wallpaper-downloader)
- [Download Notes](references/download-notes.md)
- [pic.netbian.com](https://pic.netbian.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands; downloaded JPG files are produced by the bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in pic.netbian.com session cookie and uses configurable count, interval, output directory, category, minimum width, and scan-page parameters.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
