## Description:

Douban helps agents write film and book reviews, interpret rating distributions, curate media lists, and guide users through Douban community norms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft nuanced Douban-style reviews, build book and film lists, reason about rating-distribution signals, and navigate Douban community and second-hand trading norms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rating-distribution heuristics could be mistaken for authoritative proof of review manipulation.

Mitigation: Treat rating analysis as a qualitative signal, avoid definitive manipulation claims without corroborating evidence, and preserve uncertainty in user-facing conclusions.

Risk: Douban group second-hand trading advice could expose users to payment or in-person transaction risk.

Mitigation: Keep transaction guidance focused on caution, local group rules, in-person verification, and avoiding unsafe transfers.

Risk: Users may request brushing, review manipulation, account farming, or controlled-comment tactics.

Mitigation: Maintain the artifact's boundary against刷分, 控评, and养号 methods, and redirect to honest review and community participation guidance.

## Reference(s):

- [Douban ClawHub skill page](https://clawhub.ai/zhangifonly/skills/douban)
- [zhangifonly publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance for reviews, recommendations, rating analysis, and community-use advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential access, persistence, or hidden data flow identified by security evidence.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
