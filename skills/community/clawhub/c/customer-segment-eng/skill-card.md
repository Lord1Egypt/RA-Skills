## Description: <br>
Analyzes uploaded bank customer data to segment and profile customers by assets, transactions, behavior, and activity, then produces tables, charts, and a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yukirang](https://clawhub.ai/user/yukirang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and business teams use this skill to process authorized banking customer datasets, engineer RFM-style features, run clustering, and summarize customer segments for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive banking customer data and may write customer-level exports. <br>
Mitigation: Run it only on datasets the user is authorized to process, prefer pseudonymized customer IDs, use a restricted output directory, and avoid retaining customer-level exports unless necessary. <br>
Risk: Customer segmentation outputs could be misused for discriminatory pricing or other unfair treatment. <br>
Mitigation: Review segment labels and downstream use against applicable compliance and fairness requirements before relying on the results. <br>


## Reference(s): <br>
- [RFM Model Reference](references/rfm-guide.md) <br>
- [Clustering Analysis Parameter Reference](references/clustering-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance plus generated CSV, PNG, and Markdown analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes segmentation_results.csv, cluster_summary.csv, segmentation_charts.png, and segmentation_report.md to an output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
