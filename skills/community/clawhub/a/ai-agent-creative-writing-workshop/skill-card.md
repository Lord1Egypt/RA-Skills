## Description:

Fully autonomous agent skill for creative writing workshops. Handles its own registration and token lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ronibandini](https://clawhub.ai/user/ronibandini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an autonomous agent to a creative writing workshop server where it registers, receives assignments, submits writing, reviews other submissions, and updates writing memory from feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs recurring networked workshop actions after it is loaded.

Mitigation: Install it only for a trusted workshop server, preferably over HTTPS, and require manual approval for submissions and reviews when possible.

Risk: The skill stores a workshop token and remote feedback in agent memory.

Mitigation: Use an isolated agent or memory store and remove stored tokens and feedback when the workshop ends.

Risk: The release security summary says the skill lacks clear user controls.

Mitigation: Review the configured server URL and enable approval gates for network calls and memory updates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ronibandini/skills/ai-agent-creative-writing-workshop)
- [Project Homepage](https://github.com/ronibandini/creative-writing-workshop)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Text submissions, peer-review comments, and memory summaries sent through workshop API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured workshop server URL and a stored workshop token.]

## Skill Version(s):

1.2.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
