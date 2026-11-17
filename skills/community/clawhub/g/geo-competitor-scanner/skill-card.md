## Description:

Analyze competitor GEO (Generative Engine Optimization) strategies by examining content structure, Schema markup, llms.txt, and AI citation signals to benchmark a brand and identify strategic gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

Marketing, content, SEO, and developer teams use this skill to scan public brand and competitor domains for GEO signals, compare scores, and identify practical content or technical gaps. It supports competitor benchmarking and prioritized recommendations for improving AI citation readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can make outbound requests to every domain supplied by the user.

Mitigation: Use only explicit public competitor domains, review targets before execution, and run the scanner in a restricted environment.

Risk: Untrusted copied input could cause scanning of unintended domains.

Mitigation: Avoid target lists sourced from untrusted text and limit execution to approved domains.

Risk: Dependency installation can change behavior if package versions are not controlled.

Mitigation: Prefer pinned dependency installation before executing the scanner.

## Reference(s):

- [Scan Methodology](references/scan-methodology.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with competitive matrix, GEO dimension scores, and prioritized gap analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner can write the report to a user-specified output file or print it to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
