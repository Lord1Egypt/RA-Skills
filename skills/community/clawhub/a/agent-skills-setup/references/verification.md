# Verification and evidence

Read for migration delivery, bundle evidence, or rollback. Before apply, retain
the saved plan path and `plan_sha256`. The plan records each item's
`source_state` and `target_state`; apply checks those states, Registry,
adapters, and Git provenance before writing. Its checksummed manifest records
applied destination hashes, backup paths/hashes, item outcomes, losses, and plan
provenance. It does not contain a post-apply source check or parsing result.

Run `verify --manifest <manifest.json> --json`. It validates the manifest and
target boundaries, existence, and hashes against `changes[].post_sha256`.
A zero exit code means the recorded applied targets still match; it does not
recheck sources, reparse targets, or attest permissions or runtime behavior.

Report what the request needs: artifact locations, applied/deferred/blocked
counts, source unchanged status, target parse/hash checks, backup locations,
and remaining manual actions. Read the manifest when an orchestration summary
does not include that evidence. Zero applied items, plan generation, successful
extraction, or parse success alone do not prove a completed migration.

For live-file migration, record selected source hashes before apply and repeat
after apply (and after rollback, if requested). Use the installed helper so
large files and directory sources use the same bounded-memory hash as the plan:

```bash
python3 - "$(dirname "$migrator")" /resolved/source <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from migration_core import hash_path
print(hash_path(Path(sys.argv[2])))
PY
```

Use the source path from the plan and keep these outputs beside it, outside
selected sources/targets. Compare both hashes with `source_state.sha256`.
For bundle restore, source paths are managed temporary staging paths; retain
the verified bundle's checksums instead of trying to inspect cleaned staging.
Claim unchanged content only for the live sources or bundle bytes checked.

Record syntax acceptance separately for machine-readable targets. For JSON MCP,
run `python3 -m json.tool /resolved/target/file >/dev/null` on the actual written
file and retain its exit result; use a format-aware parser for JSONC or other
formats. Do not infer parsing success from `verify`.

For MCP, report the reviewed server additions, removals, and same-name
configuration changes alongside conversion/redaction losses. An empty
`loss_report` can accompany replacement of an existing server map. Compare
the applied server map and sibling settings with the reviewed preview and
pre-apply state to assess what was retained or replaced. See
[MCP migration](mcp-migration.md).

For a bundle, run `bundle-verify`; include its checksum/secret/binding result
and collection exclusions or failures. Authenticate the signer only with
`--trusted-key` from an independently trusted public-key file. An unsigned
bundle can pass integrity checks; `signature_verified: false` must remain
visible. `doctor` checks required executables on PATH and reports reauth/rebuild
work; success does not prove packages are installed or services are usable.
See [bundle-workflow.md](bundle-workflow.md).

## Rollback

Use the exact apply manifest with `rollback --manifest <manifest.json> --yes
--json` when the user has authorized undoing those changes. The guard refuses
to overwrite a target whose recorded post-apply hash no longer matches. If it
refuses, preserve that target and review the current change with its recorded
backup before proceeding.

After rollback, confirm existing targets match their recorded pre-apply hashes
(`target_state.sha256` in the saved plan, or `backup_sha256` in the manifest)
and newly created targets are absent. Repeat the source-content comparison.
Keep the manifest and backup paths as evidence. `verify` checks applied state,
so it is not a rollback acceptance check after applied targets have been removed
or restored to their previous contents.

## Product acceptance

File parsing proves syntax, not product discovery, transport compatibility,
credentials, OAuth, permissions, or connectivity. Use a documented native local
discovery panel or offline CLI when available and within scope. Do not launch
servers or connect to endpoints as part of this offline skill. State any
unperformed product/runtime acceptance; authentication and network checks need
their own authorization. For manual remote reconstruction, use
[mcp-transport.md](mcp-transport.md), not invented protocol headers.
