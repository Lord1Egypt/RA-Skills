## Description: <br>
Extracts the investment strategy and operations analysis section from public fund periodic reports and consolidates the results into chronological plain-text summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suncxw-creator](https://clawhub.ai/user/suncxw-creator) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts and agents use this skill to fetch public fund report PDFs, extract the report-period investment strategy narrative, and create a consolidated text summary for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extractor writes report files and summaries to the local working directory. <br>
Mitigation: Run it from a dedicated folder where new report and summary files are acceptable. <br>
Risk: Fund names or codes containing path separators could affect generated paths or filenames. <br>
Mitigation: Provide normal fund codes and fund names without path separators. <br>
Risk: Public PDF downloads and PDF text extraction can fail or produce incomplete report sections. <br>
Mitigation: Review the downloaded source reports and consolidated summary before relying on the extracted text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/suncxw-creator/fund-report-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Plain text report extracts and a consolidated .txt summary, with Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a fund code and fund name; writes downloaded report extracts and a summary file in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
