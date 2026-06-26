## Description: <br>
Get Unicode codepoint, name, and category for characters, including Chinese characters, English text, and emoji, using the Python standard library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and text-processing users can use this skill to inspect unknown characters, debug encoding issues, and extract Unicode properties for supplied text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary states that available scans are clean but the exact skill files were not available for a full artifact review. <br>
Mitigation: Before installation, confirm the listed files and SHA-256 hashes match the release evidence and that the files match the Unicode lookup purpose. <br>
Risk: The skill runs a local Python script on user-supplied text. <br>
Mitigation: Review the script before execution and avoid placing sensitive text directly in shell history or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-unicode-info) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints JSON containing per-character codepoint, Unicode name, category, and total input length.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
