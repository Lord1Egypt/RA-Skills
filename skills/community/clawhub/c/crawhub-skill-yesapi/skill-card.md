## Description: <br>
Wraps the YesApi 果创云 low-code platform APIs so an agent can manage form schemas and query, create, update, delete, and batch-change form data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phalapi](https://clawhub.ai/user/phalapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with a configured YesApi account for online database form schema management and data operations. It is intended for authenticated workflows that require querying, inserting, updating, deleting, or batch-modifying YesApi form records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live authenticated changes or deletions in the configured YesApi account. <br>
Mitigation: Use test or least-privileged credentials, verify YESAPI_DOMAIN before use, and avoid production data until destructive operations have explicit confirmation or dry-run previews. <br>
Risk: Batch update and batch delete operations can affect multiple records. <br>
Mitigation: Review the target model and where conditions before execution, and prefer small test queries before running batch changes. <br>
Risk: The included test script performs live API operations when configured with real credentials. <br>
Mitigation: Do not run test_yesapi.py against production credentials or production data. <br>


## Reference(s): <br>
- [YesApi API homepage](https://api.yesapi.net/) <br>
- [ClawHub skill page](https://clawhub.ai/phalapi/crawhub-skill-yesapi) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, API calls, configuration, guidance] <br>
**Output Format:** [Python dictionaries, JSON-compatible API responses, Markdown usage guidance, and Python code interfaces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YESAPI_APP_KEY, YESAPI_DOMAIN, and YESAPI_SIGN environment variables; operations may make live authenticated changes to the configured YesApi account.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, released 2026-03-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
