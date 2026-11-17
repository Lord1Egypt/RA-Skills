## Description:

Generates English hospital recommendation reports for medical travel to China, using patient intake to produce three default hospital matches with specialist-direction guidance, cost and logistics context, evidence notes, and Markdown/PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helenalhq](https://clawhub.ai/user/helenalhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to turn paid medical-travel intake into an English hospital matching report for China. It supports a reasoned hospital shortlist, specialist direction, cost and logistics context, evidence notes, next steps, and delivery-ready Markdown/PDF files.

### Deployment Geography for Use:

Global; report content is scoped to medical travel to China.

## Known Risks and Mitigations:

Risk: Generated reports can be written outside the requested output folder when untrusted report_id or --basename values are used.

Mitigation: Use only trusted basenames, sanitize path-like values before rendering, and write reports to a private output directory until filename containment is fixed.

Risk: Every generated report appends branded ChinaMed Select consult-service contact text.

Mitigation: Confirm that this branding and contact text is appropriate for the release and disclose or remove it before using the output in another service context.

Risk: Reports may contain sensitive patient and medical-travel information.

Mitigation: Store generated Markdown and PDF files only in private locations with access limited to the intended operators and recipients.

## Reference(s):

- [Product Brief](references/product-brief.md)
- [Report Schema](references/report-schema.md)
- [Specialty Mapping](references/specialty-mapping.md)
- [Fudan Rankings 2025 Snapshot](references/fudan-rankings-2025.md)
- [Recommendation Method](references/recommendation-method.md)
- [Search Policy](references/search-policy.md)
- [PDF Spec](references/pdf-spec.md)
- [Quality Checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and PDF files generated from structured JSON input, with patient-facing English report text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to three recommended hospitals unless the input includes a justified expansion reason.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
