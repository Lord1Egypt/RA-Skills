## Description: <br>
Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation teams, and cloud platform teams use this skill to compare product documentation and API documentation across major cloud providers, then produce score rankings and prioritized improvement actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unnecessary Alibaba Cloud credential setup for a public documentation benchmarking workflow. <br>
Mitigation: Review before installing, use the skill only for public documentation benchmarking and local report generation, and do not provide Alibaba Cloud access keys unless a specific reviewed command requires them. <br>
Risk: The benchmark can rely on auto-discovered documentation links, which may miss authoritative pages or produce low-confidence comparisons. <br>
Mitigation: Pin official provider links with the documented --<provider>-links options and review the generated evidence JSON before using recommendations. <br>


## Reference(s): <br>
- [Review rubric](artifact/references/review-rubric.md) <br>
- [Scoring profiles](artifact/references/scoring.json) <br>
- [Benchmark presets](artifact/references/presets.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-platform-multicloud-docs-api-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report and JSON evidence files, with concise text recommendations and runnable shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes benchmark_evidence.json and benchmark_report.md under output/alicloud-platform-multicloud-docs-api-benchmark/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
