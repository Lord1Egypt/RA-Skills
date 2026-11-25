## Description:

Finds high-confidence positive, failure, and boundary samples in raw dialogue data, then clusters them and derives candidate rules for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jd-aicc-agent](https://clawhub.ai/user/jd-aicc-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to examine large raw dialogue or ASR transcription datasets, identify candidate positive, failure, and boundary cases, and develop patterns for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that credentials and dialogue content may be sent without encryption.

Mitigation: Avoid sending secrets or sensitive dialogue through unverified endpoints; confirm transport protection before processing data.

Risk: The security assessment reports privacy concerns when handling raw conversations.

Mitigation: Use only authorized data, remove or mask personal information where possible, and limit access to input and generated files.

Risk: The security assessment reports that configuration accepts plaintext API keys.

Mitigation: Keep API keys in a protected secret store or environment variables, restrict access to local configuration files, and do not commit secrets.

Risk: The security assessment was partial because a referenced local path was missing, so its review may be incomplete.

Mitigation: Review the missing path and complete a security scan of the full release before deployment.

## Reference(s):

- [Dialog Discovery on ClawHub](https://clawhub.ai/jd-aicc-agent/skills/dialog-discovery)
- [Publisher profile: jd-aicc-agent](https://clawhub.ai/user/jd-aicc-agent)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Candidate rules and review guidance]

**Output Format:** [JSON and Markdown files with candidate rules and analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weak-supervision buckets and extracted rules are candidates for human review, not final dialogue labels.]

## Skill Version(s):

0.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
