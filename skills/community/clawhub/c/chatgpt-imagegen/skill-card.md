## Description:

Generate raster images (PNG/JPEG/WebP) using the user's ChatGPT subscription via a local Python CLI, with browser-backed and Codex-backed generation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create bitmap assets such as photos, illustrations, icons, hero banners, mockups, sprites, and concept art for the current workspace. It is also intended to help illustrate long-form project documents when generated images are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can download and run unpinned remote code.

Mitigation: Review the skill before installing, replace silent download steps with pinned and inspected artifacts, and require user approval before fetching or running code.

Risk: The skill can use the user's logged-in ChatGPT browser session or Codex account, create local files and ChatGPT activity, and consume subscription quota.

Mitigation: Install only from trusted publishers, keep backend choice explicit, and require approval before proactive or bulk image generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/chatgpt-imagegen)
- [Server-resolved GitHub source](https://github.com/leeguooooo/chatgpt-imagegen)
- [chrome-use prerequisite repository](https://github.com/leeguooooo/chrome-use)
- [Chrome extension prerequisite](https://chromewebstore.google.com/detail/agent-browser-stealth/knfcmbamhjmaonkfnjhldjedeobeafmk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and file-path outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to save generated PNG, JPEG, or WebP image files into the workspace.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 0.16.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
