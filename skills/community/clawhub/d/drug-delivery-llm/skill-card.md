## Description:

Dreamer helps agents design, classify, filter, recommend, and visualize drug-delivery smart-response material candidates, especially visible-light-responsive molecules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-kuki](https://clawhub.ai/user/z-kuki)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, materials scientists, and developers use Dreamer to generate and evaluate drug-delivery material candidates, annotate molecular properties, rank candidates, optimize generation behavior, and produce decision-oriented analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workflows can train models, scrape sources, and write outputs automatically.

Mitigation: Run the skill only in an isolated sandbox and require explicit approval before training, scraping, or writing outputs.

Risk: The web monitor can persist scraped research and news into agent context.

Mitigation: Disable or gate the web monitor and treat latest_research.txt as untrusted reference data.

Risk: Model and checkpoint loading may use mutable or unsafe artifacts.

Mitigation: Pin model and checkpoint sources and review them before loading.

Risk: Private molecule data or credentials could be exposed if the skill is installed in a sensitive environment.

Mitigation: Do not provide credentials or sensitive private molecule data unless workflows have been reviewed and constrained.

## Reference(s):

- [LLM Generation Workflow](references/skill_llm_generation.md)
- [Property Classification Workflow](references/skill_property_classification.md)
- [Filtering and Recommendation Workflow](references/skill_filtering_recommendation.md)
- [RLHF Optimization Workflow](references/skill_rlhf_optimization.md)
- [Data Visualization Workflow](references/skill_data_visualization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports with generated molecule lists, scores, plots, code, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflows may produce saved files such as .npy molecule arrays, model checkpoints or LoRA weights, scraped research notes, and visualization images.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
