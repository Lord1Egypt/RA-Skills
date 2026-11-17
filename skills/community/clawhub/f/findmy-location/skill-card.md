## Description:

Track a shared contact's location via Apple Find My with street-level accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiley](https://clawhub.ai/user/poiley)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill on macOS to query an intentionally shared Apple Find My contact location, label known places, and return a readable or JSON location result for an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles precise live location data and can track the wrong contact if the selected or default contact is not the intended person.

Mitigation: Use it only for contacts who have intentionally shared location data, configure the target contact explicitly, and verify the returned person before using the result.

Risk: Screen captures may include more than the Find My window and are written to /tmp.

Mitigation: Review local screenshot handling, remove screenshots when no longer needed, and avoid running with sensitive information visible on screen.

Risk: The optional Hammerspoon click bridge exposes a persistent local click service.

Mitigation: Avoid enabling the bridge unless it is hardened, restricted to trusted local callers, or replaced with a safer click mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poiley/skills/findmy-location)
- [peekaboo screen reading CLI](https://github.com/steipete/peekaboo)
- [Hammerspoon](https://www.hammerspoon.org/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text or JSON from a command-line script, with setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a screenshot path in /tmp when vision analysis is needed.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
