## Description: <br>
Extracts and parses content from HTTP(S) URLs across supported platforms using the ListenHub/Marswave content extraction API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to extract normalized text, metadata, and references from supported URLs before reading, summarizing, or passing the content into another agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs and extracted content are sent to the ListenHub/Marswave API. <br>
Mitigation: Use the skill only with URLs you are comfortable sharing with that API, and avoid private, internal, signed, regulated, or confidential links unless that sharing is approved. <br>
Risk: When autoDownload is enabled, extracted Markdown and raw API responses may be saved in the current working directory. <br>
Mitigation: Disable autoDownload or run the skill in an appropriate working directory when handling sensitive content. <br>
Risk: Some supported platforms may return partial, truncated, blocked, or unavailable content. <br>
Mitigation: Review extracted output before relying on it or passing it into downstream generation workflows. <br>


## Reference(s): <br>
- [Supported Platforms](references/supported-platforms.md) <br>
- [Content Parser on ClawHub](https://clawhub.ai/0xFANGO/content-parser) <br>
- [Marswave Content Extract API](https://api.marswave.ai/openapi/v1/content/extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and JSON request examples; optional Markdown and JSON extracted-content files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write extracted content and raw API responses to the current working directory when autoDownload is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
