# Native vector workflow

Use this workflow when the user asks to recreate or edit vector artwork in a
real application through DCC-MCP. Preserve the selected reference and software
provenance, create editable geometry through typed tools, and verify the saved
document and exports in the application.

## Resolve the reference and runtime

Find the current artwork in the owning brand or website repository. Inspect the
actual image and any editable source before treating historical descriptions
as the latest design. If competing versions cannot be resolved, return labeled
previews for the user's selection while continuing independent setup work.
Record the chosen reference's revision and hash. Recreating existing artwork
does not call for a new AI-generated replacement.

Inspect actual software, adapter inventory and capabilities. A host installer
entry does not prove a vector adapter exists. Follow
[host software deployment](HOST_SOFTWARE_DEPLOYMENT.md) when software setup is
needed. If the user authorized fixing capability gaps, implement and test the
smallest reusable typed extension in the owning repository and keep its review
and release status explicit.

The dedicated [Inkscape adapter][inkscape-readme] owns the Python package,
bundled skill and native effect. Read its [installation runbook][inkscape-install]
and [architecture contract][inkscape-architecture] at the reviewed source
revision. Its planned package version is source evidence until a verified
package release and catalog promotion exist. A standard package layout and a
successful software installation do not establish a released product route.

The [merged standard adapter source][inkscape-pr] uses a standalone Core MCP controller
with an Inkscape-hosted inkex effect. It does not embed the host interpreter or
provide persistent GUI document binding. Follow the dedicated adapter's pinned
contract for setup; merging source does not publish a package release.

## Native creation through typed operations

Inspect the adapter's current CLI and install report before executing its
runbook. Software deployment, Python package installation, private extension
installation and live service startup are separate steps. A source Git clone
verifies source files; it does not install or import the adapter package.

The adapter's plan-first `install`, `status`, `verify`, `uninstall` and `upgrade`
commands manage an explicit workspace's private profile and ownership receipt.
They do not download Inkscape or start a service/gateway. Keep `installed`,
`importable`, live readiness and `verify.directly_usable` independent. A partial
installation or unavailable readiness result needs its emitted startup/verify
steps, rather than repeated installation or a claim that native editing passed.
The initial lifecycle's host probe reads Windows PE version/hash data without
launching Inkscape; Linux/macOS lifecycle probing is reported as unsupported.
Actual software actions and native effects still need the `capabilities` and
document tools below.

Retain `readiness.version_source` from verification. A legacy registry with no
adapter version may use `adapter_ready_file` only after strict live UUID, PID,
workspace, profile, backend URL, ready status and package-version correlation.
An explicit conflicting registry version is rejected. A ready file alone is
not live readiness, and this compatibility path does not invent a registry or
Core version.

Configure an explicit executable and task-owned workspace. Select an isolated
registry and non-default gateway port, then use the adapter-owned foreground
`serve` entry point. Start only the task-owned service and gateway; do not
restart or reconfigure another session's shared gateway.

Inventory the task gateway, search for `native vector document`, and follow the
returned load/describe step. Copy the exact instance-qualified slug and current
schema. Keep `--require-gateway --agent-session-id <task-id>` on measured calls;
direct instance calls do not establish gateway statistics coverage.

The adapter exposes these local tool names. They are schema names, not slugs to
construct manually:

| Operation | Role |
|---|---|
| `capabilities` | Probe the configured binary, native actions and runtime limits. |
| `document_build` | Create an SVG from a bounded typed `plan` and relative `output_file`. |
| `document_export` | Export PNG, SVG or PDF through Inkscape; optionally convert text to paths. |
| `document_inspect` | Reopen the saved SVG with Inkscape and query native geometry. |
| `document_open` | Launch an owned GUI process for visual acceptance and return its PID. |

`plan` declares a canvas and typed nodes: layers, groups, paths, rectangles,
circles, ellipses, text and linear gradients. Child parents must be earlier
layers or groups. Use native path commands and local gradient references;
the protocol excludes arbitrary SVG/XML, external resources and executable
content. The exact schema and runtime validator are both authoritative.

The controller writes JSON requests and extension configuration. Inkscape
creates the blank document, invokes the native effect, commits its returned
document and saves it. This is the authoring boundary. Writing SVG in a separate
script and opening it afterward does not demonstrate native creation. Embedding
the reference bitmap in an SVG does not deliver editable vector artwork.

Use layers, named groups and editable objects in the master. Preserve an
editable text version where text exists, then use native `text_to_path` export
for a release copy. Retain both documents and inspect the resulting paths;
setting a filename suffix or declaring conversion intent is not conversion.
The adapter rejects existing output destinations rather than overwriting them.

Native text-to-path conversion can resolve live-text `currentColor` to a fixed
paint. Inspect the actual path fill and stroke before claiming dynamic CSS
color support. When CSS must control that token, read the software's
outlined glyph paths and submit them with explicit `currentColor` paint in a
new typed native plan, then export the new document through software. Keep the
editable text master and conversion/readback evidence. Do not patch the saved
SVG outside the native authoring route.

## Fonts and asset variants

Identify actual font files and license terms before attributing or redistributing
a font. An SVG `font_family` request alone does not prove which font rendered.
Confirm the renderer or fontconfig match. The adapter can add task-private font
directories through its optional configuration; it does not install system
fonts. Include required font license and attribution with redistributed files.
Keep software, font and artwork licenses distinct in the deliverable.

For a brand kit, author separate horizontal and square compositions, light and
dark background variants, and a monochrome `currentColor` SVG when requested.
Verify `currentColor` in its intended CSS context. Build separately simplified
small-icon plans: reduce fine lines, nodes and gaps, and adjust optical weight.
Exporting the full-size composition at 16 px is not optical simplification.

Export transparent PNGs through `document_export` with the intended dimensions
and `background_opacity: 0`. Verify actual pixel dimensions and alpha data.
Package Windows ICO and macOS ICNS from those exported PNGs in a separately
recorded container step. Ordinary packaging scripts may build containers,
manifests, hashes and archives; they do not replace native vector authoring or
software export. Validate the ICO/ICNS headers and embedded image sizes. A valid
ICNS file does not prove a macOS adapter or a native macOS rendering run.

## Evidence and acceptance

Preserve each discovery, load, describe and typed-call result plus its request,
trace and session identifiers. For a native build, the adapter records
`native_effect` with a correlated nonce, `extension_pid`, `parent_pid`,
`parent_executable`, `self_call`, `document_path` and `object_count`;
`host_invocation` records exact argv, host PID, return code and diagnostics.
Keep the output `sha256` and per-output evidence file. The controller validates
invocation correlation and expected native structure before publication.
These are local pipeline provenance checks, not cryptographic host attestation.

On Windows, `native_effect.provenance_mode: windows-glib-helper` requires the
exact three-process `windows_process_lineage`: native image identities, parent
PIDs and ordered creation/exit times must match the controller-owned Inkscape
process. The Windows controller launches only its fresh owned tree with
`DEBUG_PROCESS` and retains query-only process handles at native birth events,
before those processes execute. This covers helpers that can exit before the
extension's Python entry point. The retained host, helper and Python birth
identities must all cross-match the unchanged complete effect-reported chain;
`controller_birth_observation: exact-match` records that check. The extension's
early read-only parent handle is additional evidence, not a substitute for
missing birth identities. No existing process is attached, no privileges or
security settings change, and process memory/context is not read or changed.
Unreadable or unknown chains are rejected. Failed builds/exports retain invocation
`host.json` diagnostics even when the output is not published.

Run the adapter's source tests and its opt-in real-host regression on the actual
portable version. A mock extension response, a `--version` result or a PNG
fixture is not native build evidence. Platform-specific process-parent behavior
must pass on the target host; report a failure rather than weakening the check
to make the demonstration pass.

The [validated runtime checkpoint][inkscape-runtime-checkpoint] reports 374
local pure regressions with one optional native test deselected, plus a separate
actual Windows native component regression (`1 passed, 248 deselected`). Its
installed wheel was tested with Core 0.20.36, CLI/gateway 0.20.38 and Inkscape
1.4.4. Actual lifecycle verification returned directly usable with exit 0;
six successful gateway calls covered all five tools and recorded gateway
statistics. Native builds recorded exact birth-chain matches. Preserve the
historical failed request from the prior helper-retention implementation and
correlate any reconciled new request separately. This source revision changes
the runtime; earlier test-only source-equivalence claims do not apply. GUI
visual acceptance remains incomplete: `document_open` returned
`accepted=false`. Keep each case's actual call and visual evidence.

Reopen the saved master through `document_inspect`, then perform GUI acceptance
through `document_open` and the existing exact-process DCC-CUA/app-ui contract.
Inspect layers/groups, native geometry, text/path conversion, transparent edges,
light/dark rendering and each small icon at actual size. Headless reopen and a
GUI launch PID do not establish visual acceptance. A locked or unavailable
desktop leaves GUI QA incomplete even if native exports succeeded.

The adapter currently has Windows/Linux process-provenance logic; native macOS
execution is unvalidated. It has no persistent live GUI document binding.
Native operations are monolithic, and Core cancellation does not automatically
cancel the host; the operation timeout terminates only its owned process.
Disclose these limits with the observed results.

Retain exact paths, PIDs and diagnostics locally for reproducibility. Review and
redact machine names, absolute paths, unrelated session data and private artwork
before publishing a case. A public bundle can use artifact-relative paths,
hashes, versions and redacted call evidence. Include the editable master,
release vectors, raster exports, container outputs, licenses/attribution,
usage notes, manifest, QA results and reusable typed-plan instructions. Keep
delivery separate from replacing an active website or brand repository.

Native application references: [Inkscape CLI](https://wiki.inkscape.org/wiki/Using_the_Command_Line),
[historical script extension protocol](https://wiki.inkscape.org/wiki/Script_extensions),
[inkex documentation](https://inkscape.gitlab.io/extensions/documentation/).

[inkscape-pr]: https://github.com/dcc-mcp/dcc-mcp-inkscape/pull/1

[inkscape-readme]: https://github.com/dcc-mcp/dcc-mcp-inkscape/blob/fd5a71d4a59349f34b044aeec6244523137c3453/README.md
[inkscape-install]: https://github.com/dcc-mcp/dcc-mcp-inkscape/blob/fd5a71d4a59349f34b044aeec6244523137c3453/install.md
[inkscape-architecture]: https://github.com/dcc-mcp/dcc-mcp-inkscape/blob/fd5a71d4a59349f34b044aeec6244523137c3453/docs/architecture.md
[inkscape-runtime-checkpoint]: https://github.com/dcc-mcp/dcc-mcp-inkscape/commit/fd5a71d4a59349f34b044aeec6244523137c3453
