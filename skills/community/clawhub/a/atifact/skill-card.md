## Description:

Converts HAR files, Claude Code JSONL logs, and Copilot CLI JSONL logs into ATIF v1.6 trajectory JSON using the atifact CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert agent session recordings into structured ATIF trajectory JSON. It helps them run the atifact CLI, choose the right input format, write trajectory files, and report generated output paths and key metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session logs and generated trajectory JSON may preserve prompts, responses, tool outputs, headers, metadata, or other confidential content.

Mitigation: Process HAR and session logs in a controlled directory, then review and redact generated trajectory JSON before sharing it.

Risk: The workflow depends on an externally installed npm CLI.

Mitigation: Install atifact only from a trusted npm package source, and pin or review the package version before use.

## Reference(s):

- [ClawHub atifact skill page](https://clawhub.ai/waldekmastykarz/skills/atifact)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline bash commands and ATIF trajectory JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated trajectories may include main and subagent JSON files, or a combined JSON array on stdout when requested.]

## Skill Version(s):

0.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
