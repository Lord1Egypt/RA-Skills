## Description:

A disease-to-innovative-drug analysis skill for biomedical question answering that turns disease-level questions into evidence-backed reports covering targets, drugs, clinical progress, and mechanism trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inbreak](https://clawhub.ai/user/inbreak)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to investigate innovative drugs for a specified disease by normalizing the disease, querying biomedical data sources, ranking evidence, and producing a structured disease-drug intelligence report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local runner can execute Python files by filename and may be misused outside the declared tool set.

Mitigation: Install in an isolated environment, invoke only manifest-listed commands, and do not pass arbitrary filenames to local_tools/run_tool.sh.

Risk: Disease and drug queries may be sent to external services, including ChEMBL, ClinicalTrials.gov, and Tavily.

Mitigation: Avoid submitting sensitive patient or proprietary research data, and set TAVILY_API_KEY only when the search fallback is needed.

Risk: Biomedical intelligence reports can be incomplete or outdated when source databases lack current or consistent evidence.

Mitigation: Review report conclusions against traceable database identifiers and public sources before using them for research, clinical, or commercial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inbreak/skills/disease-drug-intelligence)
- [ClawBio homepage](https://github.com/ClawBio/ClawBio)
- [Disease-to-Innovative-Drug Playbook](references/disease_to_drug_playbook.md)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown report with evidence notes and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports follow the bundled disease-drug template unless the user requests a shorter or alternate format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
