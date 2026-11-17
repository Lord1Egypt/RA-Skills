## Description:

Gaggiuino Local helps agents control local Gaggiuino espresso machines, analyze shot telemetry against profile intent, provide dial-in guidance, manage profiles and settings, and render shot graphs or synchronized overlay videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zackzmai](https://clawhub.ai/user/zackzmai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate and inspect a trusted local Gaggiuino espresso machine, analyze current or historical shots, manage profiles and settings, and produce shot visualizations for dial-in decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save an arbitrary API address and later send machine settings or control requests to that address.

Mitigation: Use only a trusted Gaggiuino machine on the local network, avoid remote or unfamiliar base URLs, and clear the saved base URL if it appears stale or unexpected.

Risk: Profile switching or settings updates can affect the real espresso machine.

Mitigation: Confirm the target machine, selected profile, and setting category before changes; prefer status, export, and read-only checks before updates.

## Reference(s):

- [Analysis Protocol](references/analysis-protocol.md)
- [Dial-In Basics](references/dial-in-basics.md)
- [Extraction Levers](references/extraction-levers.md)
- [Profile Descriptions](references/profile-descriptions.md)
- [Profile Families](references/profile-families.md)
- [Profile Mapping](references/profile-mapping.md)
- [Shot Graph Analysis](references/shot-graph-analysis.md)
- [Troubleshooting](references/troubleshooting.md)
- [espressoaf guides](https://espressoaf.com/guides)
- [Gaggiuino community profiles](https://github.com/Zer0-bit/gaggiuino/tree/community/profiles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with shell commands, JSON/API summaries, and optional PNG or MP4 visualization files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visualization outputs may include static shot graphs, animated shot graphs, or synchronized video overlays generated from local shot data.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
