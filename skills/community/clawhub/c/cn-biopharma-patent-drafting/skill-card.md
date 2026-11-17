## Description:

Assists with CNIPA-focused biopharma patent novelty assessment, claim strategy, technical disclosure preparation, and patent application draft generation from invention disclosures, structures, or sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent professionals, inventors, and legal or technical teams use this skill to prepare review-ready Chinese biopharma patent drafting materials for qualified patent attorney or patent agent review. It supports novelty assessment, claim drafting, CNIPA specification drafting, abstracts, sequence-listing checks, and source-mapped delivery notes.

### Deployment Geography for Use:

Global, for CNIPA-focused Chinese patent drafting workflows.

## Known Risks and Mitigations:

Risk: Unpublished invention disclosures may be transmitted to external OCR, patent intelligence, novelty-search, or drafting services.

Mitigation: Require explicit confirmation before any external transmission, redact sensitive excerpts when possible, and use local/manual OCR or local review paths for confidential material.

Risk: API credentials or confidential disclosures may be exposed through command-line arguments or generated reports.

Mitigation: Use environment variables or local credential configuration, avoid putting full disclosures or secrets in shell arguments, and review outputs before sharing.

Risk: Generated patent materials may contain unsupported claims, legal strategy errors, or incomplete disclosure.

Mitigation: Treat outputs as drafts and require review by a qualified Chinese patent attorney or patent agent before CNIPA filing.

## Reference(s):

- [Source Map - CNIPA Patent Drafting](references/source-map.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/cn-biopharma-patent-drafting)
- [PatSnap/Zhihuiya Connect service](https://connect.zhihuiya.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts and guidance with inline shell commands, plus optional generated document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a novelty assessment memo, claim set draft, CNIPA specification draft, abstract, drawing notes, sequence-listing notes, source appendix, and pre-filing risk notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
