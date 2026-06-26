## Description: <br>
Monitor competitor clinical trial progress and alert on market risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharma, competitive intelligence, and clinical development users use this skill to maintain a local watchlist of competitor clinical trials, scan ClinicalTrials.gov for updates, and generate risk reports for events such as completion, result publication, or approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script saves monitored trial IDs, company and drug labels, snapshots, and alert history in the user's home directory. <br>
Mitigation: Review the local ~/.openclaw/competitor-trial-monitor data before use and avoid adding confidential or restricted trial intelligence unless local storage is acceptable. <br>
Risk: Scan and add operations send NCT IDs to ClinicalTrials.gov. <br>
Mitigation: Use only NCT IDs that can be shared with the external registry service and run scans from an approved network environment. <br>
Risk: The artifact lists an extra pip install command even though the prerequisites section says no additional Python packages are required. <br>
Mitigation: Review the dependency command before installation and install only packages required for the chosen execution path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/competitor-trial-monitor) <br>
- [ClinicalTrials.gov API v2 studies endpoint](https://clinicaltrials.gov/api/v2/studies) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script stores watchlist, snapshot, alert, and configuration files under ~/.openclaw/competitor-trial-monitor.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
