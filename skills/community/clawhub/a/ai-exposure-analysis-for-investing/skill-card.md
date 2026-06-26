## Description: <br>
Scores public companies on AI vulnerability and adaptive capacity using an 8-dimension AI Exposure Index with filings, O*NET workforce mappings, patents, transcripts, and valuation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martinpmm](https://clawhub.ai/user/martinpmm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and developers use this skill to evaluate how AI may affect a public company, including workforce automation exposure, revenue disruption, moat durability, adaptive capacity, and valuation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment-oriented labels and scores may be inaccurate, incomplete, or stale if public filings, transcripts, patents, or valuation metrics are misread or outdated. <br>
Mitigation: Verify cited source documents and financial metrics before relying on the report for investment decisions. <br>
Risk: The skill directs the agent to browse public financial sources, which can expose the analysis to incomplete disclosures or unreliable third-party pages. <br>
Mitigation: Prefer primary filings and company investor-relations materials, and treat third-party transcript or valuation pages as supporting evidence only. <br>
Risk: Optional Python helpers depend on external packages and local O*NET data files. <br>
Mitigation: Pin or review Python dependencies and confirm the bundled or user-provided O*NET datasets before running helper scripts. <br>


## Reference(s): <br>
- [Framework Dimensions](references/framework_dimensions.md) <br>
- [Data Collection Guide](references/data_collection_guide.md) <br>
- [O*NET Mapping Guide](references/onet_mapping_guide.md) <br>
- [Scoring Calculations](references/scoring_calculations.md) <br>
- [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar) <br>
- [SEC EDGAR Full-Text Search](https://efts.sec.gov/) <br>
- [Google Patents](https://patents.google.com/) <br>
- [O*NET Resource Center Database](https://www.onetcenter.org/database.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown report with inline tables and optional shell-command snippets for local helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces company-specific AI exposure scores, composite vulnerability and adaptive-capacity metrics, matrix classification, valuation overlay, scenario sensitivity, and risks or catalysts.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
