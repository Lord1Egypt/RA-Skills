## Description: <br>
Generates structured disease-to-innovative-drug intelligence reports that combine disease normalization, target and mechanism analysis, representative drugs, clinical progress, and evidence limitations using local adapters for ChEMBL, ClinicalTrials.gov, and controlled search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inbreak](https://clawhub.ai/user/inbreak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Biomedical analysts, developers, and research teams use this skill to turn disease-focused drug landscape questions into reproducible, evidence-backed reports covering innovative mechanisms, representative drugs, clinical trials, trends, and limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to third-party public data providers when the Tavily-backed fallback is enabled. <br>
Mitigation: Avoid personal medical details in prompts and use a dedicated Tavily API key for this skill. <br>
Risk: Unpinned Python dependencies can reduce reproducibility across installs. <br>
Mitigation: Pin dependency versions before regulated, audited, or reproducibility-sensitive deployments. <br>
Risk: Biomedical reports may be incomplete or misleading if treated as clinical advice. <br>
Mitigation: Use the generated report as research support only and review conclusions against authoritative biomedical and regulatory sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/inbreak/disease-drug-intelligence) <br>
- [ClawBio Homepage](https://github.com/ClawBio/ClawBio) <br>
- [Disease-to-Innovative-Drug Playbook](references/disease_to_drug_playbook.md) <br>
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) <br>
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown report with evidence notes and optional command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ChEMBL and ClinicalTrials.gov adapters first; Tavily-backed search is a configured fallback for recent public updates when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
