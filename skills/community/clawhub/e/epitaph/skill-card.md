## Description:

Scans a user's logged-in social media accounts and produces a poetic, data-driven Digital Epitaph summarizing posts, saved items, unfinished plans, hidden interests, and recurring themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect a user's own social-media footprint from supported logged-in accounts and turn it into a humorous, reflective Markdown life summary. It is intended for self-reflection and shareable personal writing, with local handling of collected data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to control a logged-in browser session across social platforms and can collect sensitive profile details, likes, favorites, follows, comments, IDs, and other account data.

Mitigation: Use a separate browser profile, approve each data category explicitly, keep collected data local, and delete raw data when the final summary is no longer needed.

Risk: The security verdict is suspicious because sensitive account data is consolidated locally with weak controls.

Mitigation: Review the skill before execution, avoid saving raw data unnecessarily, and do not store ManoBrowser API keys in shared configuration files.

Risk: The browser automation dependency can expand the agent's practical access to logged-in accounts.

Mitigation: Pin or manually review ManoBrowser before use and confirm the browser-control connection is limited to the intended session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophie-xin9/skills/epitaph)
- [Publisher profile](https://clawhub.ai/user/sophie-xin9)
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown Digital Epitaph with supporting browser setup and collection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May consolidate raw local social-media data before producing the final Markdown summary.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
