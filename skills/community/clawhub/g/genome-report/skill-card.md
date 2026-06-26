## Description: <br>
Analyze 23andMe raw genome data to generate health, trait, ancestry, pharmacogenomic, athletic, and family comparison reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nomadrex](https://clawhub.ai/user/nomadrex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run local analysis of 23andMe v5 raw data, generate individual reports, and compare multiple family genome files for educational or informational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes and can save sensitive genetic, health, trait, and family comparison information. <br>
Mitigation: Use only with informed consent, store inputs and generated HTML or JSON reports in private non-synced locations, and delete or protect outputs after use. <br>
Risk: Genome report results may be mistaken for medical guidance. <br>
Mitigation: Treat results as educational information only and consult a healthcare professional before making health decisions. <br>
Risk: Family comparison can expose information about relatives who did not agree to participate. <br>
Mitigation: Run family comparison only when every included person has explicitly agreed to that use. <br>


## Reference(s): <br>
- [SNP database](references/snp_database.json) <br>
- [ClawHub skill listing](https://clawhub.ai/nomadrex/genome-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Console text, structured JSON, or HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include per-SNP details, category risk scores, disclaimers, and family comparison summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
