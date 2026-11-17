## Description:

AI consulting support for SMBs that structures McKinsey-style diagnostics, custom AI solution design, and ROI tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustosmg](https://clawhub.ai/user/bustosmg)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants and SMB operators use this skill to run structured AI opportunity discovery, produce technical proposals and implementation roadmaps, and monitor ROI for Spanish-speaking small and midsize businesses. The artifact is especially tailored to Argentine retail, healthcare, logistics, and service contexts.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: Broad command execution, file-writing, memory, and automation capabilities can affect client workspaces or operational systems.

Mitigation: Remove or tightly sandbox exec and write access, disable scheduled runs by default, and require explicit confirmation before external updates or deployments.

Risk: Consulting workflows can process transcripts, recordings, customer data, financial or tax integrations, and production migration data.

Mitigation: Segregate each client workspace and memory store, minimize retained sensitive data, and apply privacy controls before using transcripts, recordings, financial, tax, or migration records.

Risk: ROI estimates and implementation recommendations may influence client commercial decisions.

Mitigation: Have a qualified human reviewer validate assumptions, budgets, legal constraints, data readiness, and client expectations before presenting recommendations as actionable plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustosmg/skills/consultoria-ia)
- [README](artifact/README.md)
- [Executive summary](artifact/RESUMEN-EJECUTIVO.md)
- [McKinsey interview workflow](artifact/flujo-entrevistas-mckinsey.md)
- [AI solution development workflow](artifact/flujo-desarrollo-soluciones.md)
- [Hardware store example](artifact/EJEMPLO-FERRETERIA.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, YAML and JSON configuration snippets, checklists, ROI calculations, and code-oriented prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Spanish-language consulting artifacts such as diagnostic memos, opportunity matrices, technical proposals, implementation plans, dashboards, and follow-up reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
