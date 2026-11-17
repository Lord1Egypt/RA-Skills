## Description:

Aggregates official Alibaba Cloud, Huawei Cloud, AWS, and Tencent Cloud documentation and generates structured cloud product comparison material for technical evaluation and learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, architects, and technical evaluators use this skill to collect official cloud-provider documentation and produce structured comparison reports for cloud migration, multi-cloud planning, architecture design, and product learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based scraping uses unsafe settings and loose URL validation.

Mitigation: Run only in a low-privilege environment without mounted secrets or sensitive workspaces, and prefer a revised version that removes --no-sandbox and enforces strict hostname and redirect allowlists.

Risk: Generated reports can be written to user-selected output paths.

Mitigation: Choose report output paths deliberately and review generated markdown before relying on it for technical decisions.

Risk: The optional --stealth mode changes browser behavior for JavaScript-heavy documentation sites.

Mitigation: Avoid --stealth unless normal scraping fails and the target documentation source is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/cloud-product-analysis)
- [Alibaba Cloud documentation entry](https://help.aliyun.com/zh/{product})
- [Huawei Cloud documentation entry](https://support.huaweicloud.cn/{product}/index.html)
- [AWS documentation entry](https://docs.aws.amazon.com/zh_cn/{service}/)
- [Tencent Cloud documentation entry](https://cloud.tencent.com/document/product)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with comparison tables, sourced documentation excerpts, update logs, and inline shell commands when installation or execution steps are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write markdown report files to a user-selected workspace path.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
