## Description: <br>
Back up, analyze, and reuse ChatGPT | Claude | Codex | Cursor | DeepSeek | Qwen | Openclaw data + skills + attachments locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[max-ng](https://clawhub.ai/user/max-ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI tool users use this skill to install DataMoat, check local protection status, and route export, analysis, backup, restore, and reuse requests into the local DataMoat desktop UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DataMoat can start broad background capture of local AI conversation records and attachments before desktop setup is complete. <br>
Mitigation: Install only with explicit user consent, run the status check first, and complete password and recovery setup locally in the desktop app. <br>
Risk: The Linux installer fetches and runs current source code, which gives weaker supply-chain control than a pinned checksum-verified package. <br>
Mitigation: Use the official site or a pinned, verified release when stronger supply-chain assurance is required. <br>
Risk: The skill interacts with sensitive local AI work history and recovery setup boundaries. <br>
Mitigation: Do not handle passwords, authenticator codes, recovery phrases, or unlock steps in chat; keep those steps in the local DataMoat UI. <br>


## Reference(s): <br>
- [ClawHub Data Moat Plugin](https://clawhub.ai/max-ng/datamoat) <br>
- [DataMoat official site](https://datamoat.org) <br>
- [DataMoat latest release manifest](https://downloads.datamoat.org/releases/latest/manifest.json?s=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and PowerShell command blocks plus concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report local protection counts, install status, exit-code outcomes, and next-step UI handoff instructions.] <br>

## Skill Version(s): <br>
2.0.9 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
