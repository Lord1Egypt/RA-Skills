## Description:

Analyze single-lead and 12-lead ECG signal JSON files through the HeartVoice cloud API and return structured diagnostic results in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujiecharles](https://clawhub.ai/user/yujiecharles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze user-provided ECG JSON files for heart rhythm, interval, signal quality, and abnormality indicators through HeartVoice's cloud ECG service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ECG signal data is transmitted to HeartVoice's external cloud API for analysis.

Mitigation: Confirm user intent before upload, avoid identifying metadata in JSON files, and use the skill only when external processing is acceptable.

Risk: The skill requires a HEARTVOICE_API_KEY in the runtime environment.

Mitigation: Store the API key as a runtime secret, avoid hardcoding it, and run the skill in an isolated environment with pinned dependencies where possible.

Risk: AI-assisted ECG analysis can be misunderstood as a definitive medical diagnosis.

Mitigation: Present results as decision support and direct users to qualified medical professionals for diagnosis or treatment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujiecharles/skills/ecg-ai-diagnosis)
- [HeartVoice AI ECG Cloud](https://www.heartvoice.com.cn/aiCloud)
- [HeartVoice official site](https://www.heartvoice.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language report with structured JSON fields from the analysis script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HEARTVOICE_API_KEY and explicit 1-lead or 12-lead mode; supports Chinese and English summaries.]

## Skill Version(s):

0.9.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
