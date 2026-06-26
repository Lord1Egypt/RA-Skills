## Description: <br>
Parses and validates mainland Chinese ID card numbers offline, extracting region, birthdate, gender, and age, with format hints for Hong Kong, Macau, Taiwan, and passport documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interpret or validate Chinese identity-document numbers in an offline agent session for form checking, identity-data review, age calculation, and region extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal identifier data. <br>
Mitigation: Only process ID numbers the user is authorized to handle, and keep full ID numbers masked or otherwise minimized in outputs. <br>
Risk: A valid format and checksum do not prove that an identity document is real or officially issued. <br>
Mitigation: Present results as offline format parsing only, and use official verification channels when identity proof is required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted analysis with masked identifier excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline only; no API keys, network access, or executable code required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
