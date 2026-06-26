## Description: <br>
Use the Rebrickable API through the included CLI for LEGO catalog lookup, user set/part lists, build analysis, lost parts, and guarded collection writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query the Rebrickable LEGO catalog and manage Rebrickable user set, part, build, and lost-part records through a guarded CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Rebrickable API key and may use a user token for private collection features. <br>
Mitigation: Keep credentials in environment variables, never print or paste real tokens, and rely on the CLI dry-run output that redacts authorization headers and user-token path segments. <br>
Risk: Collection write commands can create, update, or delete Rebrickable user data. <br>
Mitigation: Run dry-run before writes, restate the exact list, set or part, quantity, and action, and proceed only after explicit confirmation. <br>
Risk: Private Rebrickable profile, set-list, part-list, inventory, build-analysis, and lost-part data may be returned. <br>
Mitigation: Summarize only the fields needed for the user's request and avoid exposing unnecessary private collection details. <br>
Risk: Large inventory endpoints can return broad or resource-intensive results. <br>
Mitigation: Use filters and small page sizes for all-parts and similar browse commands, especially when the request can be answered by a narrower query. <br>


## Reference(s): <br>
- [Rebrickable OpenAPI reference](references/openapi/rebrickable.yaml) <br>
- [Rebrickable tools prompt reference](references/prompts/rebrickable-tools.txt) <br>
- [Rebrickable API base](https://rebrickable.com/api/v3) <br>
- [ClawHub skill page](https://clawhub.ai/musketyr/afol-rebrickable) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REBRICKABLE_API_KEY. User collection features require REBRICKABLE_USER_TOKEN. Mutating commands are expected to use dry-run first and require explicit approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
