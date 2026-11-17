## Description:

Critigraph VM helps agents frame adversarial reasoning tasks as mathematical game-tree searches that explore counterarguments, rank paths, and report estimated win probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lybang972314](https://clawhub.ai/user/lybang972314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill for adversarial analysis workflows where a proposed path needs to be tested against opposing moves and ranked alternatives. It is suited to reasoning assistance in domains such as legal evidence review, quantitative signals, code review, and security audit planning when the user wants structured critique rather than a single answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is documentation-only and points to an external project, so claimed engine, training, benchmark, or production behavior is not independently demonstrated by the packaged files.

Mitigation: Review the linked project and any operational code separately before relying on those claims in production workflows.

Risk: The skill describes adversarial reasoning outputs such as counterargument paths and win probabilities that may be mistaken for validated domain conclusions.

Mitigation: Treat outputs as decision-support guidance and require domain expert review before acting on legal, financial, code review, or security audit recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lybang972314/skills/critigraph-vm)
- [Server-resolved GitHub provenance](https://github.com/lybang972314/critigraph-vm)
- [Publisher profile](https://clawhub.ai/user/lybang972314)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with explanatory text and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe ranked paths, expected win probabilities, and search-tree structure; the artifact itself is documentation-only.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
