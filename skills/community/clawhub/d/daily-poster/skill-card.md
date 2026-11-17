## Description:

Generate fixed Chinese poster variants for 摸鱼日报 and 百度热点/百度热搜 from minimal JSON, with SVG output and optional PNG/JPG/JPEG/WEBP export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[321704933](https://clawhub.ai/user/321704933)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interpret Chinese poster requests, choose the daily or Baidu hot-search layout, prepare JSON specs, and run Python renderers that produce shareable poster files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON specs may cause broad local file reads or outbound network fetches through fields such as image_path, data_path, or api_url.

Mitigation: Run with restricted filesystem and network access, avoid untrusted path or URL values, and use path and URL allowlists before production use.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/321704933/skills/daily-poster)
- [XXApi provider information](https://xxapi.cn/about)
- [2026 China holiday schedule source](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html)
- [Input and output schema](references/input-schema.md)
- [Daily poster example spec](references/daily-poster-spec.json)
- [Baidu hot-search example spec](references/baidu-hot-spec.json)
- [2026 holiday countdown data](references/holiday-countdown-2026.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON specs and shell commands; renderer output is JSON plus SVG or image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily and baidu_hot poster types; image export formats include SVG, PNG, JPG, JPEG, and WEBP.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
