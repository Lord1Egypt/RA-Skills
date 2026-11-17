## Description:

Agent Knowledge Format helps agents stamp trust metadata into files they create or modify, including DOCX, PDF, images, and code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check, stamp, inspect, and audit trust metadata on files handled by AI agents. It supports workflows for provenance tracking, confidence scoring, sensitivity labeling, and replayable evidence checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external package installs that may change over time.

Mitigation: Pin and verify the exact package versions before installation, especially in production or shared agent environments.

Risk: `akf replay --run` can execute commands recorded in inspected files.

Mitigation: Review the recorded command, require explicit approval, and run it only in a sandbox without sensitive credentials for untrusted artifacts.

## Reference(s):

- [AKF Website](https://akf.dev)
- [AKF GitHub Repository](https://github.com/HMAKT99/AKF)
- [AKF v1.1 Schema](https://github.com/HMAKT99/AKF/blob/main/spec/akf-v1.1.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/hmakt99/skills/akf)
- [ClawHub Publisher Profile](https://clawhub.ai/user/hmakt99)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use the external akf CLI and related package commands when available.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
