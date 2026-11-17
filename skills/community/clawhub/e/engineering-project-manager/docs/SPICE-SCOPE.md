# SPICE-like scope and limitations

This is an independent engineering workflow assistant. It is **not SPICE or
Automotive SPICE certified**, an official assessment model, or a certification
service. No affiliation, endorsement or approval by VDA QMC, iNTACS or ISO is
claimed. Automotive SPICE is a registered trademark of the VDA.

## Reference basis

Reviewed on 2026-09-16:

- [ISO/IEC 33001:2015](https://www.iso.org/standard/54175.html) introduces the
  concepts and terminology of the ISO/IEC 330xx process-assessment family.
- [Automotive SPICE 4.0 PRM/PAM, VDA QMC](https://vda-qmc.de/wp-content/uploads/2023/12/Automotive-SPICE-PAM-v40.pdf)
  describes process assessment. It is not itself a project lifecycle blueprint.
- [iNTACS certification information](https://www.intacs.info/certification-center)
  concerns qualified people and assessment arrangements; running this software
  does not provide that qualification.

These references are external resources, not included in this distribution.
Obtain authoritative editions from their publishers. Do not bundle standards,
publisher logos, assessment certificates or proprietary checklists here.

## Our implementation choices

The following are this project's own engineering controls and design choices.
They are not a reproduction of the official practices or a conformance matrix.

| Working area | Skill support | Limit of the automation |
|---|---|---|
| Planning and coordination | Tasks, dependencies, owners, bounded delegation and status | Schedules and staffing need human judgment |
| Engineering | Revisioned requirements, allocation and cross-domain traceability | Semantic completeness and feasibility need review |
| Configuration | Changes, immutable baseline snapshots and Git identity | Storage access and recovery remain operational responsibilities |
| Verification | Prescribed strategy, execution results and artifact hashes | Recorded evidence must come from genuine verification |
| Quality and delivery | Dedicated audits and internal gates G0–G3 | A pass only covers implemented checks and supplied evidence |
| Tailoring | Selected domains, exclusions, rationale and project constraints | The project decides which obligations apply |
| Risks and problems | Explicit ownership, risk review, mitigation, dispositions and verified closure | Actor labels are not authenticated authority; evidence needs engineering review |
| External obligations | Versioned sources, reviewed inventory and exact revision/evidence coverage | Completeness, applicability and actual conformity are not certified |

SYS, SWE, HWE and MLE are engineering areas reflected in the referenced base
model. CYBER and MECH are optional skill overlays; their local identifiers do
not claim to reproduce any official extension. The six discipline choices
remain available across project types, including non-automotive projects.

The capability roadmap records gaps. Do not infer a capability level from
files, test counts, coverage percentages, a green dashboard or the internal
release gate. No automated score is an assessment result.

## Responsibility and use

Use the skill as assistance to accountable engineers and project owners.
Review generated plans, code and evidence before relying on them. The user
remains responsible for appropriate validation, applicable obligations,
authorized infrastructure access and release decisions.

The software is supplied subject to its license, including its warranty and
liability provisions. This notice does not promise immunity from legal
responsibility and does not override mandatory law or separate agreements.
Safety-critical, regulated or contractual assurance requires the appropriate
independent expertise and evidence beyond these tools.
