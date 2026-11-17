## Description:

Building and maintaining social connections as an adult. Use when someone is lonely, has moved to a new city, wants to make friends, struggles in group settings, or needs to rebuild a social life.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to get practical guidance for building adult friendships, joining group conversations, hosting gatherings, and maintaining social ties. It is intended for ordinary social skill-building and should refer users with severe social anxiety toward appropriate support before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports an unnecessary filesystem requirement for a guidance-focused social skills prompt.

Mitigation: Install or run the skill in a least-privileged environment without exposing unrelated local files or credentials, and prefer a release that removes or tightly scopes filesystem access.

Risk: The server security summary reports an unpinned installer command.

Mitigation: Pin the installer or package version before deployment and review the resolved artifact hash against the server-provided release hash.

## Reference(s):

- [Robin Dunbar](https://www.robin-dunbar.com)
- [Shasta Nelson](https://www.shastanelson.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured steps, scripts, checklists, and YAML state snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides adaptive social advice and may maintain simple session state fields when supported by the agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
