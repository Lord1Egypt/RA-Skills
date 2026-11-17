## Description:

调用文档转换全能王(https://www.wdangz.com)API进行文档格式转换，支持PDF、Word、Excel、PPT、图片等格式互转、OCR识别，以及PDF合并、拆分、加密等处理，并将转换结果下载到原文件目录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daizhenping012](https://clawhub.ai/user/daizhenping012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to convert ordinary non-sensitive office documents and images through the WDangz document conversion API. It is intended for file format conversion, OCR, and PDF utility tasks when uploading the selected file to a third-party service is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents and the WDANGZ_API_KEY are sent to wdangz.com for conversion.

Mitigation: Use the skill only for ordinary non-sensitive or already redacted documents, and do not use it for contracts, financial records, credentials, personal IDs, regulated data, or confidential business files.

Risk: Converted files are written to the source file directory by default and may collide with an existing generated filename.

Mitigation: Check the output directory before and after conversion, and move or rename existing files when preserving prior outputs matters.

Risk: The conversion service requires an API key.

Mitigation: Configure WDANGZ_API_KEY only through the environment variable path supported by the skill, and avoid storing the key in local plaintext configuration files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/daizhenping012/skills/docs-converter)
- [WDangz document conversion service](https://www.wdangz.com)
- [WDangz conversion API endpoint](https://www.wdangz.com/api/v1/convert)
- [WDangz conversion status endpoint](https://www.wdangz.com/api/v1/checkState)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with command examples and locally downloaded converted files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted files are saved to the source file directory by default; the skill requires WDANGZ_API_KEY and supports files up to 50 MB.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
