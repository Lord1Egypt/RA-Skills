## Description: <br>
Claw Asset & Privacy Guardian helps agents run local privacy and digital-asset security checks, identify credential and account-security risks, and produce anonymized reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BetsyMalthus](https://clawhub.ai/user/BetsyMalthus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals, developers, security teams, and enterprise reviewers use this skill to scan local files and account or privacy configurations for sensitive information exposure, weak security posture, and digital-asset risks. It is intended to generate local, anonymized findings and remediation guidance without sending scanned data to external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads directories selected by the user and may process sensitive local files during scans. <br>
Mitigation: Run it only on directories you intend to scan and configure exclusions for files or folders that should not be inspected. <br>
Risk: Generated JSON, console, Markdown, or HTML reports may include filenames, partial paths, and operational context even when secret values are redacted. <br>
Mitigation: Keep reports private by default and review them before sharing or attaching them to tickets, audits, or public discussions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BetsyMalthus/claw-asset-privacy-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console summaries, JSON reports, Markdown reports, HTML reports, CLI examples, Python API examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are designed to be anonymized and local, but generated reports may still include filenames, partial paths, and operational context.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
