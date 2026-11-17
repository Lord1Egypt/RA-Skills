## Description:

Review legal contracts, NDAs, employment agreements, SaaS terms, and M&A documents; identify unfavorable terms, suggest redlines, and compare clauses to market standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youeshopent-debug](https://clawhub.ai/user/youeshopent-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill for first-pass contract review, due diligence, and negotiation preparation. It helps surface document completeness issues, unfavorable terms, key obligations, red flags, and candidate redline language for qualified human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce incorrect or overconfident contract analysis or redline suggestions.

Mitigation: Treat results as first-pass review only and have material terms reviewed by qualified legal counsel before relying on them.

Risk: The optional legal-redline-tools workflow installs from a mutable GitHub source, which can execute code during installation.

Mitigation: Review or pin the external repository before use and run the workflow in a dedicated environment.

Risk: The skill defaults to a US-law focus and legal enforceability varies by jurisdiction.

Mitigation: Confirm jurisdiction-specific issues with qualified counsel and adjust analysis for the governing law and venue in the contract.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youeshopent-debug/skills/claude-legal-skill)
- [Publisher profile](https://clawhub.ai/user/youeshopent-debug)
- [CUAD Dataset](https://github.com/TheAtticusProject/cuad)
- [LegalBench](https://hazyresearch.stanford.edu/legalbench/)
- [ContractEval](https://arxiv.org/abs/2303.07389)
- [legal-redline-tools](https://github.com/evolsb/legal-redline-tools)
- [Agent Skills standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown analysis with tables, prioritized risks, suggested redline language, and optional JSON redlines for downstream document tooling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as first-pass legal analysis and negotiation preparation, not legal advice.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog identify upstream skill content as 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
