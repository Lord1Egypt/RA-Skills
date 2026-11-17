## Description:

contextloader helps agents load business knowledge network context through the Context Loader API, including concept retrieval, object and action type recognition, instance queries, subgraph expansion, logical property parsing, action recall, and build status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yannan](https://clawhub.ai/user/yannan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use contextloader to identify business knowledge network concepts and retrieve grounded object instances, relationship subgraphs, logical property values, dynamic actions, and build status before acting on that context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable service URL and account identifier can route requests or identity context to an unintended service.

Mitigation: Install only where administrators control CONTEXT_LOADER_BASE_URL and APP_USER_ID, and prefer HTTPS or trusted internal networking.

Risk: The skill can create full business knowledge network rebuild jobs.

Mitigation: Require explicit user confirmation and appropriate backend authorization before creating build jobs.

Risk: Using guessed knowledge network, object type, action type, or instance identifiers can produce incorrect context or actions.

Mitigation: Use only identifiers read from SOUL.md or returned by Context Loader API responses, and ask the user to choose when candidates are ambiguous.

## Reference(s):

- [Context Loader skill page](https://clawhub.ai/yannan/skills/contextloader)
- [Context Loader API calling guide](artifact/references/api-calling.md)
- [Context Loader examples](artifact/references/examples.md)
- [Semantic search OpenAPI spec](artifact/references/openapi/kn_schema_search.yaml)
- [Knowledge network search OpenAPI spec](artifact/references/openapi/kn_search.yaml)
- [Object instance query OpenAPI spec](artifact/references/openapi/query_object_instance.yaml)
- [Instance subgraph query OpenAPI spec](artifact/references/openapi/query_instance_subgraph.yaml)
- [Logical property resolver OpenAPI spec](artifact/references/openapi/get_logic_properties_values.yaml)
- [Action recall OpenAPI spec](artifact/references/openapi/get_action_info.yaml)
- [Knowledge network job OpenAPI spec](artifact/references/openapi/ontology_job.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance]

**Output Format:** [Markdown or structured text with JSON API request and response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CONTEXT_LOADER_BASE_URL and APP_USER_ID environment variables; outputs should include selected APIs, key identifiers, candidate instances when ambiguous, and next-step guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
