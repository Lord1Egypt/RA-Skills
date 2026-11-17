## Description:

Reviews uploaded food label images or PDFs for Chinese food-label compliance risks, generates Markdown or HTML reports, and provides risk and enforcement-case guidance for label violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyxuq](https://clawhub.ai/user/cloudyxuq)

### License/Terms of Use:

MIT-0

## Use Case:

Food manufacturers, label reviewers, and compliance teams use this skill to check uploaded label images or PDFs against Chinese food-label requirements, identify likely non-compliance, and generate review reports with correction guidance.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Optional HTML report generation can render label-derived text as active HTML or JavaScript.

Mitigation: Use Markdown output by default, or require escaped and validated HTML rendering before distributing generated reports.

Risk: Uploaded labels may be sent to OCR or model providers during text extraction and visual review.

Mitigation: Review provider privacy terms before use and avoid uploading sensitive labels unless the processing environment is approved.

Risk: Compliance findings may be incomplete or inaccurate for regulated food-label decisions.

Mitigation: Treat outputs as review aids and route final determinations to qualified legal or regulatory reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudyxuq/skills/food-label-compliance-risks)
- [Review checklist](references/review-checklist.md)
- [HTML report template](references/html-template.md)
- [Basic information risks](references/risk-01-basic-info.md)
- [Ingredients and additives risks](references/risk-02-ingredients.md)
- [Nutrition label risks](references/risk-03-nutrition.md)
- [Labeling format risks](references/risk-04-labeling-format.md)
- [Special foods risks](references/risk-05-special-foods.md)
- [Special claims risks](references/risk-06-special-claims.md)
- [Production information risks](references/risk-07-production-info.md)
- [Other food-label risks](references/risk-08-other.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Files, Guidance]

**Output Format:** [Markdown tables by default, with optional single-file HTML reports and structured review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use OCR or multimodal extraction from uploaded label images or PDFs before generating compliance findings.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
