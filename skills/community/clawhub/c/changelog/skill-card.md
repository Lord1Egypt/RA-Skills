## Description: <br>
Changelog is a command-line utility skill for quick changelog-related terminal tasks and local text-history exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to handle quick changelog-related terminal tasks such as checking, generating, formatting, linting, previewing, reporting, and exporting local entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the included script keeps command text under ~/.local/share/changelog/ and can export that history. <br>
Mitigation: Do not enter secrets, customer data, private incident notes, or confidential release details unless local plaintext retention is acceptable. <br>
Risk: The security verdict is suspicious because the included script behaves more like a local text-history and export utility than the advertised changelog generator. <br>
Mitigation: Review the script behavior before installation and run it only in environments where local history logging and export are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/changelog) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command examples and concise terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point users to local data under ~/.local/share/changelog/ and exports in json, csv, or txt when used through its shell script.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
