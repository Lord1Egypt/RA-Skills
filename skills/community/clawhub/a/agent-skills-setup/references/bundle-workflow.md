# Portable bundle, restore, and signing workflow

Read for computer switching, portable backups, ACB restore, dependency checks,
or signing. Commands below use `migrator=/path/to/agent-skills-setup/scripts/smart-ide-migration.sh`;
substitute the installed Skill path and requested source, target, workspace,
scopes, and artifact paths. Run each command independently and inspect its result.
Use [migration-safety.md](migration-safety.md) for authorization and conflict rules.

## Capture and inspect

`snapshot` writes an ACB **directory**, not a compressed archive. Name the source
and output explicitly; the CLI's fallback product selectors are examples, not
permission to inspect or restore those products.

```bash
bash "$migrator" snapshot --source cursor/ide --target cursor/ide \
    --workspace /path/to/project --scope project \
    --objects skills,instructions,mcp --output /path/to/project.acb --json
bash "$migrator" bundle-verify /path/to/project.acb --json
bash "$migrator" doctor /path/to/project.acb --json
```

Review `manifest.json`, the collection summary, `rebuild.json`, and
`secrets.required.json`. ACB contains portable object bytes, sanitized inventory,
compatibility evidence, requirements, reauthentication actions, and checksums
binding every declared file. Failed, excluded, or manual objects are not
automatically backed up; report them. Credential values and private runtime
state must remain outside the bundle.

`objects_captured` counts captured product/profile/scope object surfaces;
`files_captured` counts their payload files. Compare these with the manifest's
file bindings and collection exclusions rather than treating file count as
the number of Skills or servers. ACB payload limits are 5,000 files, 10 MiB per
file, 100 MiB total, and 16 directory levels. Known image/font assets are
allowed; executable or unallowlisted binary files fail collection instead of
silently disappearing. The exact extensions are `SAFE_BINARY_EXTENSIONS` in
[acb/bundle.py](../scripts/acb/bundle.py).

New snapshots record optional integer `files[].mode` permission bits (`0..0o777`)
in the checksummed manifest. On POSIX, restore and opt-in extraction apply these
bits to copied files, preserving text helper scripts' executable bits while
dropping setuid, setgid, and sticky flags. Payload storage permissions need not
match the source. Older mode-less bundles remain readable but cannot establish
original executable permissions; Windows applies only permissions supported by
its filesystem. Verify required target file modes separately from content
hashes; directory permissions and script execution are outside this guarantee.
Recorded modes apply to copied Skill/plugin files and extracted payloads.
Generated instruction, MCP, and handoff files use their target writer's
permissions; for example, generated MCP configuration is private (`0600`).

For a requested device-wide backup, run `detect` and review eligible profiles,
then use `snapshot --all-installed --scope user,project --output ...`.
`--include-configured` and `--include-compatibility` broaden eligibility to those
detection states only when the user wants them. Do not equate shared context
directories with installation proof. Prefer explicitly selected profiles when
device detection cannot establish the requested scope.

Plugins and handoff are opt-in objects, with both the object selector and flag:
`--objects plugins --include-plugins` or `--objects handoff --include-session`.
Package copying requires compatible registry surfaces and performs no install
or activation. Handoff transports only reviewed summary, branch, selected
relative files, and an explicit patch; raw session logs and state are excluded.
Apply the same opt-in flags during restore or saved-plan apply.

## Restore on the destination device

Inspect bundle integrity and run `doctor` before execution. Resolve source
selectors from the manifest and choose concrete destination profiles. Missing
tools or packages are manual installation work; this skill installs nothing.

`doctor` reports the complete recorded `requirements` and per-executable
`executable_checks` with `found_on_path`. It checks only executable presence;
`unresolved_requirements` retains missing executables plus the recorded
packages, extensions, `manual_installs` (including local script paths), and
platform notes. These other requirements are unverified and remain manual
work, alongside `reauth_actions` and `rebuild_actions`. Script paths and
platform notes are reported as recorded, without resolving new target paths
or probing product installation. No dependency is executed, imported,
installed, or contacted.

`ok: true` and exit 0 mean bundle integrity and executable-presence checks
passed; unresolved manual requirements do not change that result. Missing
executables produce `ok: false` and exit 1 while retaining the requirement
report. An invalid bundle produces exit 1 at `stage: verify` before its
requirements are reported. This status does not establish dependency or
product readiness.

```bash
bash "$migrator" restore /path/to/project.acb \
    --source cursor/ide --target cline/ide \
    --workspace /path/to/new-project --scope project \
    --objects skills,instructions,mcp --plan-only \
    --plan-out /path/to/restore-plan.json --json
bash "$migrator" restore /path/to/project.acb \
    --source cursor/ide --target cline/ide \
    --workspace /path/to/new-project --scope project \
    --objects skills,instructions,mcp --plan-in /path/to/restore-plan.json \
    --manifest-out /path/to/restore-manifest.json --yes --json
bash "$migrator" verify --manifest /path/to/restore-manifest.json --json
```

Check target paths, source content bindings, existing-target diffs, losses, and
rebuild actions in the saved plan before replay. Restore uses bundle sources and
destination-side states; local source installations do not replace the backup.
Bundle or destination drift requires a fresh plan. Saved-plan execution can
also use `apply <plan> --bundle <bundle> --yes`; trusted-signature verification
should be performed before that path. Use `restore --trusted-key` when signer
authentication must be enforced during restore itself.

New named restore plans record `bundle_source` (bundle ID and manifest SHA256)
and an `acb_uri` such as `acb://<bundle-id>#<object-id>` for each captured source,
alongside its temporary execution path. Named replay checks the verified
manifest's product, profile, scope, and object identity before target writes;
moving the bundle does not change that identity. Saved plan bytes and
`plan_sha256` stay unchanged during replay. Generic `apply` requires `--bundle`
for these plans. Older named plans without this metadata retain their existing
source-content and destination-state validation when supplied with a bundle.

For requested multi-product restore, use `--all-installed` in both planning and
replay, review per-target conflicts and failures, and retain the same scopes and
opt-ins. Apply writes only eligible targets. A bundle resolving no eligible
objects fails by default; `--allow-noop` is for an intentional review/no-op,
not evidence of restoration.

`--plan-only` avoids product writes but can save `--plan-out`. `--dry-run`
avoids persistent output writes. `--restore-root <dir>` explicitly extracts a
review tree and is unnecessary for ordinary restore; extraction is distinct
from installation into destination product surfaces.

## Sign and authenticate

Ed25519 key generation, signing, and signature checks need an already installed
Python `cryptography` package. If unavailable, report the missing dependency;
checksum verification and unsigned backup remain usable offline. Use fresh,
distinct key paths outside bundles and migration surfaces. Keep the private
32-byte raw key owner-only; distribute only the public key. Key generation uses
POSIX mode `0600` or a protected Windows ACL granting access only to the current
user. Signing checks those permissions before reading the private key and
rejects keys with broader access. Windows key storage must support file ACLs.

If generation fails after creating an output, inspect `outputs_requiring_review`
before retrying with fresh paths. POSIX outputs are preserved because a pathname
may have been replaced concurrently; never delete a listed path without checking
its current contents and ownership. Windows removes only files still bound to
the original held creation handles. Do not use a keypair from a failed operation.

```bash
bash "$migrator" bundle-keygen --out-private /path/to/private.key \
    --out-public /path/to/public.key --json
bash "$migrator" bundle-sign /path/to/project.acb \
    --key /path/to/private.key --signer local-operator --json
bash "$migrator" bundle-verify /path/to/project.acb \
    --trusted-key /path/to/public.key --json
```

Obtain the trusted public key independently of the bundle. `signature.json`
contains an embedded public key, which by itself does not establish trust.
Signing verifies bundle integrity before attestation; report signature
verification separately from checksums and dependency readiness. Preserve
existing keys and signed bundles unless the user authorizes replacing them.
