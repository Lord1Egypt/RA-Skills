## Description:

Track home furniture, schedule maintenance, and manage warranty details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to catalog home furniture, record household notes, schedule maintenance, track warranty dates, and export local records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Furniture and household notes are stored in local plaintext files.

Mitigation: Avoid recording highly sensitive details and protect access to ~/.local/share/furniture.

Risk: Exports may expose household records when shared or opened in other tools.

Mitigation: Review JSON, CSV, and text exports before sharing, and handle CSV files cautiously in spreadsheet software.

## Reference(s):

- [Furniture Skill Page](https://clawhub.ai/bytesagain3/skills/furniture)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output and local JSON, CSV, or plain text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores records locally as plaintext files under ~/.local/share/furniture.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
