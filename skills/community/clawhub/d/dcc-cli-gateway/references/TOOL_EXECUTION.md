# Tool execution

Run bundled `scripts/` commands from the dcc-mcp skill directory.

## CLI Invocation Contract

Run documented commands directly; do not preflight them with
`dcc-mcp-cli <command> --help`. Validate CLI-returned `next_step.command` and
`next_step.arguments` against the scope contract below before preserving them. Use targeted subcommand help at most once per
CLI version only after the documented syntax is rejected or when an option is
not covered here. Use `--output json` for the versioned zero-instance decision;
otherwise do not request it merely for agent-readable output.

```bash
dcc-mcp-cli reload-skills --instance-id <instance-id> --output toon
dcc-mcp-cli load-skill <skill-name> --instance-id <instance-id> --output toon
dcc-mcp-cli stop-instance --dcc-type <dcc-type> --instance-id <instance-id> --output toon
```

`stop-instance` is only for a test-owned instance that advertises a safe-stop
hook. Its `--dcc-type` and `--instance-id` flags are both required.

## Step 2 — Search Tools

Only run this when inventory shows at least one non-stale target:

```bash
# CLI (primary)
dcc-mcp-cli search --query "create sphere" --dcc-type maya --limit 20

# Python fallback
python scripts/dcc_gateway.py search --query sphere --dcc-type maya --limit 20
```

Copy the returned slug exactly and follow that hit's `next_step`; do not run
separate broad searches for selection, geometry, and scripting unless the
first result proves they are needed. Local and gateway slugs use the same
agent-facing shape:

```text
maya.a1b2c3d4.maya_primitives__create_sphere
```

Never hand-build slugs.

## Step 3 — Follow `next_step`

- `action=call` — call directly; no-schema tools receive this only when compact safety hints are already present.
- `action=describe` — inspect the schema and safety annotations, then call.
- `action=load_skill` — pass the returned arguments unchanged. If the load
  response includes `compact_schema` and `next_step.action=call`, call directly;
  otherwise describe the selected target once.

```bash
# Only when next_step.action=describe
dcc-mcp-cli describe maya.a1b2c3d4.maya_primitives__create_sphere

# Python fallback
python scripts/dcc_gateway.py describe maya.a1b2c3d4.maya_primitives__create_sphere
```

When describe or `compact_schema` is returned, use those exact parameter names
and safety annotations before calling.

## Step 4 — Call a Tool

```bash
# CLI (primary)
dcc-mcp-cli call maya.a1b2c3d4.maya_primitives__create_sphere \
  --require-gateway \
  --agent-session-id task-42 \
  --json '{"radius":2.0}'

# When the workflow reserved this instance, repeat the exact lease owner.
dcc-mcp-cli call maya.a1b2c3d4.maya_primitives__create_sphere \
  --require-gateway \
  --agent-session-id task-42 \
  --json '{"radius":2.0}' \
  --meta-json '{"lease_owner":"workflow-42"}'

# Python fallback
python scripts/dcc_gateway.py call maya.a1b2c3d4.maya_primitives__create_sphere \
  --json '{"radius":2.0}'
```

For asynchronous render/cook tools, add `--wait`; the CLI polls `jobs_get_status` at most once per second until terminal state and writes a 5%-step progress bar plus a 30-second stalled-job heartbeat to stderr while keeping the final result on stdout. Use `--wait-timeout-secs` for longer runs. The returned `job_id` is the backward-compatible alias of `core_job_id` (`job_id_owner=core`). If a direct call or terminal Core result launches adapter-owned work, `--wait` follows a registered `adapter_job.poll` on the same instance route and within the same total timeout. Core registers only synchronous, read-only, idempotent status tools whose only required input is a string `job_id`; every other input must be optional and safe when omitted. Never pass the inner ID to `jobs_get_status`, and do not assume Core cancellation propagates across the ownership boundary. A missing/unsafe poll contract or mismatched returned ID makes `--wait` fail closed without resubmitting work.
The bar uses `progress.current`, `progress.total`, and `progress.message`; do not repeatedly scan output files when typed progress exists.
Native MCP/REST clients may subscribe to `/v1/jobs/{job_id}/events`; otherwise keep the returned `job_id` and use bounded status polling.
Do not create a scheduled task by default. After an explicit cross-session monitoring request, schedule only a one-shot status check for that ID and stop it at terminal state.
During a host reload or gateway restart, keep the ID because status stays routable; `--wait` reports `control_plane_reconnecting` then `wait_recovery` and returns `tracking_status=owner_exited` when the DCC/sidecar owner is gone; never resubmit the render or cook.

Tool-specific fields (`code`, `file_path`, `radius`, and similar) belong inside the `--json` object; do not pass them as top-level CLI flags unless the CLI adds an explicit first-class flag later.

For materialized escape-hatch scripts, generate one typed `def main(...)` using JSON-preserving annotations, materialize it with `reuse=true` plus a stable `reuse_key`, inspect `parameters_schema`, then iterate on the same `file_path` by changing only `params`; never bake varying values into regenerated source, and when supported repeat `sha256` as an integrity assertion and require `context.materialized_script.reused=true`. Structured calls re-derive the schema from the verified body and retain the same sandbox and dispatcher boundary as legacy execution; a sidecar schema mismatch must fail closed. Requiredness follows default presence, not nullability, and leading-underscore parameter names follow ordinary `main(**params)` semantics. To retain Python 3.8 runtime compatibility, use `typing.List`, `typing.Dict`, and `typing.Tuple` for parameterized containers rather than PEP 585 built-in generics.

If the selected instance has an active pool lease, every `call` must carry the
same `lease_owner` through `--meta-json`. Missing owner metadata fails with
`instance-leased`; a different owner fails with `lease-owner-mismatch`. Do not
retry either error without the matching workflow owner or a different instance.
Expired leases and instances that were never leased need no owner metadata.
The hidden compatibility lease workflow requires a non-empty owner without
surrounding whitespace on acquire and the same owner on release; ownerless
release never clears an active lease.
The owner is a visible coordination label, not an authentication secret. Lease
enforcement coordinates gateway and local CLI workflows; it does not protect a
DCC adapter endpoint that an untrusted client can reach directly.

For generated scripts, binary descriptors, or other payloads that may exceed a
shell's command-line limit, pass the JSON object through a UTF-8 file or stdin:

```bash
dcc-mcp-cli call godot_project__write_script --json-file payload.json
generate_payload | dcc-mcp-cli call godot_project__write_script --json-file -
```

Use `--json` or `--json-file`, never both. `--json-file -` keeps large payloads
off the process command line, which is especially important on Windows.

See [`references/CLI_CHEATSHEET.md`](CLI_CHEATSHEET.md) for command
patterns and common errors.
