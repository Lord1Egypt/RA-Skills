## Description: <br>
A documentation aggregation skill that scrapes official Alibaba Cloud, Huawei Cloud, AWS, and Tencent Cloud product documentation and generates structured comparison reports for technical evaluation and learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, architects, and technical evaluators use this skill to collect official cloud product documentation, compare provider capabilities, and produce source-grounded markdown reports for product selection, learning, and architecture planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper opens a headless browser and contacts official cloud documentation sites. <br>
Mitigation: Install and run it only in workspaces where outbound documentation access is expected, and review fetched content before relying on generated comparisons. <br>
Risk: Generated output files may overwrite existing workspace files if filenames are reused. <br>
Mitigation: Choose explicit output filenames and inspect the target path before running the scraper. <br>
Risk: Optional stealth mode changes browser behavior for compatibility with JavaScript-heavy sites. <br>
Mitigation: Keep stealth mode disabled unless needed and consider the target site’s automation terms before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/cloud-product-analysis) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Cloud documentation scraper](scripts/cloud_doc_scraper.py) <br>
- [Alibaba Cloud documentation entry pattern](https://help.aliyun.com/zh/{product}) <br>
- [Huawei Cloud documentation entry pattern](https://support.huaweicloud.cn/{product}/index.html) <br>
- [AWS Chinese documentation entry pattern](https://docs.aws.amazon.com/zh_cn/{service}/) <br>
- [Tencent Cloud documentation entry example](https://cloud.tencent.com/document/product/213) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with extracted documentation, comparison tables, source notes, and concise chat summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write fetched documentation and analysis reports to workspace files; supports provider, product, output filename, page limit, and optional stealth mode parameters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
