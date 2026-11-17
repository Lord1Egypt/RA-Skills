## Description:

Searches open-access Chinese medical literature, downloads available PDFs, formats citations, and checks references against source records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and writers use this skill to find open-access Chinese medical papers, collect citation metadata and available PDFs, and check Chinese references before citing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical-literature search terms are sent to Weipu OA and Yiigle.

Mitigation: Avoid including private patient details or other sensitive information in queries.

Risk: Downloaded PDFs and citation metadata are stored locally.

Mitigation: Set an explicit output directory and review its contents and access permissions.

Risk: An optional base-URL setting can redirect Weipu requests.

Mitigation: Leave WEIPU_OA_BASE unset unless the intended destination is trusted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/docsor1212/skills/cn-med-oa)
- [Weipu OA API contract](references/weipu-oa-api-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Text and Markdown; optional JSON, RIS, HTML reports, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Citation metadata and verification outcomes; downloaded PDFs and reports are saved locally when requested.]

## Skill Version(s):

2.4.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
