## Description:

Produces an auditable first draft of an A-share or Hong Kong listed-company earnings review, with traceable figures and human-filled rating fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

For investment researchers and analysts preparing an auditable first draft of an earnings review from public disclosures and user-supplied material. The draft supports source tracing and human review; ratings and target prices remain for a person to fill in.

### Deployment Geography for Use:

Global; focused on Chinese A-share and Hong Kong listed-company reporting.

## Known Risks and Mitigations:

Risk: Security evidence rates the skill suspicious because it reports credentialed requests to catalog-selected services and a redirect risk that do not match the stated report-drafting purpose.

Mitigation: Avoid installation until the credential destination and redirect behavior are addressed and service-discovery capabilities are clearly disclosed or removed.

Risk: The security scan was partial, with one component partially inspected and a tool-misuse analyzer degraded.

Mitigation: Treat the security evidence as incomplete and resolve the remaining review gaps before installation.

Risk: The security guidance says installation versions are not pinned.

Mitigation: Pin the installation version.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-cn-earnings-note)
- [Publisher profile](https://clawhub.ai/user/huhoo)
- [Skill instructions](artifact/SKILL.md)
- [Data channels](artifact/references/data-channels.md)
- [Report skeleton](artifact/references/report-skeleton.md)
- [Coverage ledger](artifact/references/coverage-ledger.md)
- [Evidence format](artifact/references/evidence-format.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, JSONL, Guidance]

**Output Format:** [Markdown earnings-review draft with a JSON coverage ledger, JSONL source index, and run log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures carry evidence-level tags; ratings and target prices remain pending human review.]

## Skill Version(s):

0.3.47 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
