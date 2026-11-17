## Description:

智能文档处理专家，支持文档解析、信息抽取、文档分类。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankylala](https://clawhub.ai/user/ankylala)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse PDFs, images, Word, Excel, and CSV files, extract structured fields with source evidence, and classify or split mixed document sets. Typical workflows include contract review, finance audits, archive organization, form processing, and compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected documents to the DocPilot/TokenAI service or another configured endpoint, and privacy controls are under-documented.

Mitigation: Use only documents approved for that external service until the publisher documents retention, deletion, jurisdiction, and privacy terms.

Risk: The bundled configuration includes credential-like data and can override environment variables.

Mitigation: Remove bundled secrets, rotate any exposed credentials, and require deployers to provide API keys through approved secret management.

Risk: The service destination is configurable, which can send document contents to an unexpected endpoint.

Mitigation: Restrict deployment to approved HTTPS destinations and review endpoint configuration before each release.

Risk: Dependencies are not pinned.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ankylala/skills/docpilot)
- [DocPilot Service Endpoint](https://docpilot.token-ai.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON, Markdown, or plain text document-processing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parse outputs may include document IDs, page counts, layout elements, tables, seals, bounding boxes, and markdown; extraction and classification outputs include structured fields, evidence, segments, confidence, and metadata.]

## Skill Version(s):

2.0.4 (source: server release evidence; source files report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
