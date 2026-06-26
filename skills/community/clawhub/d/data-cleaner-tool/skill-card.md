## Description: <br>
Data Cleaner Skill helps agents clean local CSV and Excel data by removing duplicates, filling missing values, standardizing phone and date formats, and reporting cleanup results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, finance, administrative, and sales users can use this skill through an agent to prepare local CSV or Excel files for reporting, customer-list maintenance, and routine data cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleaning operations may materially change records through de-duplication, missing-value filling, and phone or date standardization. <br>
Mitigation: Run the skill on a copy or sample first, then inspect the cleaned file and reported row-count changes before using results for business decisions. <br>
Risk: The documentation includes a batch_clean.py command that is not included in the package. <br>
Mitigation: Use the included scripts/clean_data.py command for supported cleanup, or verify and add a batch script before relying on documented batch processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shenghoo123-png/data-cleaner-tool) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Description](artifact/SKILL.md) <br>
- [Cleaning Script](artifact/scripts/clean_data.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell command examples, terminal status output, and local CSV or Excel cleaned files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on CSV or Excel inputs, writes a cleaned file, and prints row-count and cleanup statistics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
