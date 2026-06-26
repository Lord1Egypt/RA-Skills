## Description: <br>
A Chinese-language travel helper that guides users through arrival card and visa-application forms for Malaysia, Thailand, Singapore, Indonesia, Vietnam, the Philippines, Japan, and South Korea, including materials checklists, field guidance, exception handling, and automation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivy-ting](https://clawhub.ai/user/ivy-ting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to prepare required materials, understand official arrival-card workflows, and draft accurate form-filling guidance for supported Asian destinations. It can also provide optional document-recognition guidance and automation pseudocode that must be reviewed before use on official portals. <br>

### Deployment Geography for Use: <br>
Global, for travelers preparing entry forms for supported Asian destinations. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle passport-level data, travel documents, and booking details. <br>
Mitigation: Collect only the fields needed for the destination form, redact unnecessary details, avoid uploading passport or booking images unless necessary, and do not share portal passwords or mailbox access. <br>
Risk: Automation suggestions for official entry forms could submit incorrect or outdated information. <br>
Mitigation: Treat automation as a draft workflow only and require manual review before any form is submitted or any confirmation is saved. <br>
Risk: Arrival-card requirements and portal behavior can change by country. <br>
Mitigation: Use official government sites directly when possible and verify current requirements before relying on generated guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivy-ting/asia-arrival-card) <br>
- [Materials checklist](reference/materials-checklist.md) <br>
- [Country guides](reference/country-guides-new.md) <br>
- [Country comparison](reference/country-comparison.md) <br>
- [Smart document recognition](reference/smart-document-recognition.md) <br>
- [Automation framework](reference/automation-framework.md) <br>
- [FAQ](reference/faq.md) <br>
- [Malaysia Digital Arrival Card](https://imigresen-online.imi.gov.my/mdac/main) <br>
- [Thailand TDAC/TM6 portal](https://extranet.immigration.go.th/fn/TM6/) <br>
- [Singapore SG Arrival Card](https://eservices.ica.gov.sg/sgarrivalcard/) <br>
- [All Indonesia arrival portal](https://allindonesia.imigrasi.go.id/) <br>
- [Vietnam public service portal](https://dichvucong.bocongan.gov.vn/) <br>
- [Philippines eTravel](https://etravel.gov.ph/) <br>
- [Visit Japan Web](https://www.vjw.digital.go.jp/) <br>
- [Korea K-ETA](https://www.k-eta.go.kr/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with tables, checklists, structured field instructions, official portal links, and optional code or pseudocode blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted document fields for user confirmation, country-specific timing constraints, and manual-review checkpoints.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
