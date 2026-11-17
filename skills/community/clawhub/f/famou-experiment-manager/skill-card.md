## Description:

Manages Famou evolutionary experiment workflows, including setup checks, experiment submission, status polling, cancellation, deletion, log retrieval, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaom0](https://clawhub.ai/user/zhaom0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and experiment operators use this skill to submit and manage Famou experiments from a workspace that contains a config.yaml file. It helps check local Famou CLI setup, configure API access, monitor validation status, and retrieve logs or results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install mutable packages and run Famou experiment lifecycle commands, including cancellation, deletion, and resubmission.

Mitigation: Use it in a controlled environment, prefer pinned and verified Famou SDK installs, and require explicit confirmation before destructive or resubmission actions.

Risk: Famou API keys may be provided through command-line arguments and stored in ~/.famou-ctl/settings.json.

Mitigation: Avoid entering API keys through command-line arguments when possible and check file permissions on ~/.famou-ctl/settings.json.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/zhaom0/skills/famou-experiment-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local Famou CLI configuration and may request user confirmation for experiment names, IDs, and selected config.yaml files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
