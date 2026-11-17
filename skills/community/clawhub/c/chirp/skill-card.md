## Description:

X/Twitter CLI using OpenClaw browser tool for reading timelines, posting tweets, liking, reposting, replying, following profiles, and searching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zizi-cat](https://clawhub.ai/user/zizi-cat)

### License/Terms of Use:


## Use Case:

Developers and agent users use Chirp to operate a logged-in X/Twitter browser session through OpenClaw when they need timeline inspection, search, or public account actions without installing a separate CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in X/Twitter browser session and perform public account actions.

Mitigation: Use it only with an account and browser profile you are comfortable delegating to an agent, and review the session state before use.

Risk: Likes, reposts, replies, follows, and posts may be executed without consistent confirmation.

Mitigation: Require the agent to show the exact target account or post and any generated content, then wait for explicit approval before each public action.

Risk: Browser UI references can change between snapshots, which can cause the agent to act on the wrong control.

Mitigation: Take a fresh compact browser snapshot before each action and verify the current ref, label, target, and enabled state before clicking or typing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zizi-cat/skills/chirp)
- [Project homepage from artifact frontmatter](https://github.com/zizi-cat/chirp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser action command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw browser tooling, an openclaw browser profile, and a logged-in X/Twitter session.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
