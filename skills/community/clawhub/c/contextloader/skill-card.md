## Description: <br>
Loads business knowledge-network context through the Context Loader API for concept retrieval, object or action type recognition, object instance queries, instance subgraph expansion, logical property resolution, dynamic action recall, and knowledge-network build status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yannan](https://clawhub.ai/user/yannan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve business knowledge-network context, identify relevant object and action schemas, query real object instances, expand instance relationships, resolve logical properties, and recall eligible actions. It is intended for workflows where the agent must ground follow-up API calls in real identifiers rather than inventing knowledge-network IDs or instance identities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call a Context Loader endpoint with an account-scoped APP_USER_ID, which may expose business knowledge-network data to the agent. <br>
Mitigation: Install it only for trusted Context Loader endpoints and use an APP_USER_ID that is authorized for the relevant knowledge-network data. <br>
Risk: Ambiguous or stale SOUL.md knowledge-network entries can lead the agent to query the wrong business knowledge network. <br>
Mitigation: Keep SOUL.md entries accurate and require user confirmation when multiple candidate knowledge networks cannot be resolved confidently. <br>
Risk: Knowledge-network rebuild requests are operational changes that may consume backend resources. <br>
Mitigation: Review rebuild requests before execution and treat them as deliberate operational actions. <br>


## Reference(s): <br>
- [Context Loader API calling guide](references/api-calling.md) <br>
- [Context Loader examples](references/examples.md) <br>
- [Knowledge schema search OpenAPI](references/openapi/kn_schema_search.yaml) <br>
- [Knowledge network search OpenAPI](references/openapi/kn_search.yaml) <br>
- [Object instance query OpenAPI](references/openapi/query_object_instance.yaml) <br>
- [Instance subgraph query OpenAPI](references/openapi/query_instance_subgraph.yaml) <br>
- [Logical property resolver OpenAPI](references/openapi/get_logic_properties_values.yaml) <br>
- [Action recall OpenAPI](references/openapi/get_action_info.yaml) <br>
- [Knowledge-network build job OpenAPI](references/openapi/ontology_job.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/yannan/contextloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, HTTP, or shell command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the API used, key IDs such as kn_id, ot_id, at_id, and _instance_identity, candidate instances when multiple matches exist, and the next recommended API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
