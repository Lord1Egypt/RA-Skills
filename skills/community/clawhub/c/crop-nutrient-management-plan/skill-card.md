## Description: <br>
Drafts field-by-field crop Nutrient Management Plans aligned to NRCS CPS 590 and the 4R framework for qualified planner review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CCA, NRCS TSP, state-approved nutrient-management planners, and supporting agronomy consultants use this skill to draft a field-by-field Nutrient Management Plan, including intake, nutrient budgets, P-risk checks, 4R application decisions, recordkeeping, contingencies, and unresolved items for review. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Draft nutrient budgets, P-index conclusions, setbacks, or application restrictions may be wrong if LGU recommendations, state 590 supplements, or state nutrient-management rules are missing or outdated. <br>
Mitigation: Treat outputs as drafts and require a qualified CCA, NRCS TSP, or state-approved planner to verify all recommendations, rules, setbacks, and restrictions before use. <br>
Risk: The plan could be mistaken for a signed compliance document for CSP, EQIP, CAFO, or state nutrient-management submission. <br>
Mitigation: Keep outputs labeled as draft planning material and require planner review, refinement, and signature before any compliance use. <br>
Risk: Farm identifiers, permit details, parcel numbers, GPS coordinates, or producer names could expose sensitive operational information. <br>
Mitigation: Use operation and field codenames during intake and redact real farm, producer, parcel, permit, coordinate, and address details. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/archlab-space/crop-nutrient-management-plan) <br>
- [Skill README](artifact/README.md) <br>
- [Skill source instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured headings, tables, draft labels, unresolved-item flags, and cited-basis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft planning content only; qualified planner review and sign-off remain required.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
