## Description: <br>
Dreamer assists with drug-delivery smart responsive material design through molecule generation, property annotation, screening, recommendation, visualization, and research monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-kuki](https://clawhub.ai/user/z-kuki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Scientists, decision-makers, and technical users can use Dreamer to design candidate drug-delivery molecules, classify properties, rank candidates, tune models with preference data, and generate decision-oriented analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may perform web research, local file writes, or compute-heavy model operations. <br>
Mitigation: Install and run it only in a sandbox where network access, compute cost, and local output paths are acceptable. <br>
Risk: Research-memory files may contain private or stale information that could influence generated molecule designs. <br>
Mitigation: Review or clear knowledge_data/latest_research.txt before generation, especially for sensitive scientific work. <br>
Risk: Unapproved or mutable model checkpoints can affect scientific reliability and reproducibility. <br>
Mitigation: Prefer pinned or locally approved model checkpoints for sensitive work. <br>


## Reference(s): <br>
- [Dreamer ClawHub skill page](https://clawhub.ai/z-kuki/drug-delivery-llm) <br>
- [LLM Generation workflow](references/skill_llm_generation.md) <br>
- [Property Classification workflow](references/skill_property_classification.md) <br>
- [Filtering and Recommendation workflow](references/skill_filtering_recommendation.md) <br>
- [RLHF Optimization workflow](references/skill_rlhf_optimization.md) <br>
- [Data Visualization workflow](references/skill_data_visualization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports, generated code or shell commands, molecule lists, scores, model artifacts, and visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local files such as NumPy arrays, LoRA weights, and SVG or JPG figures when the referenced workflows are executed.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
