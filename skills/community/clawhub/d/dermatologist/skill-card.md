## Description: <br>
Track skin lesions, rashes, photos, treatment response, and dermatology visit prep with conservative triage, case-based records, and privacy guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to organize skin concern timelines, compare photos conservatively, track treatments and triggers, and prepare concise handoffs for dermatology or primary-care visits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive dermatology notes and photo metadata may be stored locally under ~/dermatologist/. <br>
Mitigation: Use the skill only when local storage is acceptable, require user approval before writing files, keep storage paths explicit, and support deletion or export on request. <br>
Risk: Skill files conflict on whether minor or intimate-area photos may ever be tracked. <br>
Mitigation: Avoid minor and intimate-area photo workflows unless the publisher clarifies the policy; redirect those cases to in-person care or secure clinician systems. <br>
Risk: Dermatology guidance can be mistaken for diagnosis, prescribing, or replacement of clinician review. <br>
Mitigation: Keep outputs framed as organization, conservative triage, and visit preparation; escalate red flags to urgent or emergency care and defer diagnosis and treatment decisions to clinicians. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/dermatologist) <br>
- [Skill Homepage](https://clawic.com/skills/dermatologist) <br>
- [Dermatology Triage](artifact/triage.md) <br>
- [Legal and Privacy Boundaries](artifact/legal-boundaries.md) <br>
- [Photo Protocol](artifact/photo-protocol.md) <br>
- [Consult Workflow](artifact/consult-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured checklists, tables, local file templates, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local records under ~/dermatologist/ only with user approval; does not upload photos or health data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
