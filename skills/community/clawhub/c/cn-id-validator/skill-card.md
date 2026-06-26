## Description: <br>
Validates 15- and 18-digit Chinese ID numbers and extracts region code, birth date, and gender when the format checks pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a local Python validator for Chinese ID number format checks, checksum checks, and basic demographic extraction. It is suitable for form validation or data-quality workflows, not authoritative identity verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ID numbers are personal data; sample or production inputs may expose sensitive information in terminal output. <br>
Mitigation: Use synthetic or consented values, avoid logging outputs unnecessarily, and handle results under the same controls as source ID data. <br>
Risk: The artifact states it validates format and checksum only and does not query government databases. <br>
Mitigation: Use results as a local format and data-quality signal, not as proof of legal identity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-id-validator) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact validator script](artifact/scripts/id_validator.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the script itself emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python 3 script with no external dependencies; outputs valid/invalid status and extracted fields when validation succeeds.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
