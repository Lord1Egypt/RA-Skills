## Description: <br>
CalcTool provides terminal commands that record calculation, conversion, analysis, and reporting inputs in local plaintext logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep a local activity log of calculations, conversions, comparisons, reports, and related notes when they want a searchable plaintext trail rather than a computational engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as a calculator, but the reviewed release records arbitrary user inputs in local plaintext logs. <br>
Mitigation: Treat commands as logging commands, not a trusted calculator, and verify any calculations independently before relying on them. <br>
Risk: Sensitive account data, private financial figures, customer information, proprietary notes, or secrets entered into commands may persist under ~/.local/share/calctool and later be searched or exported. <br>
Mitigation: Avoid entering sensitive data and review or delete local calctool logs before sharing the machine, backups, or exported files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/calctool) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands write timestamped local log files under ~/.local/share/calctool.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact files mention 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
