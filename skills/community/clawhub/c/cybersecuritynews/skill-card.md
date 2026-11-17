## Description:

Provides Chinese-language cybersecurity news collection and formatting guidance across company activity, mergers, incidents, vulnerabilities, policy updates, product concepts, and AI security applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donald-wick](https://clawhub.ai/user/donald-wick)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, researchers, and Chinese-language cybersecurity readers use this skill to ask an agent for structured news summaries from specified domestic and international sources. The skill standardizes ranking and output fields so each item includes a short summary, reporting-source list, source count, display link, and display-source name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cybersecurity news output may be incomplete or stale if the specified sources are unavailable, delayed, or outside the user's desired coverage.

Mitigation: Review the generated summaries against the current linked sources and adapt the source list when the deployment requires different coverage.

Risk: The skill is written for Chinese-language cybersecurity news workflows and may not match deployments that need another language or source policy.

Mitigation: Confirm language and source requirements before deployment, and revise the skill instructions when a different audience or source set is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donald-wick/skills/cybersecuritynews)
- [安全内参](https://www.secrss.com)
- [中国政府采购网](https://www.ccgp.gov.cn)
- [财新网科技](https://tech.caixin.com)
- [SecurityWeek](https://www.securityweek.com)
- [虎符智库](https://www.hufuzhiku.com)
- [国家网络安全通报中心](https://www.cac.gov.cn/jgsj/wxtb)
- [CNVD](https://www.cnvd.org.cn)
- [安全客](https://www.anquanke.com)
- [国家网信办](https://www.cac.gov.cn)
- [工信部](https://www.miit.gov.cn)
- [NIST](https://www.nist.gov)
- [Gartner](https://www.gartner.com)
- [安全牛](https://www.aqniu.com)
- [奇安信](https://www.qianxin.com)
- [深信服](https://www.sangfor.com.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown news summaries with source lists and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; each news item is expected to include a sub-100-character summary, reporting sites, source count, display link, and source name.]

## Skill Version(s):

1.0.0 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
