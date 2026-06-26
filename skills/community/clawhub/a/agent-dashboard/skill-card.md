## Description: <br>
Agent Dashboard helps OpenClaw users generate and deploy dashboard views for active tasks, cron health, issues, and action items across local canvas, GitHub Pages, or Supabase/Vercel tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tahseen137](https://clawhub.ai/user/tahseen137) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to view operational status for active agent work, scheduled jobs, action items, product status, and recent activity. It supports local viewing as well as optional hosted dashboards that update through GitHub Pages polling or Supabase Realtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted dashboard tiers may expose operational status publicly or allow tampering despite client-side PIN protection. <br>
Mitigation: Use Tier 1 for local-only viewing, or add stronger hosting and database access controls before using Tier 2 or Tier 3. <br>
Risk: Dashboard fields can reveal sensitive task names, internal URLs, customer data, or meaningful error details if users include them in status updates. <br>
Mitigation: Keep dashboard data limited to non-sensitive operational status and avoid secrets, customer data, internal URLs, and detailed error content. <br>
Risk: Scheduled dashboard updates may continue publishing status after the dashboard is no longer needed. <br>
Mitigation: Disable the dashboard cron job when monitoring is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tahseen137/agent-dashboard) <br>
- [Customization Guide](references/customization.md) <br>
- [Dashboard sample data](assets/templates/dashboard-data.json) <br>
- [Supabase setup SQL](assets/templates/setup-supabase.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSON, SQL, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dashboard setup instructions and deployable dashboard assets across three tiers.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
