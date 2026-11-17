## Description:

Use this skill when a surgical pathologist, pathology fellow, pathology assistant, or LIS report-builder needs to draft a CAP Cancer Protocol-conformant synoptic report covering protocol selection, Required Data Elements, AJCC 8th pTNM staging, biomarker fields, and attending review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Surgical pathology and LIS users use this skill to draft CAP Cancer Protocol-conformant synoptic cancer report packets from specimen, gross, microscopic, and ancillary-study inputs. The output is a draft for attending pathologist review and electronic sign-out in the laboratory information system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A draft report could be mistaken for a signed diagnosis, staging decision, biomarker release, or patient-facing communication.

Mitigation: Use the skill only as a drafting aid for qualified pathology or LIS personnel, and require attending pathologist review and LIS sign-out before clinical use.

Risk: Using the wrong CAP protocol version or leaving Required Data Elements unresolved could produce a nonconformant synoptic report.

Mitigation: Confirm the applicable CAP protocol version from the LIS or CAP source before drafting, keep Required Data Elements in protocol order, and resolve OPEN, PENDING, or DISCORDANT items before release.

Risk: Protected health information could be included in the working draft if users paste patient identifiers.

Mitigation: Use accession number only in the working draft and exclude patient name, MRN, date of birth, and other PHI until final sign-out inside the LIS.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/cap-cancer-synoptic-report-drafter)
- [Skill README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft synoptic pathology packet with structured report sections and open-question markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft output is labeled for attending pathologist review and LIS sign-out; unresolved fields may be marked OPEN, PENDING, or DISCORDANT.]

## Skill Version(s):

0.1.1 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
