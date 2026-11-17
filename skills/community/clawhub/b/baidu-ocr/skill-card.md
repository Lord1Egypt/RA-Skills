## Description:

Recognizes text in local images using Baidu AI OCR, including mixed Chinese and English text, tables, and formulas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to run OCR on local image files and receive recognized text or JSON output from Baidu AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships and uses hardcoded Baidu credentials that should be treated as compromised.

Mitigation: Do not use bundled credentials; rotate the exposed keys and load credentials only from secure user-controlled configuration.

Risk: Images submitted for OCR are uploaded to Baidu, and the skill under-discloses that data transfer.

Mitigation: Add clear user-facing disclosure before use and avoid submitting sensitive images unless Baidu processing is acceptable for the deployment.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installing or deploying it and confirm that credential handling and privacy disclosure have been corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nidhov01/skills/baidu-ocr)
- [Baidu OCR Official Documentation](https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm)
- [Baidu API Reference](https://ai.baidu.com/ai-doc/REFERENCE/Wk3h7x8bv)
- [Baidu OCR Product Page](https://ai.baidu.com/product/ocr)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text or JSON printed by a Python command-line script, with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Baidu API credentials; image contents are submitted to Baidu OCR endpoints for processing.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
