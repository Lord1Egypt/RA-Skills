## Description: <br>
Manage Volcengine Supabase workspaces, branches, SQL queries, migrations, Edge Functions, Storage, and TypeScript type generation through a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Volcengine Supabase backend resources, including workspaces, branches, SQL migrations, Edge Functions, Storage, API keys, and generated TypeScript types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can receive administrator-level access to Volcengine Supabase resources. <br>
Mitigation: Install it only for users who need that access, use least-privilege credentials, and review workspace, database, Storage, and Edge Function changes before execution. <br>
Risk: Service-role keys or other sensitive credentials may be exposed if reveal options are used or results are copied into chat or logs. <br>
Mitigation: Keep key output masked by default, use reveal options only for a specific operational need, and avoid placing service-role keys in client-side code, transcripts, or logs. <br>
Risk: Powerful SQL and deployment operations can change or delete production resources, and evidence notes that READ_ONLY should not be relied on as a complete safety control until specific database actions are fixed. <br>
Mitigation: Manually review SQL, migrations, and deployment inputs before running them, and enforce read-only or change-control limits outside the skill where production safety matters. <br>


## Reference(s): <br>
- [Tool Reference](references/tool-reference.md) <br>
- [Workflows](references/workflows.md) <br>
- [SQL Playbook](references/sql-playbook.md) <br>
- [Application Integration Guide](references/app-integration-guide.md) <br>
- [Schema Design and Migration Guide](references/schema-guide.md) <br>
- [Row Level Security Guide](references/rls-guide.md) <br>
- [Edge Function Development Guide](references/edge-function-dev-guide.md) <br>
- [Volcengine](https://www.volcengine.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-supabase) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-oriented CLI results, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Volcengine Supabase APIs through the bundled CLI and may surface masked or explicitly revealed credential material depending on command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
