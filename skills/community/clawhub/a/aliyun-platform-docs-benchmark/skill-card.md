## Description: <br>
Use when benchmarking similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation teams use this skill to compare cloud provider product and API documentation, score coverage with a shared rubric, and generate prioritized improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks users to configure Alibaba Cloud credentials even though the benchmark workflow appears limited to public documentation discovery and local report generation. <br>
Mitigation: Run without cloud credentials when possible; if credentials are necessary, use least-privilege read-only Alibaba Cloud credentials and confirm the required APIs with the publisher. <br>
Risk: Automatic discovery can miss official, private, or localized documentation and produce low-confidence comparisons. <br>
Mitigation: Pin authoritative provider links with the --<provider>-links options for strict comparisons and rerun when confidence is low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-platform-docs-benchmark) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [Review rubric](references/review-rubric.md) <br>
- [Scoring profiles](references/scoring.json) <br>
- [Benchmark presets](references/presets.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON evidence files, and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes benchmark_evidence.json and benchmark_report.md under output/aliyun-platform-docs-benchmark/] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
