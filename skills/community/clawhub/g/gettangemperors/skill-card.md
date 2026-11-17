## Description:

Query a local backend API for Tang Dynasty emperor information when the user asks about Tang emperors, needs emperor data from a local API, or references Tang Dynasty emperor terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzlpypy](https://clawhub.ai/user/hzlpypy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to query a trusted local backend for information about the first three Tang Dynasty emperors and return either human-readable text or raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a fixed GET request to a localhost service when used.

Mitigation: Install and run it only when the service at 127.0.0.1:8080 is yours or otherwise trusted.

Risk: The local backend may be unavailable, slow, or return malformed data.

Mitigation: Confirm the backend is running before use and review returned errors or raw JSON when troubleshooting.

## Reference(s):

- [gettangemperors ClawHub skill page](https://clawhub.ai/hzlpypy/skills/gettangemperors)
- [Tang Emperors local API endpoint](http://127.0.0.1:8080/api/v1/test)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code]

**Output Format:** [Plain text or JSON, with optional Markdown code blocks for shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local backend at 127.0.0.1:8080; the Python client uses a 10 second request timeout.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
