## Description: <br>
Collects ecommerce category URLs, extracts category hierarchy data, and saves the results as CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QirongZhang](https://clawhub.ai/user/QirongZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operations users use this skill to turn product collection URLs into structured category CSV data for review, catalog analysis, or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes CSV files to a local output directory, which may create or replace same-name files. <br>
Mitigation: Set an explicit output directory and check for existing CSV files before running the script. <br>
Risk: The Python workflow depends on pandas. <br>
Mitigation: Install pandas from a trusted package source in the intended runtime environment. <br>
Risk: Category parsing is heuristic and may not match every ecommerce URL structure. <br>
Mitigation: Review the generated CSV before using it for catalog decisions or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QirongZhang/category-link-collector) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; generated CSV files use UTF-8-SIG encoding.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts lists of category URLs plus optional output directory and maximum hierarchy depth; creates local CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
