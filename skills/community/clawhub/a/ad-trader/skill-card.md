## Description:

AI广告投手 Ad Trader helps advertising optimizers import multi-platform campaign data, diagnose ROI/ROAS/CTR/CVR/CPA performance, recommend budget and creative adjustments, and generate interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT

## Use Case:

External marketing teams, ad traders, and analysts use this skill to normalize advertising exports, review account health, detect anomalies, and produce budget, bidding, creative, and reporting guidance. It supports Tencent Ads, Ocean Engine, Baidu Ads, Meta Ads, and Google Ads style data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can expose sensitive advertising performance, campaign, and creative data.

Mitigation: Treat generated reports as sensitive business documents and store or share them only through approved channels.

Risk: Reports generated from untrusted datasets may include unsafe content when opened.

Mitigation: Use trusted datasets, sanitize campaign and creative names before report generation, and avoid opening reports produced from untrusted files.

Risk: HTML reports load Chart.js from jsDelivr when opened.

Mitigation: Bundle Chart.js locally or integrity-pin the dependency when remote CDN loading is not acceptable.

## Reference(s):

- [README](README.md)
- [广告投放指标体系](references/metrics.md)
- [主流广告投放平台对比](references/platforms.md)
- [广告投放优化最佳实践](references/strategies.md)
- [Tencent Ads Marketing API](https://developers.e.qq.com/)
- [Ocean Engine Marketing API](https://open.oceanengine.com/)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, JSON, HTML files, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text or JSON summaries, shell command suggestions, optional normalized data files, and generated interactive HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML reports may contain sensitive campaign data and load Chart.js from jsDelivr unless the dependency is bundled or integrity-pinned.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
