## Description:

Chinese Patent Writer helps agents draft CNIPA-style Chinese patent application materials from source code or technical descriptions, including feature extraction, claim strategy, specifications, abstracts, and self-check appendices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolegao2024](https://clawhub.ai/user/gaolegao2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, inventors, and patent drafting teams use this skill to turn code or technical descriptions into Chinese patent application drafts aligned with CNIPA document structure. It supports invention patent and utility model drafting with claim layout analysis, specification sections, abstracts, code-scan reports, and self-check guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated patent text may be incomplete, inaccurate, or unsuitable for direct submission.

Mitigation: Treat outputs as draft materials and have a qualified patent professional review claims, specification support, prior-art statements, and filing readiness before submission.

Risk: The intended workflow may inspect private repositories or technical materials to identify patentable features.

Mitigation: Limit inputs to the minimum necessary files, avoid exposing secrets or unrelated confidential material, and confirm that unpublished invention details may be processed in the target environment.

Risk: Broad activation triggers around patent drafting and code scanning could cause accidental use in sensitive contexts.

Mitigation: Use narrow prompts and explicit scoping when invoking the skill, especially for proprietary code or confidential invention disclosures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaolegao2024/skills/chinese-patent)
- [Publisher profile](https://clawhub.ai/user/gaolegao2024)
- [CNIPA patent drafting guide](artifact/references/drafting-guide.md)
- [Claim strategy guide](artifact/references/claim-strategy.md)
- [Invention patent example](artifact/references/sample-invention.md)
- [Utility model example](artifact/references/sample-utility.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown patent draft with structured sections, claims, specification content, appendices, and self-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated patent content is draft-only and should be reviewed by a qualified patent professional before filing.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
