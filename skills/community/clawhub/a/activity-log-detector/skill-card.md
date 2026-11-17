## Description:

Analyze Azure Activity Logs and Sentinel incidents for suspicious patterns and attack indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security teams and Azure administrators use this skill to analyze exported Azure Activity Logs and Microsoft Sentinel incidents, identify suspicious operations, map events to MITRE ATT&CK Cloud techniques, and produce containment and detection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported Azure Activity Logs or Sentinel incident details may contain sensitive operational or security data.

Mitigation: Use only when comfortable sharing those exports in the agent session, and review inputs to remove credentials, access keys, or secrets before analysis.

Risk: Generated containment commands could affect production access or resources if run without review.

Mitigation: Review and approve generated Azure CLI commands with authorized Azure administrators before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with findings tables, incident timelines, Azure CLI command suggestions, and Sentinel KQL query snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided exported Azure logs or incident details; does not directly access Azure accounts.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
