# Host software deployment

Use this reference when the requested DCC application needs installation or a
portable distribution. Start from the actual CLI build and its software
manifest. A source checkout, a software download entry, and a released adapter
catalog entry prove different things.

## Check the installed build

Record `dcc-mcp-cli --version`, then run the documented diagnostic commands:

```powershell
dcc-mcp-cli --output toon --no-auto-gateway host list
dcc-mcp-cli --output toon --no-auto-gateway host doctor <host-id>
```

Use the exact host identifier returned by `host list`. `host doctor` locates the
executable and invokes its version probe; it does not load an adapter,
register an MCP instance or prove an editing operation. A native version
process can initialize preferences or caches. For Inkscape, select a task-owned
`INKSCAPE_PROFILE_DIR` before that probe rather than using another workflow's
profile. This diagnostic process is distinct from the adapter lifecycle's
read-only Windows PE/hash probe.

If this CLI rejects `host`, preserve that result and record the build version.
Do not describe commands found only in newer source as installed capabilities.
An approved development build can exercise a reviewed source revision; record
its commit, binary hash and build commands separately from release evidence.
Updating the official binary follows the existing consent and verification
contract in [marketplace maintenance](MARKETPLACE_MAINTENANCE.md).

| Observation | Evidence boundary |
|---|---|
| `host list` software entry | This build knows how to detect or provision the application. |
| `host doctor` reports `available` | A discovered executable passed the requested version gate. |
| Host install receipt | A particular archive was downloaded, verified and installed. |
| `dcc-types` adapter catalog entry | The selected CLI catalog describes a DCC-MCP integration. |
| Live `list` row with required ready bits and ready dispatch | An exact registered instance is eligible for typed calls; a booting or unavailable diagnostic row is not. |
| Typed call plus authoritative readback | The requested native operation produced its observed effect. |

A software entry can exist without a public adapter. An absent adapter catalog
entry keeps integration support unknown; do not synthesize an
`install --dcc-type` plan from the software identifier. Follow
[zero-instance recovery](ZERO_INSTANCES_CLI.md) for adapter setup.

## Perform authorized installation

Read the selected manifest's version, platform channel, official HTTPS source,
license class and checksum provenance. The manifest's `open_source` or
`commercial` classification does not replace the upstream or bundled license
terms; verify the actual license before redistributing software. Confirm that
the available package really is the requested portable/archive distribution. Do not rename an installer as a
portable package or accept a new legal agreement on the user's behalf.

Downloading, installing and launching need user authorization. Carry out
existing explicit authorization for the same software, target and operation
without asking again. `--yes` applies to the approved invocation; it is not a
reason to change persistent consent, security settings or other installations.

For a reviewed CLI build containing the Windows Inkscape archive channel:

```powershell
# Task-owned absolute destination; use a process-local environment value.
$env:DCC_MCP_HOSTS_DIR = 'C:\vector-task\software'
$env:INKSCAPE_PROFILE_DIR = 'C:\vector-task\host-probe-profile'
dcc-mcp-cli --output toon --no-auto-gateway host doctor inkscape
# Run only after installation is authorized.
dcc-mcp-cli --output toon --no-auto-gateway host install inkscape --yes
dcc-mcp-cli --output toon --no-auto-gateway host doctor inkscape==1.4.4
```

These commands describe the coordinated development source, not a guarantee
that every published CLI contains this channel. The selected manifest supplies
the actual pin. `DCC_MCP_INKSCAPE_EXECUTABLE` is the host detector's explicit
executable override. The native vector runtime uses the separate
`DCC_MCP_INKSCAPE_EXE` variable; check the selected adapter's runbook rather
than assuming the two variables are interchangeable.

The archive channel verifies SHA-256 before extraction, stages the files and
rejects unsafe paths and links. ZIP uses the built-in extractor; 7z requires an
existing `7z` executable on `PATH`. Missing extraction support is a reported
dependency, not permission to fetch another installer or bypass validation.
The published directory includes `.dcc-mcp-install.json`; retain its source
URL, requested version, downloaded SHA-256 and CLI version. The Inkscape pin's
checksum provenance is the reviewed Scoop manifest; do not call it an upstream
signature or an independently published Inkscape checksum.

On a failed install command, retain the exit code, structured result and
redacted diagnostics, then use the scoped diagnostic version probe to establish current
state. A download alone is not an installation; a newly managed archive also
needs its successful receipt. Preserve an uncertain outcome rather than blindly
replaying the mutation. Route shared CLI failures through
[failure reporting](FAILURE_REPORTING.md); a repair follows the user's authorized
scope and needs its own regression and live check.

Keep task software, registry, output directory and any lock-file override
separate from another active workflow. Adapter installation, extension startup,
readiness and capability discovery remain separate steps. A host installation
does not start or enable an adapter automatically.

## Coordinated source references

The portable Inkscape channel and Windows archive handling are preserved at
source commit `8228335cb25fb9acfa53a67078850b1727de131e` in the closed, unmerged
[Core host deployment PR][core-host-pr]. They are historical development-source
evidence, not delivered Core main, CLI release or product-catalog support. Review that revision's
[CLI contract][core-cli] before using it. See [native vector workflow](NATIVE_VECTOR_WORKFLOW.md)
for the separate adapter workflow and its acceptance limits.

[core-host-pr]: https://github.com/dcc-mcp/dcc-mcp-core/pull/2652
[core-cli]: https://github.com/dcc-mcp/dcc-mcp-core/blob/8228335cb25fb9acfa53a67078850b1727de131e/docs/guide/cli-reference.md
