## Description:

Use when benchmarking similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and cloud platform teams use this skill to compare documentation and API reference quality across major cloud providers for a chosen product area, then identify prioritized improvement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Alibaba Cloud access keys even though the benchmark primarily reviews public documentation.

Mitigation: Do not provide Alibaba Cloud credentials unless the publisher removes or justifies that prerequisite; if credentials are needed, use least-privilege keys in a controlled environment.

Risk: Weak URL validation can be abused to fetch unintended hosts during documentation discovery or manual link pinning.

Mitigation: Run the skill in a network-restricted environment and prefer pinned, verified HTTPS documentation links from official provider domains.

Risk: Auto-discovery may miss authoritative, private, localized, or newly reorganized documentation pages.

Mitigation: Use the manual provider link flags to pin authoritative documentation before relying on benchmark rankings or improvement priorities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-platform-docs-benchmark)
- [Review rubric](references/review-rubric.md)
- [Scoring profiles](references/scoring.json)
- [Preset configuration](references/presets.json)
- [Alibaba Cloud Model Studio documentation](https://help.aliyun.com/zh/model-studio/)
- [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview)
- [Google Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report plus JSON evidence files, with command guidance and prioritized recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Benchmark runs write benchmark_report.md and benchmark_evidence.json under output/aliyun-platform-docs-benchmark/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
