## Description:

Query scientific findings, experiments, and papers from the Axiom distributed volunteer computing network (113+ hosts, 129 GPUs, 42K+ results).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyhelix](https://clawhub.ai/user/pyhelix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical users use this skill to query Axiom's public science APIs for distributed-computing statistics, scientific findings, active experiments, papers, and plain-text experiment suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the documented examples contacts axiom.heliex.net.

Mitigation: Review outbound requests before running examples and use the APIs only in environments where contacting the public Axiom service is acceptable.

Risk: Submitting an experiment suggestion sends the submitted text to the Axiom team for review.

Mitigation: Do not include secrets, private research plans, personal data, or proprietary information in submitted ideas.

## Reference(s):

- [Axiom Homepage](https://axiom.heliex.net)
- [Axiom Scientific Findings](https://axiom.heliex.net/scientific_findings.php)
- [Reactivity Localization Paper](https://axiom.heliex.net/reactivity_localization_paper.pdf)
- [Axiom Project Statistics API](https://axiom.heliex.net/api/stats.php)
- [Axiom Findings API](https://axiom.heliex.net/api/findings.php)
- [Axiom Experiments API](https://axiom.heliex.net/api/experiments.php)
- [Axiom Papers API](https://axiom.heliex.net/api/papers.php)
- [ClawHub Skill Page](https://clawhub.ai/pyhelix/skills/axiom-distributed-science)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented API examples.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
