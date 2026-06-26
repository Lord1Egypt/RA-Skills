## Description: <br>
Manage the full lifecycle of Alibaba Cloud ADBPG Supabase projects, including listing, querying, creation, pause and resume, password reset, API key access, and security IP management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud AnalyticDB for PostgreSQL Supabase projects through Aliyun GPDB commands. It supports read-only inventory and detail lookups as well as controlled lifecycle, credential, and network-access operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve API keys and dashboard credentials. <br>
Mitigation: Require explicit approval before retrieving secrets, return them minimally, avoid shared logs, and rotate any exposed credentials. <br>
Risk: Create, pause, resume, password reset, and security IP changes can affect cost, availability, credentials, or network access. <br>
Mitigation: Use a least-privilege RAM profile and require explicit user confirmation with key parameters before any mutating command. <br>
Risk: Local CLI and plugin setup can affect which cloud account and commands are used. <br>
Mitigation: Verify the Aliyun CLI version, plugin source, and active credential profile without printing access keys or secrets. <br>


## Reference(s): <br>
- [CreateSupabaseProject API Reference](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/developer-reference/api-gpdb-2016-05-03-createsupabaseproject) <br>
- [Create Supabase Project Parameters](references/create-supabase-project-parameters.md) <br>
- [RAM Policies for ADBPG Supabase Management](references/ram-policies.md) <br>
- [Related APIs - ADBPG Supabase Management](references/related-apis.md) <br>
- [Operation Verification Methods](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and JSON-oriented CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud credentials, Aliyun CLI 3.3.3 or newer, the GPDB plugin, user confirmation for mutating operations, and careful handling of returned secrets.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
