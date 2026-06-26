## Description: <br>
Customer Segment analyzes banking customer CSV data with RFM-style feature engineering and K-Means clustering to produce customer segments, summary statistics, visualizations, and a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yukirang](https://clawhub.ai/user/yukirang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and analysts use this skill to segment banking customers from uploaded transaction, asset, and behavior datasets and generate actionable segment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive banking customer segmentation outputs to local CSV, PNG, and Markdown files. <br>
Mitigation: Install only in workspaces approved for banking or customer data, use a restricted output folder, consider pseudonymizing customer IDs, and delete generated files when they are no longer needed. <br>


## Reference(s): <br>
- [RFM Model Reference](references/rfm-guide.md) <br>
- [Clustering Analysis Parameter Reference](references/clustering-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yukirang/customer-segment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Command-line status text plus generated CSV, PNG, and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes segmentation_results.csv, cluster_summary.csv, segmentation_charts.png, and segmentation_report.md to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
