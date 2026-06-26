## Description: <br>
Generate an interactive family tree dashboard from any GEDCOM (.ged) file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinhartbiz](https://clawhub.ai/user/justinhartbiz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and genealogy users use this skill to turn GEDCOM family history files into a local, interactive HTML dashboard for exploring people, relationships, timelines, anniversaries, and family tree views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML embeds family data, including details that may be sensitive for living people. <br>
Mitigation: Treat the generated file as private and review or redact living-person details before sharing or hosting it. <br>
Risk: The generated HTML references Google Fonts, which can create an external request when opened in a browser. <br>
Mitigation: Remove or block the Google Fonts link when stricter privacy or offline-only use is required. <br>
Risk: Processing unintended GEDCOM files can expose or duplicate family history data into a generated HTML file. <br>
Mitigation: Use the skill only with GEDCOM files intended for processing and write outputs to a dedicated local directory. <br>


## Reference(s): <br>
- [GEDCOM Explorer ClawHub release](https://clawhub.ai/justinhartbiz/gedcom-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated single-file HTML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML embeds parsed GEDCOM data and can be opened locally without a server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
