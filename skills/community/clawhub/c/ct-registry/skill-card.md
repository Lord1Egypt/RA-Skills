## Description:

Cross-source search of global clinical-trial registries (ClinicalTrials.gov, CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP, PubChem), normalizes and aggregates phase/status/sponsor/timeline/competitor landscape into JSON/Markdown for trial planning, de-duplication, control-design benchmarking, and competitive intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Clinical-trial researchers and planning teams can search public registries, remove duplicate records, compare trial designs, and review phase, status, sponsor, timeline, and competitor landscapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags data-sharing and document-processing concerns, and review coverage is incomplete.

Mitigation: Review the skill's outbound data behavior before use, avoid sending sensitive text, and decide whether its external network features fit your needs.

Risk: The security assessment reports cleanup and file-path risks.

Mitigation: Review file destinations and cleanup behavior before enabling document processing or downloads.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/medstatstar/skills/ct-registry)
- [ct-series web portal](https://ct.medstatstar.com)
- [Search procedure](references/search_procedure.md)
- [Retrieval time and data-volume guide](docs/retrieval_guide.md)

## Skill Output:

**Output Type(s):** [Trial landscape analysis, JSON, Markdown, Excel workbook, PNG charts]

**Output Format:** [JSON and Markdown summaries, Excel workbooks, and optional PNG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language follows the user's English or Chinese setting; broad searches may return partial results.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
