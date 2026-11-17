## Description:

Analyzes public companies with an 8-dimension AI Exposure Index using filings, transcripts, patent research, O*NET workforce mappings, and valuation comparisons to classify AI vulnerability and adaptive capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpmm](https://clawhub.ai/user/martinpmm)

### License/Terms of Use:


## Use Case:

External users and investment researchers use this skill to evaluate how AI may affect a public company's risk profile, adaptive capacity, competitive moat, and valuation posture. The output is an evidence-based analyst-style report, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-oriented classifications can be misleading if source filings, transcripts, patents, valuation data, or citations are incomplete or misread.

Mitigation: Verify all cited evidence and treat the report as research support rather than financial advice.

Risk: The skill performs public web research and may rely on changing third-party pages for financial and company data.

Mitigation: Use current public sources, preserve citations, and note data gaps or confidence limits in the final report.

Risk: Python helper execution requires third-party packages and local O*NET data parsing.

Mitigation: Run helpers in an isolated environment with pinned or locked dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/martinpmm/skills/ai-exposure-analysis-for-investing)
- [Framework Dimensions](references/framework_dimensions.md)
- [Data Collection Guide](references/data_collection_guide.md)
- [O*NET Mapping Guide](references/onet_mapping_guide.md)
- [Scoring Calculations](references/scoring_calculations.md)
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar)
- [SEC EDGAR full-text search](https://efts.sec.gov/)
- [Google Patents](https://patents.google.com/)
- [O*NET Resource Center](https://www.onetcenter.org/database.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables and cited research evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Python helper commands for O*NET lookup and score calculation; conclusions should be reviewed before relying on investment-oriented classifications.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
