## Description: <br>
Extracts structured case documents from chat records or spoken experience using the SPAS case-extraction method. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, consultants, and knowledge managers use this skill to review interview or chat material, identify missing SPAS interview coverage, and turn qualified experience narratives into structured case documents for training or best-practice sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive interview, customer, or internal chat content may be processed by the skill. <br>
Mitigation: Use only files the user is authorized to process and avoid confidential material unless the deployment environment and retention policy are approved. <br>
Risk: The optional parser can persist cleaned chat content in a predictable _cleaned_temp.txt side file next to the source file. <br>
Mitigation: Disable or modify the side-file behavior before use with sensitive data, or explicitly approve and manage the storage location. <br>


## Reference(s): <br>
- [Case Extraction ClawHub page](https://clawhub.ai/pengpengliu1212-art/case-extraction) <br>
- [SPAS model reference](references/spas-model.md) <br>
- [Case output template](references/case-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance and structured Word document output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce supplemental interview questions when source material lacks required SPAS coverage; the optional parser can write a _cleaned_temp.txt side file next to processed chat files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
