## Description:

A free local contract consistency checker that identifies recomputable inconsistencies in party names, dates, amounts, placeholders, clause references, and defined terms with source evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local mechanical consistency pass over Chinese or English contract text before final review. It flags evidence-backed inconsistencies but does not provide legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a clean consistency result as legal clearance.

Mitigation: Use the output as a mechanical consistency checklist only, and send contracts that require legal judgment to qualified review.

Risk: The skill processes contract text through a local Node script.

Mitigation: Confirm the local execution environment and input-handling expectations before installing; server security evidence reports no hidden network, persistence, credential, or destructive behavior.

Risk: Most interface text and results are in Chinese, which can make review harder for non-Chinese readers.

Mitigation: Have a fluent reviewer check the findings, evidence, and advice before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/contract-consistency-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON findings; usage guidance may include shell commands and JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, category, line, message, advice, evidence, summary verdict, checks_given, and checks_withheld; insufficient input returns no conclusion.]

## Skill Version(s):

1.0.51 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
