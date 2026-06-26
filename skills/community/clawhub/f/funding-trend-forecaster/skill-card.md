## Description: <br>
Predict funding trend shifts using NLP analysis of grant abstracts from NIH, NSF, and Horizon Europe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate funding trend analyses, forecasts, and report files from research-grant abstract data or the artifact's simulated dataset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports and forecasts may appear to analyze real grant data while the artifact generates mock project data. <br>
Mitigation: Label outputs as simulated unless real source ingestion is added and each report records source provenance. <br>
Risk: Growth rankings and INVEST recommendations could be mistaken for funding, business, or research advice. <br>
Mitigation: Require human review against authoritative funding data before using outputs for decisions. <br>
Risk: The script writes reports to user-selected paths and installs Python dependencies. <br>
Mitigation: Run in an isolated Python environment and choose output paths inside the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/funding-trend-forecaster) <br>
- [AIPOCH-AI publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>
- [NIH RePORTER](https://reporter.nih.gov/) <br>
- [NSF Award Search](https://www.nsf.gov/awardsearch/) <br>
- [Horizon Europe Funding and Tenders](https://ec.europa.eu/info/funding-tenders/opportunities/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, JSON, Text, Guidance] <br>
**Output Format:** [JSON or plain-text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files to a user-selected output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
