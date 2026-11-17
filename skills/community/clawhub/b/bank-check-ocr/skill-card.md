## Description:

Recognizes key fields on bank checks, including check numbers, dates, written and numeric amounts, and signatures or stamps, only when the user explicitly requests bank-check OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers with authorization to process bank-check images use this skill to send a specified check image to SCNet OCR and receive structured check-field extraction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive bank-check images and credentials can be sent to SCNet or a configured OCR endpoint.

Mitigation: Install only when this data transfer is acceptable, keep SCNET_API_BASE on the official HTTPS SCNet endpoint, and process checks only with authorization from the account holder or signer.

Risk: Input validation can be bypassed with symlinked files.

Mitigation: Do not process symlinked files, and review the resolved absolute path before sending a check image for OCR.

Risk: Bank-check images may contain account numbers, signatures, stamps, and payment amounts that could enable financial fraud if mishandled.

Mitigation: Upload only the minimum required check image, avoid unrelated sensitive content, and follow the provider's retention and deletion guidance after receiving results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/bank-check-ocr)
- [SCNet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Bank-check OCR field summary](assets/templates/fields-summary.md)
- [SCNet OCR API endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results with text guidance and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs structured OCR data from the API response and friendly error messages for configuration, authentication, unsupported files, rate limits, and network failures.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, skill.yaml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
