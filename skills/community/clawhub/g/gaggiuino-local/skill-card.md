## Description: <br>
Gaggiuino skill for machine control, espresso shot analysis through profile intent, dial-in guidance, shot graph rendering, and synchronized overlay videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zackzmai](https://clawhub.ai/user/zackzmai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with a trusted local Gaggiuino machine: checking status, selecting profiles, reading or updating settings, analyzing shot telemetry, and rendering shot graph or overlay artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Machine-control commands can change the active profile or settings on a real local Gaggiuino machine. <br>
Mitigation: Use the skill only with the user's own trusted machine, review profile switches and settings payloads before sending them, and confirm machine state after changes. <br>
Risk: The saved base URL determines which local API endpoint receives machine commands. <br>
Mitigation: Keep the saved base URL pointed at a trusted LAN host or mDNS name, and clear or update stale addresses instead of using untrusted remote endpoints. <br>
Risk: Rendering commands can write to custom output paths and may overwrite files. <br>
Mitigation: Prefer the standard Gaggiuino output directory or review custom output paths before running graph or overlay rendering. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zackzmai/gaggiuino-local) <br>
- [Analysis protocol](references/analysis-protocol.md) <br>
- [Dial-in basics](references/dial-in-basics.md) <br>
- [Extraction levers](references/extraction-levers.md) <br>
- [Profile descriptions](references/profile-descriptions.md) <br>
- [Profile families](references/profile-families.md) <br>
- [Profile mapping](references/profile-mapping.md) <br>
- [Shot graph analysis](references/shot-graph-analysis.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Gaggiuino community profiles](https://github.com/Zer0-bit/gaggiuino/tree/community/profiles) <br>
- [Espresso Aficionados guides](https://espressoaf.com/guides) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PNG and MP4 files when graph or overlay rendering commands are run.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
