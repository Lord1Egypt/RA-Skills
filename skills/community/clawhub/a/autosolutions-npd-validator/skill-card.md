## Description: <br>
Run a full NPD validation pipeline on a product concept using coordinated research, independent evaluator perspectives, adversarial review, and consensus scoring to produce a GO, CONDITIONAL GO, REVISIT, or NO-GO recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, brand, and innovation teams use this skill to validate product concepts before launch decisions. It builds a concept brief, researches the market, coordinates specialist evaluations, and produces a scored recommendation with cited findings and iteration options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local files may contain confidential product, sales, customer, margin, or launch-planning details. <br>
Mitigation: Use an appropriate workspace for sensitive business data, avoid sharing confidential inputs unless permitted, and clean up generated data and reports when no longer needed. <br>
Risk: Web research and model-generated evaluations can be incomplete, outdated, or misleading for product launch decisions. <br>
Mitigation: Review cited sources, compare findings with internal data and expert judgment, and treat the recommendation as decision support rather than a final commercial approval. <br>
Risk: The workflow may use Bash for local report-file operations. <br>
Mitigation: Disable Bash or run the skill in a constrained environment when shell access is not allowed for this workflow. <br>


## Reference(s): <br>
- [NPD Product Validation Pipeline](SKILL.md) <br>
- [NPD Validation Methodology Reference](npd-methodology/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with scoring tables, cited research summaries, and local markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates concept briefs, evaluator reports, adversarial analysis, and final validation reports under local data paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
