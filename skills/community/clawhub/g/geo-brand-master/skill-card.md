## Description:

Geo Brand Master monitors brand visibility across AI search platforms, scores visibility from 0 to 100, generates optimization analysis, and can send reports to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether selected brands or competitors appear in AI platform responses, then produce visibility scores, markdown reports, and optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends brand names, competitor terms, snippets, and reports to external AI/search services and to Feishu when configured.

Mitigation: Use only data approved for those services, configure webhooks carefully, and avoid submitting confidential brand strategy or customer information.

Risk: The bundled Flask API is not suitable for public exposure in its current form.

Mitigation: Keep the API private unless authentication, input validation, rate limits, network binding, and key handling have been reviewed and fixed.

Risk: Local quota and report files can retain sensitive monitoring data.

Mitigation: Review file locations, retention, and access permissions before production use.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin and review dependencies before deploying the skill in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeffersplind92/skills/geo-brand-master)
- [Publisher Profile](https://clawhub.ai/user/jeffersplind92)
- [YK-Global Official Site](https://yk-global.com)
- [Tavily Search API](https://tavily.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, terminal output, JSON API responses, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include brand names, competitor terms, platform snippets, GEM scores, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
