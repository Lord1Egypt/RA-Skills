## Description:

Drafts a five-section, source-linked review of a skill’s declarations, prerequisites, documented behavior, sample-run evidence, and license, while leaving the installation decision to a person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Skill users, maintainers, and reviewers use it to draft a source-linked pre-install review of one skill or compare skills on the same topic. A person makes the installation decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote parsing may expose confidential material or embedded credentials to an external service.

Mitigation: Use local-only review for confidential material; only approve external parsing for content intended to share, and remove embedded tokens or signed links.

Risk: The checker validates report structure, not whether the reviewed skill is safe, and external service behavior was not verified.

Mitigation: Review the cited source material and assess the reviewed skill independently; treat the generated report as a draft.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-skill-review-cn)
- [Publisher profile](https://clawhub.ai/user/huhoo)
- [Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown report, Source index]

**Output Format:** [Five-section Markdown report with source entries using file-and-line locations or URLs and retrieval dates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft review only; does not execute the reviewed skill code, and the installation decision remains with a person.]

## Skill Version(s):

0.1.4 (source: SKILL.md frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
