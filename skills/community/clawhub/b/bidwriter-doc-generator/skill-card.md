## Description:

Generates a Chinese-language offline bid-document skeleton from project details, bidder materials, and tender clauses, with volume outlines, clause-response conclusions, disqualification checks, material guidance, and completeness suggestions for goods, works, services, and government procurement bids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement teams use this skill to turn tender clauses, bidder qualifications, project metadata, and material lists into a structured bid-file outline and review checklist. It is intended as a drafting and self-check aid, not as legal advice or a final procurement compliance determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake mechanically matched clause responses for legal advice or a final procurement compliance decision.

Mitigation: Treat the output as a draft checklist and verify every conclusion against the tender document, evaluation rules, and qualified procurement or legal review.

Risk: Bidder, pricing, and project data can be sensitive even when processed locally.

Mitigation: Run the skill only in trusted local environments and provide only project data the user is comfortable processing in the skill runtime.

Risk: The free release limits detailed clause evidence and several downstream checklists.

Mitigation: Do not rely on the free output as the sole final-submission review; manually inspect all tender clauses and required materials before submission.

## Reference(s):

- [投标文件分册结构与撰写口径](references/bid-doc-structure.md)
- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bidwriter-doc-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese-language console text or JSON generated from local project input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free release shows the full volume outline and the first five clause-response conclusions; detailed bases, full clause coverage, material checklists, disqualification lists, and completeness scoring are limited.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
