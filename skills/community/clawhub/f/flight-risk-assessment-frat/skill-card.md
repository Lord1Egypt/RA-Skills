## Description: <br>
Runs a pre-flight FRAT for pilots, dispatchers, chief pilots, and instructors by walking PAVE plus IMSAFE, scoring risk, mapping Green/Yellow/Red, and producing a draft FRAT log with mitigations while preserving the PIC's final go/no-go authority. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aviation operators, pilots-in-command, dispatchers, chief pilots, and flight-school instructors use this skill to structure a pre-flight risk assessment, document hazards and mitigations, and identify the appropriate operational review path. It supports but does not replace the qualified PIC's and operator's final authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assessment can be misleading if flight, weather, NOTAM, regulatory, maintenance, or operator inputs are incomplete or stale. <br>
Mitigation: Use current official sources supplied by the user and require qualified PIC, dispatcher, chief pilot, director of operations, or maintenance review as applicable. <br>
Risk: A draft FRAT log could be mistaken for a flight release, dispatch authorization, or final go/no-go decision. <br>
Mitigation: Keep the draft banner and authority language intact, and preserve final decision authority with the PIC and operator roles. <br>
Risk: Operational, aircraft, route, or passenger details may be sensitive. <br>
Mitigation: Collect only details needed for the assessment, avoid unnecessary passenger or personal details, and redact aircraft identifiers as directed by the skill. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft FRAT log with scored tables, risk color, named hazards, mitigations, dispatch-authority recommendation, and review banner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output is explicitly draft decision support and relies on user-supplied current aviation, weather, NOTAM, maintenance, and operator information.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
