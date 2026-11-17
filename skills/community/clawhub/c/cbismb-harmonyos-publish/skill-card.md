## Description:

Automates publishing articles to the HarmonyOS section of cbismb.com when a user asks to publish to the CBISMB HarmonyOS developer community.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itcastwsy](https://clawhub.ai/user/itcastwsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through publishing HarmonyOS articles on cbismb.com, including article content, category, tags, originality, privacy agreement, and comment settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post live articles to cbismb.com using the user's logged-in browser session.

Mitigation: Review the generated title, body, category, tags, originality setting, privacy checkbox, and comments setting before allowing the final publish action.

Risk: A user may not be ready for immediate publication.

Mitigation: Use the draft option when content should be saved but not published live.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itcastwsy/skills/cbismb-harmonyos-publish)
- [CBISMB HarmonyOS publishing page](https://www.cbismb.com/harmonyos/release)
- [CBISMB HarmonyOS section home](https://www.cbismb.com/harmonyos/home)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Browser actions]

**Output Format:** [Markdown instructions with browser action steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate live posting actions through an attached browser session.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
