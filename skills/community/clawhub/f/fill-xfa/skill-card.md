## Description: <br>
Fill XFA (Adobe LiveCycle) PDF forms programmatically by discovering embedded XML field names, setting values, and writing an updated PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiagentkronos-cell](https://clawhub.ai/user/kiagentkronos-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and fill Adobe LiveCycle XFA PDF forms when standard AcroForm-oriented PDF tools do not work. It is suited for local form-filling workflows that need JSON, stdin, or command-line field input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive form data can appear in terminal output, logs, or shared transcripts because the helper prints written field values after saving the PDF. <br>
Mitigation: Run the tool in a trusted local environment and avoid sharing logs or transcripts that contain filled form values. <br>
Risk: Incorrect field names or duplicate-field handling can leave expected values unwritten or written to repeated fields. <br>
Mitigation: Use the fields command to discover field names first, review warnings for missing fields, and inspect the generated PDF before using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kiagentkronos-cell/fill-xfa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python command examples, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command guidance and can run a helper script that writes filled PDF files when used by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
