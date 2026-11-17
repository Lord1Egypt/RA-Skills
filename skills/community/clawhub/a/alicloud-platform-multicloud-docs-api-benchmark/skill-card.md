## Description:

Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation teams use this skill to compare similar product documentation and API references across major cloud providers. It helps rank documentation quality, identify integration blockers, and produce prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Alibaba Cloud credentials although the documented benchmark is documentation-only.

Mitigation: Run without cloud access keys unless a revised version explains why credentials are required and limits them to read-only scope.

Risk: URL filtering may allow unintended internal or arbitrary fetches when links come from untrusted input.

Mitigation: Run in a sandbox with restricted outbound network access and use only trusted, pinned official documentation URLs.

Risk: Automated discovery can return low-confidence or incomplete documentation matches.

Mitigation: Prefer user-pinned authoritative links and review generated rankings and recommendations before using them for decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cinience/skills/alicloud-platform-multicloud-docs-api-benchmark)
- [Review rubric](references/review-rubric.md)
- [Scoring configuration](references/scoring.json)
- [LLM platform preset](references/presets.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report and JSON evidence files, with concise agent guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes benchmark_report.md and benchmark_evidence.json under output/alicloud-platform-multicloud-docs-api-benchmark/.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
