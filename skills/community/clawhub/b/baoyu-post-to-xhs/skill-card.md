## Description:

Posts image-text notes to Xiaohongshu (小红书) through Chrome CDP, with support for multiple images, title and description filling, topics, preview, and optional auto-submit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praguepp](https://clawhub.ai/user/praguepp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and publish image-text Xiaohongshu notes from local titles, content, Markdown, image files, and topic inputs through an authenticated Chrome profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls an authenticated Xiaohongshu browser profile and local posting assets.

Mitigation: Use a dedicated Chrome profile, close unrelated tabs, and run it only with assets intended for posting.

Risk: Auto-submit can publish immediately.

Mitigation: Keep the default preview flow unless immediate public posting is intended; use --submit only for content already approved.

Risk: Debug and probe scripts can inspect sensitive page state through Chrome CDP.

Mitigation: Avoid debug and probe commands on sensitive pages.

Risk: Runtime execution may use npx to fetch Bun when Bun is not already installed.

Mitigation: Prefer a preinstalled trusted Bun runtime and review dependencies before running scripts.

Risk: Chrome CDP process cleanup may stop browser sessions unexpectedly.

Mitigation: Review Chrome processes before allowing cleanup and preserve open work first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/praguepp/skills/baoyu-post-to-xhs)
- [Baoyu skill homepage](https://github.com/praguepp/baoyu-skills#baoyu-post-to-xhs)
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fill browser fields and leave Chrome open for user review unless auto-submit is requested.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
