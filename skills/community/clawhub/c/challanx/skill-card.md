## Description:

ChallanX helps agents use the ChallanX OpenClaw API for RTO, challan, RC lookup, and media download workflows from a URL, message, or image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajniwebdeveloper](https://clawhub.ai/user/rajniwebdeveloper)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to produce concise ChallanX API guidance, curl examples, response formats, and bootstrap reminders for media and vehicle lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin can inject ChallanX guidance into primary agent bootstrap sessions, beyond an explicit user-invoked lookup or download task.

Mitigation: Install it only in workspaces where ChallanX guidance should affect primary agent sessions, and review the injected reminder and instruction files before use.

Risk: Submitted URLs, messages, or images may be sent to the ChallanX endpoint under the configured API key.

Mitigation: Set CHALLANX_API_KEY as a runtime secret and submit only data approved for ChallanX processing.

## Reference(s):

- [ChallanX API Reference](artifact/references/api.md)
- [ChallanX public OpenClaw API endpoint](https://challanx.in/openclaw/api)
- [ClawHub skill page](https://clawhub.ai/rajniwebdeveloper/skills/challanx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference downloadable media filenames, content types, ChallanX status names, and x-api-key authentication requirements.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
