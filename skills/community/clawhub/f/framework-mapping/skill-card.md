## Description:

Map document sections to compliance framework controls with confidence scoring. Produces bidirectional mappings for gap analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

Apache-2.0

## Use Case:

Compliance analysts, auditors, and developers use this skill to map policy or procedure document sections to controls in frameworks such as NIST 800-53, HITRUST, HIPAA, ISO 27001, and SOC 2. The resulting bidirectional mapping supports coverage review and gap analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance documents can contain confidential or regulated information.

Mitigation: Use the skill only in agent environments approved for the documents being analyzed, and avoid providing sensitive documents unless that access is appropriate.

Risk: Generated control mappings and gap findings may be incomplete or inaccurate.

Mitigation: Have a qualified compliance reviewer verify mappings, relevance scores, and gap conclusions before relying on them for audit or remediation decisions.

Risk: Web fetching for framework context may retrieve external material during analysis.

Mitigation: Review network access policy and framework-source requirements before using the skill in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/framework-mapping)
- [Publisher profile](https://clawhub.ai/user/dangsllc)
- [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills)
- [Dang's Solutions](https://dangssolutions.com)
- [Rote Compliance](https://rotecompliance.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown with JSON structures for per-section mappings and per-control coverage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes relevance scores, coverage types, rationales, coverage status, unaddressed aspects, and aggregate confidence values.]

## Skill Version(s):

0.1.3 (source: server release metadata); artifact frontmatter version 1.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
