## Description:

Generate, review, and govern software documentation, including API docs, project templates, AI verification, drift detection, and doc-as-code CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create and review code and project documentation, including API references, design and operational templates, and AI-generated documentation. It also helps teams verify documentation, manage drift, and plan documentation governance and CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the example-running workflow for unclear isolation and notes that some referenced files were only partly inspected; the verdict is suspicious with medium confidence and does not establish malicious intent.

Mitigation: Consider postponing installation until safeguards are clear. Review the partially inspected references, and run examples in an isolated environment without credentials or network access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zengfr/skills/ai-docgen-expert)
- [Publisher profile](https://clawhub.ai/user/zengfr)
- [Server-resolved GitHub source](https://github.com/zengfr/kb-distiller/tree/main/output/ai-docgen-expert)
- [Diátaxis documentation framework](https://diataxis.fr)
- [TSDoc](https://tsdoc.org)
- [TypeDoc](https://typedoc.org)
- [JSDoc](https://jsdoc.app)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Conventional Commits 1.0.0](https://conventionalcommits.org/en/v1.0.0/)
- [ADR templates](https://adr.github.io/adr-templates/)
- [Google documentation best practices](https://google.github.io/styleguide/docguide/best_practices.html)
- [C4 model](https://c4model.com/)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OMG BPMN specification](https://www.omg.org/spec/BPMN/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with documentation templates, review checklists, and code or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is tailored to the repository, documentation type, and evidence supplied by the user.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
