## Description: <br>
botlearn-certify generates BotLearn capability certificates by comparing historical and fresh assessment results and producing localized HTML and Markdown certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, educators, and OpenClaw agent users use this skill to run or compare BotLearn assessments and generate localized capability certificates for certification, repeat review, or post-optimization progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad certificate-related triggers could start assessment or certification behavior when the user's intent is ambiguous. <br>
Mitigation: Confirm the user explicitly wants BotLearn certification before running assessments, reading assessment history, or creating certificate files. <br>
Risk: The setup flow can install or locate botlearn-assessment, which may change the local skill environment. <br>
Mitigation: Ask for clear consent before installing dependencies and prefer using an already verified botlearn-assessment installation. <br>
Risk: Generated certificates may include local assessment results and capability summaries that users may treat as authoritative. <br>
Mitigation: Review certificate contents for accuracy and intended audience before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-certify) <br>
- [README](README.md) <br>
- [Historical assessment retrieval flow](flows/flow1-historical.md) <br>
- [Fresh assessment execution flow](flows/flow2-fresh-exam.md) <br>
- [Certificate generation flow](flows/flow3-certificate.md) <br>
- [Dynamic comparison methodology](knowledge/comparison-methodology.md) <br>
- [Professional profile classification logic](strategies/classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Localized user-facing text plus generated Markdown and standalone HTML certificate files, with shell commands for assessment checks and result parsing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped certificate files under results/ and may read BotLearn assessment history from an installed botlearn-assessment skill.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact SKILL.md and README.md list 0.1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
