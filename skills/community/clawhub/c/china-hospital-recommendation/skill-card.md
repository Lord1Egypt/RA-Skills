## Description: <br>
Generates patient-facing English hospital recommendation reports for medical travel to China, using intake data to produce a three-hospital shortlist with specialist-direction guidance, cost and logistics advice, evidence notes, and Markdown/PDF exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helenalhq](https://clawhub.ai/user/helenalhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to turn paid patient intake details into an English hospital matching report for China medical travel. The report helps compare recommended hospitals, specialist directions, expected costs, travel logistics, next steps, and evidence limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient and medical-travel details may be sensitive, and generated Markdown/PDF reports can persist that information locally. <br>
Mitigation: Use the skill only in environments approved for this data, store outputs in a secure directory, and remove or protect generated files after delivery. <br>
Risk: Dynamic facts such as hospital access paths, JCI status, specialist profiles, visa details, transportation, and accommodation can change. <br>
Mitigation: Verify dynamic facts with current authoritative sources and mark uncertain items as needing manual confirmation instead of presenting them as settled. <br>
Risk: Hospital recommendations could overstate clinical certainty, exact pricing, teleconsult availability, or named-doctor suitability. <br>
Mitigation: Keep recommendations evidence-aware, use scenario-based cost framing, separate administrative intake from doctor-led consultation, and avoid named doctors unless strong public evidence supports them. <br>


## Reference(s): <br>
- [Product Brief](references/product-brief.md) <br>
- [Report Schema](references/report-schema.md) <br>
- [Specialty Mapping](references/specialty-mapping.md) <br>
- [Fudan Rankings 2025 Snapshot](references/fudan-rankings-2025.md) <br>
- [Recommendation Method](references/recommendation-method.md) <br>
- [Search Policy](references/search-policy.md) <br>
- [PDF Spec](references/pdf-spec.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [ChinaMed Select](https://www.chinamed.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Patient-facing English Markdown report with optional PDF export generated from structured JSON input.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 3 recommended hospitals, includes evidence notes and disclaimer text, and keeps Markdown as the editable intermediate artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
