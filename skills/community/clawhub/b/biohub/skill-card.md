## Description:

biohub lets an agent answer wellness questions using the user's local biometric, glucose, blood-panel, supplement, nutrition, and body-composition data, while keeping guidance non-medical.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxnau89](https://clawhub.ai/user/maxnau89)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent query locally stored wellness and biometric data for recovery, sleep, glucose, blood-marker, supplement, nutrition, and body-composition status checks. It is for personal wellness analysis and explicitly not medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health and biometric data that may be exposed to the agent or the user's model provider.

Mitigation: Use only health data the user is comfortable exposing, and do not write user-identifying biometric data into public or shipped files.

Risk: The backing biohub software is external and unpinned in the skill evidence.

Mitigation: Install the backing software from a specific trusted release where possible and review it before use.

Risk: Watch-folder importers and the Apple Health receiver expand the local data-ingestion surface when enabled.

Mitigation: Avoid enabling watch-folder importers or the Apple Health LAN receiver unless needed, and keep receiver exposure limited to the intended local interface.

Risk: Optional persona and profile files are editable local data and may influence agent behavior.

Mitigation: Treat persona and profile files as data, not trusted instructions, and avoid placing agent instructions in those files.

## Reference(s):

- [biohub ClawHub skill page](https://clawhub.ai/maxnau89/skills/biohub)
- [openclaw-biohub homepage](https://github.com/maxnau89/openclaw-biohub)
- [openclaw-biohub disclaimer](https://github.com/maxnau89/openclaw-biohub/blob/main/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, shell command examples, and optional JSON analytics summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should preserve non-medical boundaries and avoid writing user-identifying biometric data into shipped or public files.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
