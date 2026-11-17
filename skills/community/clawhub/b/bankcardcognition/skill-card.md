## Description:

Recognizes bank-card images with OCR and returns the card number, bank name, card type, and bank identifier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process authorized bank-card images and obtain OCR fields such as card number, bank name, card type, and bank code. It is suited for workflows where an agent can safely send the image to JisuAPI and handle the returned card data with appropriate privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive bank-card images and OCR results are sent to a third-party API.

Mitigation: Use only for cards the operator is authorized to process, review JisuAPI privacy and retention terms, and avoid storing full card numbers unless necessary.

Risk: Path handling could upload an unintended local file.

Mitigation: Run the skill from a narrow working folder containing only the intended image, avoid symlinks, and review the selected file path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/bankcardcognition)
- [JisuAPI bank card recognition API documentation](https://www.jisuapi.com/api/bankcardcognition/)
- [JisuAPI provider website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON object containing recognized bank-card fields or structured error details, with natural-language guidance when used by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a local relative image path or raw base64 image content.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
