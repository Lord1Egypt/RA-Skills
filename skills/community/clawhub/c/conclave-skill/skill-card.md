## Description:

Conclave is a multi-agent reasoning skill that orchestrates multiple AI CLIs into structured debates. Each agent independently analyzes the problem, challenges competing arguments, identifies flaws and contradictions, and refines the reasoning through multiple rounds of discussion - helping you reach more reliable conclusions than relying on a single AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mclyang](https://clawhub.ai/user/mclyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and decision makers use Conclave to run structured multi-agent debates for consequential decisions such as architecture choices, contract risk, pricing, or investment judgment. It produces chair-adjudicated markdown reports, meeting minutes, and debate records after multiple AI agents analyze, rebut, and converge on a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and preflight can change global CLI tools and dependencies.

Mitigation: Review the install and update behavior first; use --check-only for inspection and --skip-update when you do not want automatic CLI updates.

Risk: Debate topics and drafts can be sent to multiple third-party AI providers.

Mitigation: Use official provider endpoints unless intentionally choosing a relay, obtain appropriate approval, and avoid sensitive, regulated, classified, or trade-secret material.

Risk: Full debate records persist under ~/.hermes/debates and may be exported into the working directory.

Mitigation: Run debates from a private non-synced directory and periodically delete archives and exported copies with the provided cleanup workflow.

Risk: Credential readiness is checked across local CLI and environment configuration.

Mitigation: Provide credentials only through each provider's normal authentication path and do not paste secrets into prompts or debate files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mclyang/skills/conclave-skill)
- [Consensus protocol v1.1](references/consensus-protocol-v1.md)
- [Panelist roster](references/panelists.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, debate files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent debate archives and exported copies unless the user cleans them up.]

## Skill Version(s):

1.6.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
