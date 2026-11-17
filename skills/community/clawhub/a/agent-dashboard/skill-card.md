## Description:

Agent Dashboard provides a real-time OpenClaw dashboard for monitoring active tasks, cron health, issues, action items, products, and recent activity across canvas, GitHub Pages, or Supabase/Vercel deployment tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tahseen137](https://clawhub.ai/user/tahseen137)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to view agent activity, cron status, action items, product health, and recent events from a dashboard. It supports a local canvas mode and optional hosted modes for GitHub Pages polling or Supabase Realtime updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote tiers can publish operational agent and cron status outside the local machine.

Mitigation: Use Tier 1 for sensitive workflows, and keep dashboard fields free of internal URLs, secrets, private error text, personal data, or other confidential operational details.

Risk: The embedded client-side PIN is weak protection for hosted dashboards.

Mitigation: Add real server-side authentication, Vercel password protection, Supabase Auth, or a private hosting model before publishing sensitive dashboard content.

Risk: Tier 3 uses public Supabase anon access that can read and update the dashboard table.

Mitigation: Tighten Supabase policies for production use and limit the table to non-sensitive dashboard status data.

Risk: A scheduled cron update can continue publishing status data automatically.

Mitigation: Review the cron configuration and generated dashboard payload before enabling or changing scheduled publishing.

## Reference(s):

- [Customization Guide](references/customization.md)
- [ClawHub Skill Page](https://clawhub.ai/tahseen137/skills/agent-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON, SQL, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes static dashboard assets and setup paths for local canvas rendering, GitHub Pages polling, and Supabase Realtime deployment.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
