## Description: <br>
Analyze CSV/Excel files with natural language. Get statistics, filter rows, find anomalies, generate summaries, and export results. No pandas needed - uses Python stdlib for lightweight operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to inspect local CSV datasets, calculate summaries, filter rows, find simple numeric outliers, group values, and export filtered results without installing pandas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Numeric filtering uses a constrained unsafe evaluation pattern. <br>
Mitigation: Use only simple comparisons on trusted CSV values, and replace the eval-based filter with explicit operator comparisons before sensitive or critical analysis. <br>
Risk: Excel and natural-language capabilities are overstated relative to the artifact behavior. <br>
Mitigation: Use this release for local CSV command-line analysis, and verify file format support and analytical outputs before relying on them. <br>
Risk: The analyzer loads CSV data into memory and is documented for files up to about 100MB. <br>
Mitigation: Use smaller local files or a streaming or pandas-based workflow for larger datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zacjiang/csv-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/zacjiang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Terminal text output with optional CSV file exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python standard-library CSV processing; filtered results can be written to a CSV output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
