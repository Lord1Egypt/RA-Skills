# Runtime Adapter Contract

`gear-up` is portable policy. Hot creation and activation require runtime support. An adapter should expose the following conceptual operations without forcing portable skills to know harness-specific tool names.

## Minimum useful operations

- `inspect_capabilities` — list discoverable skills, tools, context mechanisms, and supported artifact types.
- `search_academy` — search lightweight Academy metadata without loading every candidate.
- `create_ephemeral_workspace` — return an isolated task-scoped location.
- `validate_artifact` — perform structural/syntax/security checks appropriate to the artifact type.
- `activate_artifact` — activate a temporary skill/context/tool and return explicit confirmation or failure.
- `deactivate_artifact` — remove the temporary capability from the active runtime when supported.
- `record_outcome` — persist evidence needed for Academy evaluation.
- `cleanup_workspace` — delete ephemeral artifacts that are not retained as candidates.

An implementation may combine these operations, but it must preserve their semantics.

## Activation contract

Activation must return evidence such as:

```yaml
artifact_id: req-normalizer
artifact_type: tool
status: active
scope: current-session
runtime: pi
validation:
  syntax: pass
  smoke_test: pass
```

A file being written to disk is not activation evidence.

## Safety contract

Adapters must not let generated artifacts silently obtain broader permissions than the active agent already has. When the harness cannot sandbox generated executable code, treat it as ordinary executable code with user permissions and apply `dry-run` / `human-gates` proportionately.

## Fallback contract

If the runtime cannot activate an artifact hot:

1. report `status: staged`, never `active`;
2. provide the smallest reload/session action needed;
3. continue with existing capabilities only when that can still satisfy the task safely;
4. otherwise stop capability creation rather than generating more staged artifacts.
