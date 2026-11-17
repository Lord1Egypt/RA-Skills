## Description:

Use this skill when the user wants to operate Airtap or complete a request through a mobile app on an Airtap device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-airtap](https://clawhub.ai/user/skills-airtap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Airtap to delegate mobile-app tasks to Airtap devices, monitor progress, add follow-up messages, cancel tasks, and optionally relay milestone updates into OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an Airtap personal access token and can store it in scripts/.env.

Mitigation: Use only trusted Airtap credentials, keep scripts/.env private, and avoid pasting tokens into chat.

Risk: Task text, routing data, and precise location may be written to /tmp/log.

Mitigation: Share location only when needed, avoid sensitive task text where possible, and review or clear local logs according to your retention policy.

Risk: AIRTAP_BASE_URL can redirect authenticated requests away from the official Airtap endpoint.

Mitigation: Keep AIRTAP_BASE_URL set to the official endpoint unless using separate test credentials in a controlled environment.

Risk: The skill can send authenticated task, image, and location data to Airtap and optionally mirror progress into OpenClaw.

Mitigation: Install only after review, use a locked virtual environment with pinned dependencies, and enable OpenClaw delivery only for approved destinations.

## Reference(s):

- [OpenClaw Relay](references/openclaw.md)
- [Airtap Web App](https://airtap.ai/app)
- [Airtap API Endpoint](https://airtap.ai/cortex/api)
- [ClawHub Airtap Skill Page](https://clawhub.ai/skills-airtap/skills/airtap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Airtap task identifiers, task-state summaries, follow-up prompts, cancellation results, location update responses, and optional OpenClaw relay messages.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
