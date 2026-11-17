## Description:

City Life Copilot helps users plan city outings by combining AMap routing and web content retrieval for mood-based routes, social-post route replication, housing-area scans, and accessible travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzhyjr2021-beep](https://clawhub.ai/user/hzhyjr2021-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn city-life requests into route, housing, and accessibility guidance. It can generate local HTML report cards with embedded AMap route maps for weekend plans, social-media route replication, property-area assessment, and mobility-aware trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify the OpenClaw skills directory and install unpinned third-party components.

Mitigation: Review scripts/install.js before running it, avoid elevated privileges, and install only in a trusted or disposable OpenClaw workspace.

Risk: Browser automation and web fetching may access user-provided social-media or route-planning pages.

Mitigation: Use the skill only with expected city-planning links and review extracted locations before trusting or sharing generated routes.

Risk: Generated HTML reports are local files that may load network-backed map content.

Mitigation: Treat generated reports as network-enabled pages, review them before sharing, and avoid opening untrusted reports in privileged contexts.

## Reference(s):

- [City Life Copilot skill page](https://clawhub.ai/hzhyjr2021-beep/skills/city-life-copilot)
- [Publisher profile](https://clawhub.ai/user/hzhyjr2021-beep)
- [Workflow rules](references/workflows.md)
- [AMap LBS skill dependency](https://www.modelscope.cn/skills/@AMap-Web/amap-lbs-skill)
- [Web anti-crawl fetch dependency](https://clawhub.ai/dlutwuwei/web-anti-crawl-fetch)
- [SkillHub installation guide](https://skillhub.cn/install/skillhub.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses and generated local HTML files with embedded map iframes and route data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML reports are saved locally and may load network-backed map content.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
