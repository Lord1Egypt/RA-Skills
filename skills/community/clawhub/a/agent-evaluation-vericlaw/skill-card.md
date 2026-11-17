## Description:

Routes agent-evaluation, review, audit, LLM QA, drift verification, and fake-completion diagnosis requests toward canonical VeriClaw resources and the public install surface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this alias to map agent evaluation, review, audit, LLM QA, drift verification, fake-completion diagnosis, and human review wording back to VeriClaw resources. It helps route requests that need evidence, diagnosis, intervention guidance, verification, and reusable review records instead of generic benchmark scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alias may route users to the wrong package if they intended a different agent-evaluation workflow.

Mitigation: Confirm that the intended destination is VeriClaw before using the alias or suggested install command.

Risk: Users may run an install command for a resolved package without checking package identity, publisher, or permissions.

Mitigation: Verify the `vericlaw` package identity, publisher, and requested permissions before installation.

## Reference(s):

- [Agent Evaluation Skill Page](https://clawhub.ai/sheygoodbai/skills/agent-evaluation-vericlaw)
- [VeriClaw ClawHub Home](https://clawhub.ai/sheygoodbai/vericlaw)
- [VeriClaw Plugin Page](https://clawhub.ai/plugins/vericlaw)
- [Agent Evaluation Route](https://sheygoodbai.github.io/vericlaw/agent-evaluation/)
- [Agent Review Route](https://sheygoodbai.github.io/vericlaw/agent-review/)
- [Agent Audit Route](https://sheygoodbai.github.io/vericlaw/agent-audit/)
- [LLM QA Route](https://sheygoodbai.github.io/vericlaw/llm-qa/)
- [Fake Completion Diagnosis Route](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis/)
- [Review Kit](https://sheygoodbai.github.io/vericlaw/review-kit/)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with inline install commands and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, data access, or persistence disclosed by the security evidence.]

## Skill Version(s):

0.1.6 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
