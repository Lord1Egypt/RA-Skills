## Description:

Use this skill when a digital-forensic examiner, DFIR responder, or e-discovery custodian needs to draft a court-admissible chain-of-custody record aligned to NIST SP 800-86 and ISO/IEC 27037.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Digital-forensic examiners, DFIR responders, e-discovery custodians, investigators, internal-investigation leads, and counsel use this skill to collect case facts and draft a reviewable chain-of-custody package for digital evidence. The skill supports evidence-item registers, acquisition worksheets, transfer logs, examiner-action logs, working-copy registers, evidence-integrity checks, and open-question tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include sensitive evidence details, exhibit contents, or unnecessary PII while drafting custody records.

Mitigation: Use the skill only for authorized matters and limit inputs to the case facts needed to draft the record.

Risk: A draft chain-of-custody record could be mistaken for a certified or legally sufficient record.

Mitigation: Keep the draft label, leave signature blocks unsigned, and require examiner-of-record and counsel review before relying on the record.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/chain-of-custody-log-drafter)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft chain-of-custody package with structured tables and open-question lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs remain drafts for examiner and counsel review; missing evidence facts are marked unknown rather than invented.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
