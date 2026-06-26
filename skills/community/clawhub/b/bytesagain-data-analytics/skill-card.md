## Description: <br>
Analyze CSV files with statistical summaries, correlations, top-value rankings, trend charts, data quality reports, and pivot tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to quickly inspect CSV exports, check data quality, find correlations, rank column values, chart simple trends, and build small pivot summaries from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV summaries and top-value reports can expose sensitive values from the selected dataset in agent or terminal output. <br>
Mitigation: Use the skill only on datasets whose summaries can be shared in the current agent session, or remove sensitive columns before analysis. <br>
Risk: The skill runs a local bash/Python helper against files chosen by the user. <br>
Mitigation: Install and run it only in a trusted local workspace, and inspect or constrain the input files when working with confidential data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/bytesagain-data-analytics) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal reports with tabular summaries and ASCII charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-selected CSV files with bash and python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
