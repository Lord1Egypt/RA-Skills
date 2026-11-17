## Description:

Audits product UX for briefs, specs, implementation plans, or built apps using the Formula 100K rubric and browser walkthroughs, then produces evidence-backed scores, findings, and approved fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product builders, and app owners use this skill to audit a UX brief, PRD, implementation plan, repository, or deployed app. It evaluates the experience against a ten-dimension rubric, records evidence, produces a scored report, and applies document or code fixes only after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit workflow can create or use bypass-style access paths, including local preview routes or injected localStorage state for gated flows.

Mitigation: Require explicit user approval before route creation or localStorage injection, prefer existing local-only preview fixtures, mark synthetic state in notes, and clean it up after testing.

Risk: Running the skill on untrusted repositories could execute or rely on project code during local UX review.

Mitigation: Use the skill only on repositories trusted to run locally, review before installing, and prefer test accounts over personal credentials.

Risk: Approved UX fixes may edit source files or affect deployment-sensitive flows.

Mitigation: Apply source edits only after the checkpoint approval, and require separate explicit approval before any push or deploy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/auditor-ux-app-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [UX product rubric](references/rubrica.md)
- [Browser walkthrough protocol](references/recorrido-navegador.md)
- [Report templates](references/plantillas-informe.md)
- [Production failure patterns](references/cicatrices-produccion.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and plans, with optional code, shell commands, configuration edits, and written guidance when fixes are approved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-backed findings with unverified items separated; source or document edits require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
