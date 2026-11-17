## Description:

生成企业技术专利竞争分析报告，梳理竞争格局、对手动向与专利布局。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External business, strategy, and IP teams use this skill to analyze a named company's patent position and competitors in a defined technology area, then review the Word report as competitive-intelligence input. It does not replace legal advice or guarantee complete patent coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background documents may be shared with PatentMax without sufficient disclosure.

Mitigation: Confirm which documents may be sent and omit confidential material unless sharing is authorized.

Risk: Saved API keys may not be adequately protected.

Mitigation: Keep production keys out of chat and use protected credential storage.

Risk: Authenticated requests may reach unapproved destinations through cross-origin redirects.

Mitigation: Restrict authenticated requests to approved HTTPS destinations and reject cross-origin redirects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/company-patent-analysis)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Workflow guide](references/workflow.md)
- [Materials guide](references/materials-guide.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Word (.docx) patent competition report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronously generated; report coverage and quality may vary.]

## Skill Version(s):

1.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
