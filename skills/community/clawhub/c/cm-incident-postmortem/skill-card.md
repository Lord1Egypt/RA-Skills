## Description: <br>
Generates structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident response teams use this skill to draft postmortems, reconstruct timelines from logs and structured incident data, check for blameful language, and produce follow-up action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident logs and generated reports can contain sensitive incident data or secrets. <br>
Mitigation: Use narrow log files, redact secrets before generating reports, and review Markdown, HTML, or JSON output before sharing. <br>
Risk: The skill runs a local Python script against incident materials. <br>
Mitigation: Install and run it only in environments where local processing of those materials is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/cm-incident-postmortem) <br>
- [Postmortem Templates & Guidelines](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, HTML, JSON, or plain text incident postmortem reports; blame-language checks return plain text findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files via -o and may include log excerpts or incident metadata from user-provided inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
