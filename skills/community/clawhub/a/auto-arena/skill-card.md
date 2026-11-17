## Description:

Auto Arena helps agents compare and rank multiple AI models or agents for a custom task by generating test queries, collecting endpoint responses, creating rubrics, running pairwise judge comparisons, and producing reports and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloml0326](https://clawhub.ai/user/helloml0326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation teams use this skill to run arena-style comparisons of at least two OpenAI-compatible model or agent endpoints on a task they define. It supports generating test queries and rubrics, collecting responses, ranking systems by win rate, and resuming or extending evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends prompts, generated queries, responses, and judge comparisons to configured external model providers.

Mitigation: Use only prompts and responses that are authorized for the selected providers, and configure endpoints and API keys according to the user's data-handling requirements.

Risk: Evaluation artifacts may be saved locally, including queries, responses, rubrics, comparison details, reports, and checkpoints.

Mitigation: Review the output directory before sharing or retaining results, and remove sensitive artifacts when they are no longer needed.

Risk: The prerequisite install commands use Python packages without pinned versions.

Mitigation: Install in an isolated virtual environment and pin reviewed package versions where reproducibility or supply-chain control is required.

## Reference(s):

- [Auto Arena Guide](https://agentscope-ai.github.io/OpenJudge/applications/auto_arena/)
- [ClawHub Auto Arena Skill](https://clawhub.ai/helloml0326/skills/auto-arena)
- [Publisher profile](https://clawhub.ai/user/helloml0326)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, YAML, and Python examples; evaluated runs may produce JSON results, Markdown reports, charts, and checkpoints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated queries, model responses, rubrics, pairwise comparison details, win-rate rankings, charts, and saved checkpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
