## Description: <br>
雄韬企业头条助手为企业生成专业级公关头条文案与海报，覆盖签约、考察、技术升级、合作、节日和行业动态等场景，并支持制造业、财税、科技SaaS、新能源、电商消费和通用行业预设。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtoyun](https://clawhub.ai/user/xtoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and communications teams use this skill to draft company news, public-relations posts, internal updates, channel-specific copy, and poster assets for routine business announcements. It guides higher-risk events into human-led review instead of generating final sensitive content automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store company names, customer details, brand tone, and other business context in `.company-headlines/brand-card.md`. <br>
Mitigation: Review what business information is appropriate to save locally, avoid storing confidential details unless approved, and back up the brand card before rerunning configuration. <br>
Risk: Optional image-generation or visual prompt workflows may expose unpublished announcements or sensitive brand context outside the local skill flow. <br>
Mitigation: Screen event details, customer names, visual prompts, and announcement timing before sending them through any Gemini or image-generation workflow. <br>
Risk: Generated PR drafts can contain inaccurate numbers, customer names, dates, or overstatements if source details are incomplete. <br>
Mitigation: Use the built-in review posture: verify numbers and names for L2 events, keep L3 events human-led, and limit L4 sensitive events to framing guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xtoyun/company-headlines) <br>
- [README](artifact/README.md) <br>
- [品牌配置向导](artifact/docs/00-品牌配置向导.md) <br>
- [叙事引擎手册](artifact/docs/01-叙事引擎手册.md) <br>
- [渠道适配手册](artifact/docs/03-渠道适配手册.md) <br>
- [事件分级与审批流](artifact/docs/05-事件分级与审批流.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown copy drafts, local brand-card configuration, generated HTML drafts, and PNG poster or cover image files when rendering dependencies are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node and Playwright for local HTML-to-PNG rendering; may fall back to HTML output when headless rendering is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
