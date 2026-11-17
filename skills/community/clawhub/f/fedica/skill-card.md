## Description:

Compose and schedule cross-platform social posts on Fedica (X, LinkedIn, Threads, Mastodon, Bluesky) via agent-browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkobject](https://clawhub.ai/user/jkobject)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through composing, scheduling, verifying, editing, and troubleshooting public social posts in Fedica across connected social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates an authenticated Fedica session that can publish public social posts.

Mitigation: Require explicit confirmation of final post text, target platforms, and local scheduled time before any post, schedule, or update action.

Risk: The documented server workflow may launch the browser with no sandbox.

Mitigation: Prefer running the browser with sandboxing enabled where possible, and use an isolated environment when no-sandbox mode is required.

Risk: The prerequisite installation uses an unpinned global agent-browser package.

Mitigation: Prefer a pinned, local, or isolated agent-browser installation before using the skill.

Risk: Fedica displays scheduling times in GMT+00, which can cause posts to be scheduled at the wrong local time.

Mitigation: Convert the user's local scheduled time to UTC before entry, then re-verify the displayed scheduled time after saving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkobject/skills/fedica)
- [Publisher profile](https://clawhub.ai/user/jkobject)
- [Fedica](https://fedica.com)
- [Fedica dashboard](https://fedica.com/dash/)
- [Fedica composer](https://fedica.com/publish/)
- [Fedica scheduled queue](https://fedica.com/schedule/)
- [agent-browser](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash commands and browser automation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Fedica session, agent-browser, and explicit user confirmation before posting, scheduling, or updating public content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
