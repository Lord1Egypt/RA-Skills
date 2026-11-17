## Description:

Collects local OpenClaw conversation logs, converts eligible sessions into trajectory files, and submits them to a data collection server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miracle](https://clawhub.ai/user/miracle)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to scan local conversation records, select eligible sessions, submit conversation data, query submission history, and optionally submit scrubbed workspace or Harness files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes global OpenClaw logging settings and may capture system prompts and reasoning data.

Mitigation: Use it only after reviewing the environment changes it proposes and confirming that this level of logging is acceptable.

Risk: The skill can upload raw conversation logs and workspace or Harness configuration details.

Mitigation: Inspect generated trajectory files and archives before upload, and proceed only with data that is appropriate to submit.

Risk: A custom CLAWTRACES_SERVER_URL can redirect submissions to an untrusted endpoint.

Mitigation: Avoid custom server URLs unless the endpoint is trusted and expected for the release.

Risk: The local .clawtraces/.env key is sensitive.

Mitigation: Restrict access to the local key file and rotate credentials if the file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miracle/skills/clawtraces)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown status messages and tables, inline shell commands, JSON command output, trajectory JSON files, stats JSON files, prompt hints, session bundles, and workspace zip archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before authentication, data submission, and workspace upload steps.]

## Skill Version(s):

2.0.8 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
