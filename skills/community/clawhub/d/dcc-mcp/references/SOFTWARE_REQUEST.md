# Request software support without automatic publication

When the user wants software added to DCC-MCP, prepare a structured local draft.
An empty live inventory or an old CLI catalog is not evidence of missing
support. First search the current official catalog with the safe entry point
in [UPDATE_INSPECTION.md](UPDATE_INSPECTION.md), the canonical product metadata,
and the relevant official adapter repository. Keep a failed lookup unknown.

Use this minimum-field draft, leaving unknown facts explicit:

```json
{
  "request_type": "software_support",
  "software": {"name": "", "vendor": "", "version": "unknown", "official_url": ""},
  "environment": {"os": "unknown", "architecture": "unknown"},
  "integration": {"public_api_or_scripting_docs": [], "license_class": "unknown"},
  "workflow": {"goal": "", "inputs": "synthetic description", "expected_result": ""},
  "existing_support": {"catalog": "unknown", "adapter_repository": null},
  "destination": {"repository": null, "verified_owner": false},
  "duplicates": {"status": "not_checked", "issue_urls": []},
  "publication": {"status": "draft", "requires_user_confirmation": true}
}
```

Review all free text locally. Do not include absolute paths, usernames,
computer names, environment dumps, credentials, project files, private assets,
chat transcripts, screenshots or raw logs. Link public vendor/API documentation
and describe a synthetic workflow. Do not assume an API exists or infer a
commercial licence grants redistribution rights.

For existing adapter/Skill/runtime failures, reuse `feedback route`,
`feedback bundle`, and plan-only `feedback file` with the repository/fingerprint,
content digest and exact-draft authorization binding described in
[FAILURE_REPORTING.md](FAILURE_REPORTING.md). This software-support draft is not
a Finding v1: never fabricate a tool failure or force it through an incompatible
schema. For a genuinely new software request with no owner, verify the current
request destination from the official [Core repository](https://github.com/dcc-mcp/dcc-mcp-core)
and its contribution/issue guidance. Do not guess an adapter repository.

Search for duplicates in that exact verified repository, using only the reviewed
public product/vendor and workflow terms. Present likely matches; a failed or
truncated search is not “no duplicates”. Before publishing, show the repository,
exact title and issue/comment body, and whether this creates an issue or adds to
an existing one. Ask for confirmation of that concrete publication. A user
asking to explore support, a catalog entry, or approval for software installation
does not authorize an external issue. Changed destination or content requires
fresh review. Leave the draft local when issue access is unavailable.
