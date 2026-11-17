## Description: <br>
Alibabacloud Migration Sdm Sql Trans helps agents translate SQL syntax across data warehouse engines, with implemented rules for Synapse T-SQL to Hologres PostgreSQL conversion and explicit handling for unsupported engine pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when an agent needs rule-based assistance converting SQL, DML, DDL, stored procedure patterns, functions, identifiers, data types, and query syntax from Synapse T-SQL to Hologres PostgreSQL. Unsupported engine pairs should be refused with clear alternatives rather than converted speculatively. <br>

### Deployment Geography for Use: <br>
No geography-specific deployment limit is stated in the evidence. Use where ClawHub access, organizational policy, and applicable database governance requirements permit. <br>

## Known Risks and Mitigations: <br>
Risk: Converted SQL or migration guidance may be incorrect or unsuitable for a production database. <br>
Mitigation: Review converted SQL manually, validate it against the target environment, and do not execute generated DDL or DML directly in production. <br>
Risk: The skill is rule-based and only Synapse to Hologres is implemented; unsupported engine pairs could lead to speculative output if not rejected. <br>
Mitigation: Treat unsupported engine pairs as manual work until the relevant rule files are added, and require explicit refusal plus actionable alternatives. <br>
Risk: Including real business data, database names, credentials, or connection strings in prompts or examples could expose sensitive information. <br>
Mitigation: Use placeholder names and synthetic values, and avoid entering secrets or real customer data into conversion examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-sdm-sql-trans) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Converted SQL snippets, validation notes, refusal messages for unsupported pairs, and concise migration guidance.] <br>
**Output Parameters:** [Input SQL, source engine, target engine, conversion scope, and any known schema, identifier casing, or target-environment assumptions.] <br>
**Other Properties Related to Output:** [Outputs should preserve source query structure, mark uncertain mappings for manual review, avoid real business data, and follow the skill's validation checklist before delivery.] <br>

## Skill Version(s): <br>
0.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
