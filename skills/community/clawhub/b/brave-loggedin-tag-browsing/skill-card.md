## Description:

Uses a logged-in Brave browser session to browse X/Twitter or Facebook profile pages and extract recent posts, profile details, login status, and optional engagement stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sean810720](https://clawhub.ai/user/sean810720)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to collect recent posts, profile metadata, login status, and engagement counts from X/Twitter or Facebook accounts through an already logged-in Brave session for monitoring, analysis, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a logged-in browser session and may access a broad browser profile, existing tabs, and account state.

Mitigation: Use a dedicated Brave or Chrome profile containing only the X/Facebook accounts needed for this task, and avoid using a normal profile or sensitive tabs.

Risk: The security summary notes weakened browser sandboxing and profile isolation concerns.

Mitigation: Run the skill only in an isolated environment and avoid sensitive or high-privilege accounts until sandboxing and profile isolation are fixed.

Risk: The skill automates scraping of social-media pages through authenticated sessions.

Mitigation: Use it only for authorized monitoring or analysis and confirm the target platform terms and account permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sean810720/skills/brave-loggedin-tag-browsing)
- [Publisher profile](https://clawhub.ai/user/sean810720)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON object containing username, platform, login status, profile, posts, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post count is controlled by maxPosts; engagement stats are optional.]

## Skill Version(s):

2.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
