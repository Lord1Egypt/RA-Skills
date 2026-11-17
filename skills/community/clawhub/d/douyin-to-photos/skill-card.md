## Description:

Build and maintain an Apple Shortcuts workflow that takes a Douyin share link, resolves a no-watermark MP4 URL via configurable backend APIs, saves the video into the Photos app, and cleans temporary cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahnxu](https://clawhub.ai/user/vahnxu)

### License/Terms of Use:


## Use Case:

External users and shortcut builders use this skill to create or maintain a one-tap Apple Shortcuts workflow that saves authorized Douyin videos into Photos. It is useful for Share Sheet or clipboard-triggered workflows that need configurable resolver APIs, validation, error handling, and local cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared Douyin links are sent to TikWM or a configured resolver API.

Mitigation: Use trusted resolver providers, prefer a self-hosted fallback when appropriate, and avoid arbitrary parser APIs.

Risk: Downloaded media is added to the user's Photos library.

Mitigation: Confirm the workflow validates real Douyin hostnames and prompts or clearly signals before saving media.

Risk: Users may process content they are not allowed to download or store.

Mitigation: Process only links the user has rights to save and do not use the workflow to bypass paid, member-only, or protected access controls.

## Reference(s):

- [Shortcut Build Guide](references/shortcut-build-guide.md)
- [Resolver Script](scripts/fetch_douyin_no_watermark.sh)
- [ClawHub Skill Page](https://clawhub.ai/vahnxu/skills/douyin-to-photos)
- [ClawHub Publisher Profile](https://clawhub.ai/user/vahnxu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Apple Shortcuts workflow instructions, resolver script usage, configurable API settings, and validation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
