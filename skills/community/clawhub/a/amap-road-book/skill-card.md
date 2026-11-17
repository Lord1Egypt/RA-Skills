## Description:

Generates Amap road books from natural-language travel plans, including clarification questions, place lookup, route planning, daily timelines, weather notes, and optional public HTML, JSON, and Excel outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuo-wentao](https://clawhub.ai/user/zuo-wentao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to turn travel ideas into executable Amap itineraries with routes, daily schedules, weather reminders, assumptions, and shareable outputs. It is also useful for agents that need to produce structured roadbook JSON plus optional HTML and Excel artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default public publishing can expose itinerary details, travel dates, lodging areas, budgets, generated files, and Amap credentials.

Mitigation: Prefer local-only generation unless the user accepts public sharing; remove credentials from exported JSON and share public links only with trusted recipients.

Risk: The evidence security summary flags unsafe upload and rendering paths for published roadbooks.

Mitigation: Use authenticated HTTPS publishing, enforce the publish token server-side, sanitize generated HTML, and review generated artifacts before sharing.

Risk: Unrestricted or valuable Amap keys can be exposed or misused if used with this skill as written.

Mitigation: Use restricted test keys, rotate keys after testing, and avoid storing real keys in committed files or public outputs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zuo-wentao/skills/amap-road-book)
- [Amap Open Platform](https://lbs.amap.com/)
- [OpenClaw Skill Format](https://docs.openclaw.ai/clawhub/skill-format)
- [Amap API mapping](references/amap-api-map.md)
- [Clarification policy](references/clarification-policy.md)
- [Roadbook schema](references/roadbook-schema.md)
- [Demo scenarios](references/demo-scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Excel files, Shell commands, Configuration guidance]

**Output Format:** [Markdown response with itinerary details and links; generated JSON, HTML, and XLSX files when the bundled scripts run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_WEB_SERVICE_KEY, AMAP_JS_API_KEY, and AMAP_JS_SECURITY_CODE for full Amap-backed generation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
