## Description:

Benchmark and compare agent prompts and evaluation results. Use when tuning strategies, evaluating outputs, or comparing configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to log, search, benchmark, compare, and export prompt, evaluation, cost, usage, and optimization records during agent experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, evaluations, cost notes, and related exports may be stored locally in plaintext.

Mitigation: Do not log secrets, credentials, customer data, or proprietary prompts unless the machine and file permissions are controlled; treat exports as sensitive files.

## Reference(s):

- [Agent Learner on ClawHub](https://clawhub.ai/xueyetianya/skills/agent-learner)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, files, JSON, CSV]

**Output Format:** [stdout text with optional exported json, csv, or txt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists timestamped local records and writes exports to the agent-learner data directory.]

## Skill Version(s):

2.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
