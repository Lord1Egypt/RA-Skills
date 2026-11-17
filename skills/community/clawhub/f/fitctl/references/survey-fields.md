# Survey field map (`host-survey.v2`, schema_version 2)

Field paths target fitctl-core 0.8.0 and Python bindings 0.1.1.
Root: `.survey` unless stated.

## Envelope / provenance (`.envelope`)

| Field | Meaning |
|---|---|
| `schema_id`, `schema_version`, `artifact_id` | artifact identity |
| `provenance.collected_at` | `unix:<seconds>` (live) or ISO Z (fixture) |
| `provenance.fitctl_version` | core release line that produced it |
| `provenance.source` | e.g. `live:linux_core_v1`, `fixture_corpus:...` |
| `provenance.command_name`, `correlation_id` | producing command, correlation |

## Collection context

| Field | Meaning |
|---|---|
| `.survey.collection_mode` | `live` or `replay` |
| `.survey.host_alias`, `.snapshot_id`, `.source_ref` | naming of snapshot |
| `.survey.core_evidence.execution_context.privilege_level` | e.g. `limited` |
| `.survey.core_evidence.execution_context.visibility_scope` | e.g. `bare_metal_like`, container scopes |
| `.survey.core_evidence.execution_context.container_runtime` | null outside containers |
| `.survey.core_evidence.identity_summary` | stable host identity + class |

## Observations (`.survey.core_evidence.observations.<name>`)

Every observation is `{"state": "observed"|..., "value": ...}`. A non-`observed`
state is missing evidence; never rewrite it as zero or absent hardware.

| Section | value fields |
|---|---|
| `cpu` | `model`, `architecture`, `logical_cores`, `physical_cores`, `threads_per_core`, `cache_summary` (representative instance sizes), `feature_flags` |
| `memory` | `total_bytes` only — capacity, not availability |
| `storage` | `block_devices` (names), `block_device_details` (name, class, removable), `mounts`, `mount_details` (path, filesystem_type, role) |
| `network` | `interfaces`, `interface_details` (addresses with family/prefix), `addressability_summary` (default_route_families, non_loopback_address_families) |
| `accelerators` | `devices` (vendor, model, family, pci_address, driver), `operability` (`static_operability`, `driver_bound_devices`, `visible_device_nodes`) |
| `topology` | `cpu_packages`, `numa_nodes` |
| `hostname` | string |

`operability.static_operability` is a static driver/node check — not runtime
health, memory, or utilisation.

## Coverage and gaps

| Field | Meaning |
|---|---|
| `.survey.core_evidence.collectors[]` | which collectors ran (`collector_id`, `source_family`) |
| `.survey.core_evidence.section_metadata.<section>` | `evidence_paths`, `assurance_source`, `derivation_stage` |

## What the survey never contains

Free/available memory, GPU utilisation, temperatures, load, network
throughput, or any fit verdict. Surveys MAY contain directly observed
static GPU memory/VRAM capacity (conservative, e.g. total per device from
an observable driver query) — that is capacity, never current
free/allocatable GPU memory. State artifacts and validation reports are
separate evidence kinds.
