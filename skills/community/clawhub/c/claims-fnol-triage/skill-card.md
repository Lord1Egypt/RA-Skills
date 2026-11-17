## Description:

Converts raw First Notice of Loss reports into PII-safe draft triage records with coverage-verification prompts, severity tiering, fraud red-flag scoring, next-action playbooks, and insured acknowledgements for licensed-adjuster review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Claims intake teams, inside adjusters, MGAs, carriers, and SIU pre-screeners use this skill to turn raw FNOL reports into structured draft triage material for licensed-adjuster review. It supports auto, property, general liability, and workers' compensation intake workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on claims intake information that can include PII or PHI.

Mitigation: Use masked claim information only and stop to request masked replacements when unmasked sensitive identifiers appear.

Risk: Draft triage output could be mistaken for a final insurance determination.

Mitigation: Keep outputs as drafts for licensed-adjuster review and avoid coverage, fault, payment, reserve, settlement, medical, or legal determinations.

Risk: Claimant narratives may contain unverified or misleading facts.

Mitigation: Tag each fact as Confirmed, Reported, or Unknown and map fraud flags only to user-supplied facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/claims-fnol-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown triage record with tables, checklists, coverage-verification questions, fraud scorecard, and insured acknowledgement draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft output for licensed-adjuster review; no final coverage, fault, reserve, settlement, medical, or legal determination.]

## Skill Version(s):

0.1.2 (source: evidence.json release.version and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
