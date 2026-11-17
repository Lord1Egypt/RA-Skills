## Description:

Posts content to Weibo, including regular text, image, and video posts and headline articles from Markdown via Chrome CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Weibo posts and long-form Weibo headline articles from text, media files, or Markdown. The skill fills content into a real browser session so the user can review and publish manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser and clipboard automation can act through a saved Weibo browser session and read user-provided Markdown or media files.

Mitigation: Use a dedicated Chrome profile, keep only intended files in scope, and review every filled post or article before publishing.

Risk: The npx fallback can download or run an unpinned Bun runtime.

Mitigation: Install and use a trusted Bun runtime directly in sensitive environments instead of relying on the npx fallback.

Risk: PlantUML content may be rendered through a remote data flow.

Mitigation: Avoid confidential PlantUML blocks unless remote rendering is disabled or configured to use a trusted server.

Risk: The recovery flow can kill Chrome or Chromium processes using a remote debugging port.

Mitigation: Run the skill in a dedicated browser profile or workspace so recovery does not interrupt unrelated browser automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nengnengz/skills/baoyu-post-to-weibo-2)
- [ClawHub publisher profile](https://clawhub.ai/user/nengnengz)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-weibo)
- [Weibo article editor](https://card.weibo.com/article/v3/editor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and browser-published draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Chrome or Chromium browser session, Bun runtime access, and user review before publishing.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
