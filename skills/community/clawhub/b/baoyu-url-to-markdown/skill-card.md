## Description:

Fetch any URL and convert to markdown using baoyu-fetch CLI with Chrome CDP and site-specific adapters for X/Twitter, YouTube transcripts, Hacker News threads, and generic pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web pages, convert them into Markdown or JSON, and optionally save page media beside the generated document. It is intended for webpage capture workflows that may require site-specific handling or interactive login/CAPTCHA resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser sessions may expose private page content or account state during capture.

Mitigation: Use the skill only on URLs approved for browser automation, and avoid private, internal, invitation-only, password-reset, or token-bearing URLs unless the workflow has been reviewed.

Risk: Generic Markdown extraction can send target URLs to defuddle.md as a remote fallback.

Mitigation: Review remote fallback behavior before use on confidential pages, and disable or modify the fallback path when sensitive URLs must remain local.

Risk: X/Twitter session cookies can be persisted in a plaintext sidecar file.

Mitigation: Treat the Chrome profile directory and x-session-cookies.json as sensitive, restrict access to them, and delete saved session files when they are no longer needed.

Risk: Debug output can save page HTML, generated Markdown, document metadata, and network contents.

Mitigation: Avoid --debug-dir on confidential pages, or store debug artifacts only in approved protected locations and remove them after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-url-to-markdown)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown)
- [Adapters & Media](references/adapters.md)
- [Quality Gate & Recovery](references/quality-gate.md)
- [First-Time Setup](references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown or JSON output, optionally written to files with downloaded media assets in adjacent directories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun and a Chrome or Chromium browser; output quality should be checked after headless captures.]

## Skill Version(s):

1.117.2 (source: ClawHub release metadata, changelog dated 2026-05-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
