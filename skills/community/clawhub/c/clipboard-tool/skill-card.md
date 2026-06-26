## Description: <br>
Perform clipboard-tool operations from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to copy, paste, clear, and transform local clipboard text from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied text or selected file contents can include sensitive data, and the first part of copied text may appear in terminal output. <br>
Mitigation: Avoid using this skill with passwords, tokens, private keys, or sensitive documents unless that exposure is acceptable. <br>
Risk: Clipboard contents may remain available to other local applications after use. <br>
Mitigation: Clear the clipboard after handling sensitive or temporary text. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May copy provided text or selected file contents to the local clipboard and may print clipboard contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
