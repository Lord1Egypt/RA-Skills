## Description:

Automates CSB-AEP agent evaluation with automated scoring across seven dimensions and optional human review for final reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilozhao](https://clawhub.ai/user/lilozhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to test A2A-compatible agents for memory, preference handling, boundaries, trust behavior, learning, expression quality, and CSB-AEP behavior, then combine automated and human scores into reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured A2A endpoints may receive evaluation prompts and return sensitive agent responses over unsecured connections.

Mitigation: Review all configured endpoints before running all-agent mode, test only agents you control or have permission to evaluate, and require HTTPS for public hosts.

Risk: Evaluation reports can persist sensitive responses and scoring data under eval-results.

Mitigation: Protect the results directory, avoid collecting production-memory responses, and clean reports after review when they are no longer needed.

Risk: Memory and behavior tests may alter agent state or leave evaluation artifacts in agent memory.

Mitigation: Use isolated test identities or non-production agent memory during evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilozhao/skills/csb-agent-eval)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON and text evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped automatic and human evaluation reports under eval-results when the scripts are run.]

## Skill Version(s):

0.2.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
