## Description:

Use this skill when a software architect, tech lead, or staff engineer needs to capture an in-flight architectural decision as a structured ADR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software architects, tech leads, and staff engineers use this skill to document architectural decisions before, during, or after implementation. It guides them through scope, drivers, alternatives, outcome, consequences, related decisions, and references to produce a MADR-style ADR suitable for docs/adr/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADRs may include confidential architecture, vendor, pricing, or security details.

Mitigation: Treat sensitive inputs as confidential, avoid external publication, and include sensitive details only when needed for the ADR.

Risk: An ADR can mislead maintainers if it records a bundled decision, vague drivers, or one-sided trade-offs.

Mitigation: Use the skill's staged review, require at least two considered options, connect outcomes to decision drivers, and include honest negative consequences before finalizing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/architecture-decision-record-drafter)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown ADR draft with filename guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured MADR-style Architecture Decision Record and proposes a docs/adr/ filename; the skill uses staged user review before finalizing the record.]

## Skill Version(s):

0.1.1 (source: release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
