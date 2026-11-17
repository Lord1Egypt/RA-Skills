## Description:

Write contracts from scratch with guided intake, multi-party negotiation, risk analysis, and version control for lawyers, freelancers, and individuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Lawyers, freelancers, and individuals use this skill to draft new contracts through guided intake, structured clause generation, risk review, negotiation tracking, and version-controlled finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drafts contract language but does not provide legal advice or jurisdiction-specific validity determinations.

Mitigation: Include the required AI-generated legal disclaimer in every draft and have a qualified attorney review important or jurisdiction-sensitive contracts before signing.

Risk: Contract drafts, party details, negotiation notes, and finalized records may contain sensitive personal or business information.

Mitigation: Store and share the ~/contracts workspace according to the user's confidentiality, access-control, and retention requirements.

Risk: Incomplete intake can produce missing, ambiguous, or mismatched contract terms.

Mitigation: Treat discovery as blocking, ask for missing parties, jurisdiction, relationship, and contract details, and run the documented coherence and ambiguity review before finalization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/contract)
- [Source: SKILL.md](artifact/SKILL.md)
- [Contract writing phases](artifact/phases.md)
- [Discovery questions by contract type](artifact/intake.md)
- [Clause patterns library](artifact/clauses.md)
- [Risk analysis and disclaimers](artifact/risks.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown contract drafts, intake notes, party records, negotiation notes, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files under ~/contracts for drafts, versions, intake, party details, notes, and finalized records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
