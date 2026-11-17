## Description:

Build Docs Creator produces a standardized developer handoff package from accumulated project design work, including a BRD-style product overview, SRS-style requirements, technical design, interface source, and traceability documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn project conversation history, artifacts, interface source, and partial imported documentation into a complete pre-build handoff package. It is intended for full build-documentation packages rather than single narrow document requests or ongoing SDLC artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated package may consolidate sensitive project conversation history, artifacts, interface source, and imported requirements into a shareable zip.

Mitigation: Install and run only in projects where that source access is acceptable, then review and redact the generated package before sharing it outside the intended handoff audience.

Risk: Imported requirements may be stale or conflict with later project design and interface artifacts, which can mislead a development handoff if left unresolved.

Mitigation: Review the generated Open Questions, source manifest, and traceability matrix so unresolved gaps and imported-versus-built discrepancies are visible before development starts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/skills/build-docs-creator)
- [Product Overview Reference](references/product-overview.md)
- [Requirements Reference](references/requirements.md)
- [Design Reference](references/design.md)
- [Interfaces Reference](references/interfaces.md)
- [Traceability Matrix Reference](references/traceability.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Zipped documentation package containing Markdown documents and interface source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The package follows a fixed build-docs structure and emphasizes explicit open questions, source manifests, and traceability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
