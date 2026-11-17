## Description:

AI Company CQO provides an AI-native chief quality officer role for end-to-end quality inspection workflows, PDCA-BROKE governance loops, G0-G4 quality gates, multi-agent review, and quality improvement planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and quality teams use this skill to structure AI-agent quality governance, inspect deliverables against quality gates, produce defect and risk reports, and define follow-up improvement plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled quality checker writes reports into the directory being checked.

Mitigation: Run it only with low privileges on trusted directories, especially in CI or when evaluating third-party skill packages.

Risk: The skill has a broad agent-coordination and quality-governance scope that requires review before installation.

Mitigation: Review the skill before deployment, narrow activation triggers, and confirm its workflows match the intended quality process.

Risk: The security result from the bundled checker is not authoritative by itself.

Mitigation: Use stronger scanning and human review before relying on the skill for security or release decisions.

Risk: Some artifact instructions ask agents to expose reasoning traces.

Mitigation: Avoid instructions that request chain-of-thought disclosure and require concise, reviewable rationales instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/ai-company-cqo-2-0-0)
- [Declared skill homepage](https://clawhub.com/skills/ai-company-cqo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured reports, JSON examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quality assessments, defect reports, governance workflows, audit-oriented records, and improvement plans.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter states 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
