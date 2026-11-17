## Description:

雄韬企业头条助手为企业生成专业级公关头条文案与海报，覆盖签约、考察、技术升级、合作、节日、行业动态等场景，并支持制造业、财税、科技SaaS、新能源、电商消费和通用行业预设。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, communications, and operations teams use this skill to turn routine company events into Chinese-language public relations copy, channel-specific drafts, self-checklists, and poster or cover-image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand preferences and company messaging may be saved locally and could contain sensitive business context.

Mitigation: Keep confidential material out of the brand card when local retention is unacceptable and exclude .company-headlines/ from source control.

Risk: The poster workflow renders local HTML in a browser using Playwright/Chromium.

Mitigation: Render only trusted HTML and review generated designs before sharing or publishing them.

Risk: The skill depends on Node and Playwright/Chromium, which adds dependency review and update considerations.

Mitigation: Install dependencies from trusted sources and pin Playwright to a reviewed version for managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/company-headlines)
- [Brand configuration guide](docs/00-品牌配置向导.md)
- [Narrative engine manual](docs/01-叙事引擎手册.md)
- [Category writing guide](docs/02-品类写作指南.md)
- [Channel adaptation manual](docs/03-渠道适配手册.md)
- [Event severity and approval workflow](docs/05-事件分级与审批流.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown copy drafts, HTML poster designs, PNG render outputs, configuration files, and concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a local brand card under .company-headlines/ and may use Node with Playwright/Chromium to render trusted local HTML to PNG.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
