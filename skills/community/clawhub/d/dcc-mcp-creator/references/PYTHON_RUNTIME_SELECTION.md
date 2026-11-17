# Python runtime selection

Choose the runtime after the shared production-reuse gate and any relevant
template/license review. A reusable project does not establish interpreter
compatibility. Keep the task's existing evidence report for host probes,
selected versions, artifact identities and unresolved checks.

The companion [template-first catalog PR #38](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/pull/38)
adds candidate license evidence to that production workflow. Keep runtime
ownership decisions here independent of template adoption or catalog availability.

## Owners and public contracts

- **DCC-MCP Runtime / Python payload:** owned by
  [dcc-mcp-runtime](https://github.com/dcc-mcp/dcc-mcp-runtime). It owns the
  external CPython/Core/adapter payload contract for a versioned side-by-side
  root with isolated `lib/site-packages`. Verify actual release payload availability.
  Preserve that isolation; do not add
  global or host `site-packages`, rewrite `PYTHONPATH`, or bundle Python again
  per adapter. Select an existing compatible verified runtime version first.
  A documented layout does not prove an implemented dependency-isolation lifecycle.
- **Rust `dcc-mcp-sidecar`:** the transport/service companion managed through
  Core's lifecycle helpers; its executable is not a Python interpreter. Preserve
  the host/adapter ownership and stop rules in [Runtime integration](RUNTIME_INTEGRATION.md).
- **Gateway:** shared discovery/routing service, not the Python payload or the
  adapter's interpreter owner. A healthy gateway does not prove either is ready.

The reviewed Runtime source is
[`3a54f666c4283bab160dbab3ac90630c9ed39087`](https://github.com/dcc-mcp/dcc-mcp-runtime/tree/3a54f666c4283bab160dbab3ac90630c9ed39087).
Its package declares version `0.2.0`; the source example manifests still declare
`0.1.0`, a null runtime digest/signature and placeholder adapter hashes. These
files are contract examples, not verified release artifacts or installation plans.
Check the actual selected release; neither a version string nor this document
proves a payload is installed or approved.

## Default decision

Use the small, offline [decision example](examples/python_runtime_selection.py)
as an authoring template for already-collected facts. It does not discover,
install, import or start a runtime. Keep actual selection, manifest handling,
negotiation and lifecycle implementation in their existing owners.
`verified` requires the selected payload, launch/isolation contract and actual
interpreter/dependency probe to be verified; an accepted manifest handshake is
only `handshake_only`. The example selects an owner, not launch readiness, and
never emits `success` or `ready_for_launch`.

| Facts | Next step |
|---|---|
| Official JS/native bridge meets the task without Python | Use it; no Python payload is required. |
| Host Python exists and version, ABI and required dependencies are compatible | Use that host interpreter through the existing embedded adapter/dispatcher. |
| Host Python exists but is unknown or incompatible | Verify or repair the supported host profile; do not silently inject external CPython. |
| No host Python; adapter needs Python; shared Runtime is verified | Use that external runtime and the existing public handshake before registering the adapter. |
| No host Python; shared Runtime is missing or unverified | Produce installation preflight and an exact plan through the supported owner; obtain normal authorization before executing it. |
| Runtime/manifest/version mismatch, offline acquisition or denied authorization | Report the blocker; preserve the active version and never fall back to PATH Python, another download, per-adapter bundle or elevated permissions. |
| Only handshake acceptance, or missing payload/launch/isolation/probe evidence | Keep launch blocked and hand off the missing shared contract; do not treat negotiation as deployment. |

Probe the real host interpreter's version/ABI and dependency availability; do
not infer them from the desktop shell. Native Python 3.7 remains an existing
LTS profile. Do not raise its minimum version or import the external Runtime
package into it. Runtime's reviewed package declares Python >=3.9; verify its
actual published interpreter/ABI requirements separately from the embedded
adapter and from native-versus-lite Core acceptance.

## Preflight, negotiation and installation

1. Bind the selected runtime and adapter identities, versions, platform,
   architecture, Python ABI, Core compatibility and capability set. Use the
   existing Runtime manifest loader and handshake, not a second adapter parser.
2. Obtain manifests and artifacts from the selected trusted release. Verify
   non-placeholder digests, the operator's signature/trust policy and actual
   bytes before importing code or activation. `load_manifest` validates shape;
   `negotiate` checks ABI and Core contract equality. Neither verifies artifact
   integrity, signature authenticity or that the running version matches the
   plan. Keep those checks with the existing installer/operator trust owner.
3. In an already verified external runtime, the public bootstrap entry is:

   ```python
   from dcc_mcp_runtime.bootstrap import require_adapter

   handshake = require_adapter(adapter_id)  # Existing configured manifest identity.
   ```

   It reads `runtime/manifest.json` and `runtime/manifests/<adapter_id>.json`
   from the runtime root, optionally configured by `DCC_MCP_RUNTIME_ROOT`.
   The variable selects a location, not trust. Reuse the configured owner; do
   not mutate a live environment or retry a rejected handshake as embedded mode.
4. The public CLI at that source only exposes `validate-manifest`; there is
   no documented `install` or `upgrade` CLI verb. The existing `plan_install`
   API produces a typed plan with operation ID, runtime ID, exact target,
   package path/digest, confirmation and rollback version. Execution belongs
   to an authorized host-owned allow-list installer. If that installer,
   verified payload or required signature is unavailable, stop at preflight.
   Do not invent a downloader or installation command to fill the gap.
5. Reuse Core's [adapter install SOP work](https://github.com/dcc-mcp/dcc-mcp-core/issues/2252)
   and the supported install/upgrade/rollback route for the actual installed
   release. The issue is a contract/work tracker, not evidence that every verb
   ships. Preserve older-peer capability checks and existing lifecycle helpers.
   Activate only after integrity, health and capability verification; failed
   activation retains/restores the previous side-by-side version.

Source unit tests and offline decision examples are not real-host acceptance.
Verify the selected interpreter, native bridge, one typed operation and shutdown
in the real host before claiming usable integration. An offline or refused
installation stays blocked; source planning may continue without changing it.

## Figma integration case and shared-owner gaps

The existing Figma adapter is in the access-controlled
[`dcc-mcp-figma` draft PR #1](https://github.com/dcc-mcp/dcc-mcp-figma/pull/1),
reviewed at `6485de72bd17597c81080ceb1eb83924410625a1` against its
`docs/RUNTIME_INTEGRATION.md` and read-only preflight source. It is not merely
a local project. Its selected architecture uses external Python for the adapter
service and the official JavaScript Plugin API inside Figma, not injected Python.
Source/wheel/three-platform CI evidence is separate from native Figma acceptance.

The existing `python -m dcc_mcp_figma runtime-preflight` returns exit **2** when
`ready_for_launch` is false. Reported `runtime_package_unavailable` maps to
`shared_runtime="missing"` in the authoring example: plan/preflight only, with
normal authorization before installation through the supported shared owner.
It is not permission to install a package, start a process or search PATH.
No Figma preflight or host operation was rerun for this documentation change.

| Observed contract boundary | Creator decision / minimum shared deliverable |
|---|---|
| Package absent; no selected Runtime | Installation preflight, not an adapter-owned downloader or implicit pip/venv setup. Runtime owner must supply the supported acquisition and environment lifecycle. |
| Runtime 0.2.0 release assets are wheel/sdist, manifests and migration notes | Publish a trusted CPython payload with a versioned executable layout and supported process entry/launch plan; existing `validate-manifest` does not supply it. |
| No Figma adapter manifest, null runtime digest/signature, placeholder wheel digests | Publish exact signed/integrity-verifiable Runtime and Figma wheel manifests. Never fabricate a Figma manifest or substitute a capability fingerprint for integrity evidence. |
| Runtime Core requirement `>=0.19.13,<1.0.0` differs from Figma's `>=0.20.44,<0.21` | Current handshake compares strings for equality. Shared owner must implement a real compatible-version policy; do not widen Figma's actual requirement to make equality pass. |
| Package Python >=3.9 and manifest ABI `cp311-win_amd64` | Probe the actual selected interpreter, ABI, architecture, Core and native dependencies; package syntax support is not an observed payload ABI. |
| No supported isolated dependency lifecycle | Publish the shared isolated adapter dependency install/upgrade/rollback contract; a `lib/site-packages` path alone cannot prove isolation. |
| `runtime_handshake_accepted_launch_blocked` with accepted handshake | Map to `handshake_only`; preserve `success: false`, `ready_for_launch: false` and exit 2 until all launch evidence exists. |

Figma currently names the remaining gates
`trusted_runtime_payload_contract_missing`, `adapter_launch_contract_missing`
and `dependency_isolation_unverified`. The shared example also blocks on
`probe_unverified`, `payload_unverified`, `launch_unavailable` and
`isolation_unverified`. Keep each unresolved gate visible rather than converting
the first success into overall readiness. These are authoring/preflight facts,
not new Runtime API names.

Core's supported doctor/launch-plan interfaces may consume an explicitly
provided interpreter or an existing plan, but they do not create this missing
shared payload or authorize activation. Coordinate that work with the Runtime
owner and Core #2252; this Creator change supplies decision guidance and tests,
not those unimplemented contracts. No Runtime route grants Figma file/plugin,
loopback or credential permission, nor resolves a separate CUA input denial.
