## Description: <br>
BloodHound Narrator turns BloodHound attack path exports into offline dual-layer Markdown security reports with executive risk narratives and technical remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurostrike](https://clawhub.ai/user/kurostrike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pentesters, blue teams, SOC analysts, security consultants, and security leaders use this skill to translate BloodHound Active Directory attack paths into client-ready audit, health check, incident response, compliance, and remediation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BloodHound exports and generated reports can reveal sensitive Active Directory weaknesses. <br>
Mitigation: Protect the input export and generated Markdown report, and share them only through approved security channels. <br>
Risk: The skill runs local PowerShell and loads bundled helper scripts. <br>
Mitigation: Install and run it only from a trusted directory, do not override BH_NARRATOR_DIR, and use PowerShell from a trusted source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kurostrike/bloodhound-narrator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with executive summary, per-path findings, and technical remediation appendix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local BloodHound JSON export and can filter results by minimum severity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
