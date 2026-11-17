## Description:

Execute and improve Avenir-Web autonomous web tasks end-to-end with mode selection, instruction validation, single or batch runs, and next-step recommendations.

This skill is for research and development only.

## Publisher:

[yiliu-li](https://clawhub.ai/user/yiliu-li)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and automation engineers use Avenir Web to run autonomous browser tasks, inspect task results, and iterate on instructions or configuration. The skill supports single runs, batch runs, one-step browser actions, and screenshot-based page reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary URLs, including sites that may expose sensitive or internal information.

Mitigation: Run it in a contained environment with network egress controls and URL allowlisting; avoid private dashboards, localhost, internal services, and authenticated accounts unless explicitly approved.

Risk: Screenshots and page-derived text may be sent to the configured LLM provider and retained in local artifacts.

Mitigation: Use non-sensitive browser sessions, avoid pages containing secrets, and apply logging redaction and artifact-retention controls before broader use.

Risk: Server security evidence reports verified safety weaknesses and vulnerable dependencies.

Mitigation: Update vulnerable dependencies and address URL allowlisting, task_id path validation, logging redaction, and the os.system copy path before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yiliu-li/skills/avenir-web)
- [Avenir-Web arXiv Paper](https://arxiv.org/abs/2602.02468)
- [Avenir-Web PDF](https://arxiv.org/pdf/2602.02468.pdf)
- [Avenir-Web Demo Video](https://www.youtube.com/watch?v=X38CH0xc_sg&t=16s)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON summaries, and generated run artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs may create local artifacts such as agent logs, result JSON, resolved config snapshots, LLM records, and screenshots.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; package pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
