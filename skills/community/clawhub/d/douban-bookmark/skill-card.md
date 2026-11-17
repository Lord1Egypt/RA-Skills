## Description:

Adds a user-requested book to the user's Douban Want to Read list using the skill's bundled automation flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinntrance](https://clawhub.ai/user/jinntrance)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to add a named book to their Douban Want to Read collection after the user has established a reusable Douban login session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reuses a persistent Playwright browser profile that may contain logged-in Douban session data.

Mitigation: Treat the profile directory as sensitive session data and delete or rotate ~/.openclaw/browser-profiles/douban-playwright when reuse is no longer desired.

Risk: The skill can make a real change to the user's Douban Want to Read list.

Mitigation: Install and run it only when the user wants the agent to make Douban wishlist changes on their behalf.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinntrance/skills/douban-bookmark)
- [Publisher Profile](https://clawhub.ai/user/jinntrance)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script reports fields such as subject_url, clicked, needs_login, and success.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
