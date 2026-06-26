## Description: <br>
case.dev helps agents use the casedev CLI for encrypted legal document vaults, OCR, audio transcription, legal search, and related setup workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxsonderby](https://clawhub.ai/user/maxsonderby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Legal teams, developers, and agents use this skill to install and authenticate the casedev CLI, manage encrypted case document vaults, run OCR and transcription jobs, and search legal, web, patent, and vault sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to upload, download, search, and process sensitive legal materials through case.dev. <br>
Mitigation: Use it only with trusted case.dev accounts, protect API keys, and confirm exact vaults, files, directories, and outputs before running commands. <br>
Risk: The setup guidance includes a shell installer and broad API commands, including API URL overrides and raw endpoint calls. <br>
Mitigation: Prefer the Homebrew install path or inspect the installer first, and require explicit approval before raw API calls, API URL overrides, or operations that create or change remote data. <br>


## Reference(s): <br>
- [case.dev](https://case.dev) <br>
- [ClawHub skill page](https://clawhub.ai/maxsonderby/casedev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to use --json for machine-readable casedev CLI output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
