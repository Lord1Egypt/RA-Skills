## Description:

资源交付分发技能 - 处理素材导出、格式转换和多平台分发

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Ad production teams and developers use this skill to export completed advertising materials, convert formats, package assets, and prepare distribution to social media and advertising platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future versions with real platform uploads could send ad assets, platform configuration, or account credentials to third-party services.

Mitigation: Require explicit confirmation of target platforms, assets, configuration, and credential use before distribution.

Risk: Platform packaging and conversion outputs are represented as local or mock paths in the inspected artifacts.

Mitigation: Verify generated packages, converted files, and platform requirements before relying on them for production delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeyeshield/skills/ad-production-delivery-distribution)

## Skill Output:

**Output Type(s):** [Files, Configuration, Text]

**Output Format:** [JSON command responses with package IDs, download paths, platform requirements, distribution results, and manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates delivery package records and mock local package or conversion paths; inspected artifacts do not include real platform upload or credential handling.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
