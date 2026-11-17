# Packing Services (Service Configuration Guide)

> **This document** is the canonical packing reference for Nodo. It defines the
> input format `nodo pack` expects: the project layout, `pack_config.json`,
> `service.json`, and the `Dockerfile` rules. It was promoted here from
> `src/commands/packer/zip_with_dockerfile/README.md` so it is discoverable next
> to the other docs; that path now just points here. Linked from
> [`USAGE.md`](./USAGE.md) (the `pack` command) and the project `README.md`.

> **Where the build happens:** by default nodo does **not** build services
> locally. `nodo pack` sends your project archive to an external
> **packer-service** (a Celaut microVM that runs `docker buildx` inside a sealed
> VM, so Docker is never installed on your host) and imports the returned
> `.celaut.bee`. Reference the packer by its published service id under
> `core_services` in `config.yaml` — the single source of truth
> (`core_services: [{ name: "packer", id: "<id>" }]`). nodo launches an instance
> on demand if none is running (or reuses one you started with `nodo execute`) —
> nodo resolves that instance's `ip:port` automatically.
> When nodo needs to download the packer it uses `packer.PACKER_SOURCE_URL` if
> set, otherwise the source-application core service. Use
> `packer.PACKER_SERVICE_URL` only to override with an out-of-band packer.
>
> Setting `packer.local: true` in `config.yaml` switches to a **local** backend
> that builds on this host with nodo's own isolated Docker toolchain (provisioned
> on demand via `bash/install_docker.sh`, independent of any host Docker). Either
> way you author the `Dockerfile`/`service.json` exactly as described below — the
> `docker buildx` mechanics in *Service Preparation Process* run inside the
> packer-service microVM (default) or the isolated local toolchain (`packer.local`).

## Table of Contents
1. [Directory Structure](#directory-structure)
2. [Configuration Files](#configuration-files)
3. [pack_config.json - Complete Reference](#pack_configjson---complete-reference)
4. [service.json - Complete Reference](#servicejson---complete-reference)
5. [Dockerfile - Complete Reference](#dockerfile---complete-reference)
6. [Service Preparation Process](#service-preparation-process)
7. [Best Practices](#best-practices)
8. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Directory Structure

A service can be structured in two main ways:

### Option 1: Configuration in `.service` directory (Recommended)
```
my-service/
├── .service/
│   ├── Dockerfile
│   ├── service.json
│   ├── pack_config.json
│   └── .dockerignore
├── src/
│   └── app.py
├── tests/
│   └── test_app.py
├── requirements.txt
└── README.md
```

### Option 2: Root Configuration (Simple)
```
my-service/
├── Dockerfile
├── service.json
├── .dockerignore
├── src/
│   └── app.py
└── requirements.txt
```

> **Note:** When using Option 2, the script will automatically:
> 1. Create the `.service` directory
> 2. Copy `Dockerfile` and `service.json` to `.service`
> 3. Create a default `pack_config.json` with `{"ignore": []}`
> 4. Read `.dockerignore` and merge its lines into `pack_config.json → ignore`
>    (the file itself is not copied, so Docker never sees it)
>
> Both structures will end up properly organized in `.service` during the build process.

---

## Configuration Files

### Overview

| File | Required | Location | Purpose |
|------|----------|----------|---------|
| `pack_config.json` | No (auto-created) | `.service/` or root | Main build and packaging configuration |
| `Dockerfile` | Yes | `.service/` or root | Docker image build instructions |
| `service.json` | Yes | `.service/` or root | Service metadata and runtime configuration |
| `.dockerignore` | No | `.service/` or root | Docker build exclusions |

---

## pack_config.json - Complete Reference

The `pack_config.json` is the central configuration file that controls how your service is built and packaged.

### Full Example

```json
{
    "service_dependencies_directory": "__services__",
    "metadata_dependencies_directory": "__metadata__",
    "blocks_directory": "__block__",
    "zip": true,
    "ignore_loadable_protobuf": true,
    "dependencies": {
        "MY_DEP": "dependencies/my-dependency",
        "ANOTHER_DEP": "https://github.com/org/another-dep"
    },
    "dependencies_env": true,
    "include": [
        "protos",
        "src",
        "__init__.py",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "tests/",
        "*.pyc",
        "__pycache__",
        ".env"
    ]
}
```

---

### Configuration Options Reference

#### `include`
- **Type:** `array of strings`
- **Required:** No
- **Description:** Specifies exactly which files and directories to include in the build. When defined, **only** the listed items will be included. If omitted, all files (except those in `ignore`) will be included.

**Example — Including specific files and directories:**
```json
{
    "include": [
        "src",
        "protos",
        "__init__.py",
        "start.sh",
        "requirements.txt",
        ".service/pack_config.json"
    ]
}
```

> **Tip:** Use `include` when you want precise control over what goes into your package.

---

#### `ignore`
- **Type:** `array of strings`
- **Required:** No
- **Default:** `[]`
- **Description:** List of files or directory patterns to exclude from the build. Each pattern is matched **recursively** against every path under the packaged source directory, so a pattern like `*.pyc` or `__pycache__/` also removes nested matches (e.g. `src/foo.pyc`, `src/__pycache__/`). Matching is filename/glob based (via `rglob`), not a full re-implementation of the `.dockerignore` specification. Trailing slashes on directory patterns are tolerated, and blank lines, comments (`#`), and negation patterns (`!keep.txt`) are skipped. Patterns in `.dockerignore` are automatically merged into this list.

**Example:**
```json
{
    "ignore": [
        "tests/",
        "*.pyc",
        "__pycache__/",
        ".env",
        "*.md",
        ".git/"
    ]
}
```

> **Note:** `ignore` and `.dockerignore` patterns are merged automatically. Avoid duplicating patterns between both files.

---

#### `dependencies`
- **Type:** `object (dict)` or `array`
- **Required:** No
- **Description:** Specifies the service's dependencies and their source paths. Dependencies can be:
  - A **local path** relative to the project root
  - A **Git repository URL** (must contain `http`)
  - A **registry entry** (already packed service hash/identifier)

**Example — Dictionary format (recommended):**
```json
{
    "dependencies": {
        "REGRESSION_MODEL": "dependencies/regression_cnf",
        "DATA_GENERATOR": "dependencies/random_cnf_generator",
        "REMOTE_DEP": "https://github.com/my-org/my-dependency"
    }
}
```

**Example — Array format:**
```json
{
    "dependencies": [
        "dependencies/regression_cnf",
        "dependencies/random_cnf_generator"
    ]
}
```

> ⚠️ **Warning:** Array format cannot be used together with `dependencies_env: true`. Use dictionary format when environment variable mapping is required.

**Dependency resolution order:**
1. Check if the dependency exists in the **service registry** directly
2. If not found and the path contains `http` → treat as **Git URL**
3. If not found and no `http` → treat as **local path relative to project root**, and pack it on the fly

---

#### `dependencies_env`
- **Type:** `boolean`
- **Required:** No
- **Default:** `false`
- **Description:** When `true`, generates a `.dependencies` file inside the service package mapping each dependency key to its resolved identifier.

**Example:**
```json
{
    "dependencies": {
        "REGRESSION_MODEL": "dependencies/regression_cnf"
    },
    "dependencies_env": true
}
```

**Generated `.dependencies` file:**
```env
REGRESSION_MODEL=abc123hashvalue
DATA_GENERATOR=def456hashvalue
```

> **Note:** Requires `dependencies` to be a dictionary, not an array.

---

#### `service_dependencies_directory`
- **Type:** `string`
- **Required:** No (required if `dependencies` is defined)
- **Description:** Directory name inside the package where service dependencies will be copied.

```json
{
    "service_dependencies_directory": "__services__"
}
```

---

#### `metadata_dependencies_directory`
- **Type:** `string`
- **Required:** No
- **Description:** Directory name inside the package where metadata files associated with dependencies will be stored.

```json
{
    "metadata_dependencies_directory": "__metadata__"
}
```

---

#### `blocks_directory`
- **Type:** `string`
- **Required:** No
- **Description:** Directory name where block files referenced by dependencies will be stored. Blocks are resolved automatically from each dependency's `_.json` manifest.

```json
{
    "blocks_directory": "__block__"
}
```

---

#### `zip`
- **Type:** `boolean`
- **Required:** No
- **Default:** `false`
- **Description:** When `true`, compresses the dependency directories into a single `services.zip` file and removes the originals.

**With `zip: true`:**
```
service/
├── src/
├── services.zip   ← Contains __services__, __metadata__, __block__
└── start.sh
```

**With `zip: false`:**
```
service/
├── src/
├── __services__/
├── __metadata__/
├── __block__/
└── start.sh
```

---

#### `ignore_loadable_protobuf`
- **Type:** `boolean`
- **Required:** No
- **Default:** `false`
- **Description:** When `true`, the `wbp.bin` file (compiled protobuf binary) is removed from each dependency after it is copied into the package.

```json
{
    "ignore_loadable_protobuf": true
}
```

| Scenario | Recommended Value |
|----------|-------------------|
| You need the full compiled protobuf in dependencies | `false` (default) |
| You want to reduce package size | `true` |
| The consuming service recompiles protobufs | `true` |

---

### Complete pack_config.json Examples

#### Minimal (no dependencies)
```json
{
    "ignore": ["tests/", "*.pyc", "__pycache__/"]
}
```

#### Service with local dependencies
```json
{
    "service_dependencies_directory": "__services__",
    "metadata_dependencies_directory": "__metadata__",
    "blocks_directory": "__block__",
    "dependencies": {
        "REGRESSION": "dependencies/regression_cnf",
        "RANDOM": "dependencies/random_cnf_generator"
    },
    "dependencies_env": true,
    "include": ["src", "start.sh", ".service/pack_config.json"]
}
```

#### Service with remote dependencies, zipping and protobuf stripping
```json
{
    "service_dependencies_directory": "__services__",
    "metadata_dependencies_directory": "__metadata__",
    "blocks_directory": "__block__",
    "zip": true,
    "ignore_loadable_protobuf": true,
    "dependencies": {
        "MODEL_SERVICE": "https://github.com/my-org/model-service",
        "DATA_SERVICE": "https://github.com/my-org/data-service"
    },
    "dependencies_env": true,
    "include": ["protos", "src", "__init__.py", "start.sh", ".service/pack_config.json"],
    "ignore": ["tests/", "*.pyc", "__pycache__/"]
}
```

---

## service.json - Complete Reference

The `service.json` file defines **runtime metadata** for the service: its architecture, resource requirements, entrypoint, API slots, network configuration, and environment variables. This file is parsed by the packer to build the `celaut` protobuf specification.

### Full Example

```json
{
    "tag": "my-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 52428800,
            "disk_space": 1073741824,
            "cpu_period": 100000,
            "cpu_quota": 50000,
            "blkio_weight": 100
        },
        "at_most": {
            "mem_limit": 524288000,
            "disk_space": 5368709120,
            "cpu_period": 100000,
            "cpu_quota": 200000,
            "blkio_weight": 500
        }
    },
    "init": {
        "entry_path": ["usr", "local", "bin", "start.sh"],
        "xattrs": {
            "custom.flag": "enabled"
        }
    },
    "config_declaration": {
        "path": ["__config__"]
    },
    "api": [
        {
            "port": 8080,
            "transport": "tcp",
            "protocol": ["grpc"],
            "gas_amount_per_call": {
                "MyMethod": 100,
                "HeavyMethod": 500
            }
        }
    ],
    "envs": ["MY_ENV_VAR"],
    "network": [
        {
            "tags": ["ipv4", "public"],
            "prose": "Public IPv4 network access"
        }
    ],
    "possible_environment_workload": [
        {
            "workloads": [
                {
                    "count": 2,
                    "resources": { "mem_limit": 536870912 },
                    "dependency": {
                        "hash": [
                            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
                        ]
                    }
                }
            ]
        }
    ]
}
```

---

### service.json Fields Reference

#### `tag`
- **Type:** `string` or `array of strings`
- **Required:** No
- **Description:** Human-readable name(s) for the service. Used as metadata tags for identification. Does not affect runtime behaviour.

```json
{ "tag": "my-awesome-service" }
```
```json
{ "tag": ["my-service", "v2", "stable"] }
```

---

#### `architecture`
- **Type:** `string`
- **Required:** Yes
- **Description:** Target platform architecture for the Docker build. Must match one of the supported architectures configured in the packer.

| Common values | Description |
|---------------|-------------|
| `linux/amd64` | 64-bit x86 Linux |
| `linux/arm64` | 64-bit ARM Linux |
| `linux/arm/v7` | 32-bit ARM Linux |

```json
{ "architecture": "linux/amd64" }
```

> ⚠️ **The architecture must match the host machine running the packer**, unless cross-compilation is explicitly supported and configured. If the architecture is not supported or does not match, the packer will raise an error and abort.

---

#### `resources`
- **Type:** `object`
- **Required:** No
- **Description:** Defines resource constraints for the service container. Contains two sub-objects:
  - `at_init`: Resources allocated when the service starts
  - `at_most`: Maximum resources the service can use

> `at_most` values are automatically clamped to be **at least as high** as `at_init` values.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `mem_limit` | int (bytes) | `10_000_000` (10 MB) | Memory limit |
| `disk_space` | int (bytes) | `2_000_000_000` (2 GB) | Disk space limit |
| `cpu_period` | int (microseconds) | `0` (no limit) | CPU CFS period |
| `cpu_quota` | int (microseconds) | `0` (no limit) | CPU CFS quota |
| `blkio_weight` | int | `0` (no limit) | Block I/O weight |

> A value of `0` means **no limit** for that resource.

**Example — Constrained service:**
```json
{
    "resources": {
        "at_init": {
            "mem_limit": 52428800,
            "disk_space": 1073741824,
            "cpu_period": 100000,
            "cpu_quota": 25000
        },
        "at_most": {
            "mem_limit": 209715200,
            "disk_space": 5368709120,
            "cpu_period": 100000,
            "cpu_quota": 100000
        }
    }
}
```

**Example — Unlimited resources (development):**
```json
{
    "resources": {
        "at_init": {},
        "at_most": {}
    }
}
```

---

#### `possible_environment_workload`
- **Type:** `array` of objects
- **Required:** No
- **Description:** Declares the **worst-case descendant workloads** the service may request during its lifetime (a service can spawn child services locally or on other peers). It exists for scheduling admission decisions — *can the network satisfy any execution this service could trigger?* Unlike `resources` (this instance's own needs), `possible_environment_workload` describes its **descendants**. Serialized directly to `Service.possible_environment_workload`, outside `Service.Container`.
- Each array entry is **one independent concurrent execution scenario**. Scenarios are **not cumulative** and imply **no temporal ordering**; a scheduler only needs to check whether each scenario, in isolation, could be satisfied.
- Each scenario has a `workloads` array; each item groups identical concurrent descendants:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | int | `1` | Number of concurrent descendant instances in this group |
| `resources` | object (`Sysresources`) | `{}` | Resources each of those descendants may require (`mem_limit`, `disk_space`, `cpu_period`, `cpu_quota`, `blkio_weight`; bytes / microseconds; `0` = no limit) |
| `dependency` | object or `null` | omitted | Optional identity, embedded specification, and availability information for the descendant service |

##### `workloads[].dependency`

Every dependency field is optional, but a non-null dependency object must contain at least
one `hash` or an embedded `service`:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `hash` | array | `[]` | Known content hashes. A string is a SHA3-256 digest in hexadecimal. Object form is `{ "type": "sha3_256", "value": "<hex>" }`; `type` also accepts another configured hash name or hash-id hex. |
| `service` | object | omitted | Full or partial embedded `celaut.Service`, using protobuf JSON structure. For example, resources are under `container.resources`. |
| `is_completed` | bool | `false` | `true` asserts that the embedded `service` is complete and can be checked against the declared hashes. Requires `service`. |
| `on_filesystem` | bool | `false` | `true` declares that the complete dependency artifact is already stored in this service's filesystem (for example as a `.celaut.bee`). This does not copy it automatically; use the existing `pack_config.json` dependency flow to place the artifact in the filesystem. |

`dependency: null` and an omitted `dependency` both leave the protobuf message absent.
The booleans are independent: a service may be embedded, stored on the filesystem, both, or
neither. The packer serializes these declarations; scheduler/runtime enforcement remains
future work.

**Hash-only dependency — resolve by content identity:**

```json
{
    "count": 1,
    "resources": { "mem_limit": 536870912 },
    "dependency": {
        "hash": [
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        ]
    }
}
```

**Filesystem-backed dependency:**

```json
{
    "count": 1,
    "resources": { "mem_limit": 536870912 },
    "dependency": {
        "hash": [
            { "type": "sha3_256", "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef" }
        ],
        "on_filesystem": true
    }
}
```

**Partial service projection — scheduler-relevant fields only:**

```json
{
    "count": 1,
    "resources": { "mem_limit": 536870912 },
    "dependency": {
        "hash": ["0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"],
        "service": {
            "container": {
                "resources": {
                    "at_init": { "mem_limit": 536870912 },
                    "at_most": { "mem_limit": 1073741824 }
                }
            },
            "possible_environment_workload": [
                {
                    "workloads": [
                        {
                            "count": 2,
                            "resources": { "mem_limit": 268435456 },
                            "dependency": null
                        }
                    ]
                }
            ]
        },
        "is_completed": false
    }
}
```

**Complete service embedded in the parent specification:**

```json
{
    "count": 1,
    "resources": { "mem_limit": 536870912 },
    "dependency": {
        "hash": ["0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"],
        "service": {
            "prose": "Complete dependency specification",
            "container": {
                "architecture": { "tags": ["linux/amd64"] },
                "filesystem": "<base64 protobuf bytes>",
                "init": { "entry_path": ["service", "start"] },
                "resources": {
                    "at_init": { "mem_limit": 536870912 },
                    "at_most": { "mem_limit": 1073741824 }
                }
            }
        },
        "is_completed": true,
        "on_filesystem": false
    }
}
```

The special `dependency.hash` values are hexadecimal for operator convenience. Other
protobuf `bytes` fields inside `dependency.service` (such as `container.filesystem`) use
standard protobuf JSON base64 encoding.

> **Spec-only:** the field is declared and serialized, but nodo's scheduler does **not** yet interpret or enforce it. Scheduler interpretation is future work (celaut-project/nodo#163).

**Example — two independent scenarios (`2×5 GB + 1×40 GB`, or `4×16 GB`):**
```json
{
    "possible_environment_workload": [
        {
            "workloads": [
                {
                    "count": 2,
                    "resources": { "mem_limit": 5000000000 },
                    "dependency": {
                        "hash": ["0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"]
                    }
                },
                {
                    "count": 1,
                    "resources": { "mem_limit": 40000000000 },
                    "dependency": {
                        "service": {
                            "container": {
                                "resources": {
                                    "at_init": { "mem_limit": 40000000000 },
                                    "at_most": { "mem_limit": 48000000000 }
                                }
                            }
                        }
                    }
                }
            ]
        },
        {
            "workloads": [
                { "count": 4, "resources": { "mem_limit": 16000000000 } }
            ]
        }
    ]
}
```

---

#### `init`
- **Type:** `object`
- **Required:** No
- **Description:** Defines the container entrypoint and optional extended attributes.

| Field | Type | Description |
|-------|------|-------------|
| `entry_path` | `string` or `array` | Path segments to the entrypoint binary or script |
| `xattrs` | `object` | Key-value extended attributes passed to the container init |

**`entry_path` formats — all equivalent:**
```json
{ "init": { "entry_path": "usr/local/bin/start.sh" } }
{ "init": { "entry_path": ["usr", "local", "bin", "start.sh"] } }
{ "init": { "entry_path": "/usr/local/bin/start.sh" } }
```

> Path segments are normalized automatically: leading/trailing slashes are stripped and the path is split into individual components. All three formats above produce the same result: `["usr", "local", "bin", "start.sh"]`.

> ⚠️ **Packs fine, but never runs without it.** Only `architecture` is a hard requirement for *packing* — a service with no `init.entry_path` packs successfully. But at runtime `resolve_entrypoint_path` raises `entry_path is empty.`, so the service can **never** start. Always set `init.entry_path`.
>
> **`entry_path` constraints** (enforced at runtime): it must be a **single** path — no whitespace, no `.` or `..` segments, and no CLI arguments appended (the entry path is a path only, not a command line). Put any flags or arguments inside your entrypoint script instead.

**Example — With xattrs:**
```json
{
    "init": {
        "entry_path": ["usr", "local", "bin", "myservice"],
        "xattrs": {
            "exec.mode": "daemon",
            "custom.flag": "enabled"
        }
    }
}
```

**Legacy compatibility — `entrypoint` field:**

The older `entrypoint` top-level field is still supported and will be automatically mapped to `init.entry_path` if `init` is not defined:

```json
{ "entrypoint": "/usr/local/bin/start.sh" }
```

> ⚠️ The `entrypoint` field is deprecated. Use `init.entry_path` in new services.

---

#### `config_declaration`
- **Type:** `object`
- **Required:** No
- **Default:** `{"path": ["__config__"]}`
- **Description:** Declares the path inside the container filesystem where the service expects to find its runtime configuration.

```json
{
    "config_declaration": {
        "path": ["__config__"]
    }
}
```

```json
{
    "config_declaration": {
        "path": ["etc", "myservice", "config"]
    }
}
```

---

#### `api`
- **Type:** `array of objects`
- **Required:** No
- **Description:** Declares the API slots (ports) exposed by the service, along with their transport protocol, application protocol stack, and gas cost per method call.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `port` | int | Yes | Port number the service listens on |
| `transport` | string or array | No | Transport protocol(s). Defaults to `["tcp"]` |
| `protocol` | array | No | Application-level protocol tags (e.g. `["grpc"]`). Accepts `None` if omitted |
| `gas_amount_per_call` | object | No | Map of method name → gas cost (integer) |

**Example — Single gRPC slot:**
```json
{
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"],
            "gas_amount_per_call": {
                "Solve": 100,
                "SolveStream": 200
            }
        }
    ]
}
```

**Example — Multiple slots with different protocols:**
```json
{
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"]
        },
        {
            "port": 8080,
            "transport": ["tcp", "http"],
            "protocol": ["rest", "http1.1"]
        }
    ]
}
```

---

#### `envs`
- **Type:** `array of strings`
- **Required:** No
- **Description:** List of environment variable **names** the service declares. This is a names-only declaration.

```json
{
    "envs": ["MY_ENV_VAR", "ANOTHER_ENV"]
}
```

> **Note:** Per-variable `<name>.field` descriptors are **not** currently embedded. There is no target field for them in the packed schema (`pack.proto`'s `Container` has no `environment_variables` field), so the packer records the names only. Embedding descriptors would require adding that field to `pack.proto` first.

---

#### `network`
- **Type:** `array of objects`
- **Required:** No
- **Description:** Declares the network access requirements of the service.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tags` | array of strings | Yes | Network type identifiers. Required when a `network` entry is present — omitting it raises `KeyError` |
| `prose` | string | Yes | Human-readable description of the network requirement. Required when a `network` entry is present — omitting it raises `KeyError` |

```json
{
    "network": [
        {
            "tags": ["ipv4", "public"],
            "prose": "Requires public internet access to reach external APIs"
        },
        {
            "tags": ["ipv4", "private"],
            "prose": "Requires access to internal cluster network"
        }
    ]
}
```

---

### Complete service.json Examples

#### Minimal — Simple service, no API
```json
{
    "tag": "my-worker",
    "architecture": "linux/amd64",
    "init": {
        "entry_path": ["usr", "local", "bin", "worker"]
    }
}
```

#### Standard gRPC service
```json
{
    "tag": "solver-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 104857600,
            "disk_space": 2147483648
        },
        "at_most": {
            "mem_limit": 524288000,
            "disk_space": 10737418240
        }
    },
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"],
            "gas_amount_per_call": {
                "Solve": 100
            }
        }
    ]
}
```

#### Full-featured service
```json
{
    "tag": ["ml-inference", "v3"],
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 536870912,
            "disk_space": 10737418240,
            "cpu_period": 100000,
            "cpu_quota": 50000,
            "blkio_weight": 200
        },
        "at_most": {
            "mem_limit": 2147483648,
            "disk_space": 53687091200,
            "cpu_period": 100000,
            "cpu_quota": 200000,
            "blkio_weight": 700
        }
    },
    "init": {
        "entry_path": ["usr", "local", "bin", "serve"],
        "xattrs": {
            "runtime.mode": "production"
        }
    },
    "config_declaration": {
        "path": ["etc", "mlservice", "config"]
    },
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"],
            "gas_amount_per_call": {
                "Predict": 150,
                "BatchPredict": 600
            }
        }
    ],
    "envs": ["MODEL_VERSION", "DATASET_ID"],
    "network": [
        {
            "tags": ["ipv4", "private"],
            "prose": "Access to internal model registry"
        }
    ]
}
```

---

## Dockerfile - Complete Reference

The Dockerfile plays a critical role in the service packing process. Unlike a typical Docker deployment where the image is run directly, here **the Docker build is used solely to produce a filesystem snapshot** — the container is never actually run. The packer uses `docker buildx build` with `--output type=tar` to export the full filesystem of the built image, which is then parsed, hashed, and stored as the service specification.

### How the Dockerfile is Used

```
Dockerfile
    │
    ▼
docker buildx build
--platform <architecture>    ← from service.json "architecture"
--output type=tar,dest=...   ← exports raw filesystem, not an image
    │
    ▼
filesystem.tar
    │
    ▼
Extracted to: CACHE/<aux_id>/filesystem/
    │
    ▼
Parsed recursively into celaut.Service.Container.Filesystem protobuf
    │
    ├── Small files → embedded directly as bytes
    └── Large files → stored as blocks (referenced by hash)
```

> **Key insight:** The Dockerfile is not used to define a running container — it is used to **construct a filesystem**. Everything that ends up in the image's filesystem will be part of the service specification. The entrypoint, ports, environment variables, and resource limits are all defined in `service.json`, not in the Dockerfile.

---

### What to Put in the Dockerfile

The Dockerfile should:
- Install all runtime dependencies
- Copy the service source code and assets
- Set up the filesystem so the entrypoint defined in `service.json → init.entry_path` is executable and in place

The Dockerfile should **not**:
- Define `CMD` or `ENTRYPOINT` (these are ignored — entrypoint is read from `service.json`)
- Expose ports with `EXPOSE` (ports are defined in `service.json → api`)
- Define `ENV` for runtime configuration (declare variable names with `service.json → envs`)

---

### COPY Path Adjustment

During preparation the `.service/Dockerfile` **always** has its `COPY` paths rewritten (this applies whether the Dockerfile started at the project root or was already in `.service/`). Any `COPY` origin that starts with `.` is adjusted by prefixing it with `service/`:

```dockerfile
# Original Dockerfile (at project root)
COPY ./src /app/src
COPY ./requirements.txt /app/

# After preparation (moved to .service/, paths adjusted)
COPY service/src /app/src
COPY service/requirements.txt /app/
```

This happens because the Docker build context is set to `.service/`, where the `service/` directory contains the packaged project files.

> ⚠️ The rewrite applies to any origin starting with `.` (so `./src` and `.env` — which becomes `serviceenv` — are affected), **except** `--from=` origins in multi-stage builds. Absolute paths and URLs are left unchanged.
>
> ⚠️ A bare relative origin **without** a leading `./` (e.g. `COPY src /app`) is **not** adjusted. Because the build context is `.service/` and the project files live under `service/`, such a path will break the build. Always write project-relative `COPY` origins with a `./` prefix.

---

### Dockerfile Examples

#### Example 1 — Simple Python service
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./start.sh /app/start.sh

RUN chmod +x /app/start.sh
```

Paired `service.json`:
```json
{
    "tag": "my-python-service",
    "architecture": "linux/amd64",
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"]
        }
    ]
}
```

---

#### Example 2 — Multi-stage build to minimize filesystem size
```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /build
COPY ./requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage — only the final stage's filesystem is exported
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY ./src /app/src
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh
```

> **Tip:** Multi-stage builds are highly recommended. Only the **final stage** is exported as the filesystem. Use intermediate stages to compile, install, or build without including build tools in the final service package.

---

#### Example 3 — C/Go compiled binary service
```dockerfile
# Build stage
FROM golang:1.22 AS builder
WORKDIR /src
COPY ./src /src
RUN go build -o /out/myservice ./cmd/myservice

# Minimal runtime image
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /out/myservice /app/myservice
RUN chmod +x /app/myservice
```

Paired `service.json`:
```json
{
    "tag": "my-go-service",
    "architecture": "linux/amd64",
    "init": {
        "entry_path": ["app", "myservice"]
    }
}
```

---

#### Example 4 — Service with internal dependencies already packed into the filesystem
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./start.sh /app/start.sh

# Include dependency directory inside the filesystem
# (as packed by pack_config.json into __services__)
COPY ./__services__ /app/__services__
COPY ./__metadata__ /app/__metadata__

RUN chmod +x /app/start.sh
```

---

Agrega esta sección al README, después de los ejemplos de Dockerfile existentes:

---

### Dockerfile Examples by Language / Framework

---

#### Java (Spring Boot)

```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /build
COPY ./pom.xml .
# Download dependencies first (layer caching)
RUN mvn dependency:go-offline -B
COPY ./src ./src
RUN mvn package -DskipTests -B

# Runtime stage
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=builder /build/target/*.jar /app/app.jar
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh
```

`start.sh`:
```bash
#!/bin/sh
exec java \
  -XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0 \
  -jar /app/app.jar
```

`service.json`:
```json
{
    "tag": "my-spring-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 268435456,
            "disk_space": 2147483648,
            "cpu_period": 100000,
            "cpu_quota": 50000
        },
        "at_most": {
            "mem_limit": 1073741824,
            "disk_space": 5368709120,
            "cpu_period": 100000,
            "cpu_quota": 200000
        }
    },
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 8080,
            "transport": "tcp",
            "protocol": ["http1.1", "rest"],
            "gas_amount_per_call": {
                "POST /solve": 100,
                "GET /status": 10
            }
        }
    ]
}
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "pom.xml",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "target/",
        "*.md",
        ".mvn/",
        "**/*.class"
    ]
}
```

> **Note:** The JAR is assembled inside the Docker build stage — you do **not** need to include compiled artifacts in `pack_config.json`. Only source files and the startup script are needed.

---

#### Java (Gradle)

```dockerfile
# Build stage
FROM gradle:8.7-jdk21 AS builder
WORKDIR /build
# Copy only gradle files first for dependency caching
COPY ./build.gradle.kts ./settings.gradle.kts ./
COPY ./gradle ./gradle
RUN gradle dependencies --no-daemon
COPY ./src ./src
RUN gradle bootJar --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=builder /build/build/libs/*.jar /app/app.jar
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "build.gradle.kts",
        "settings.gradle.kts",
        "gradle",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "build/",
        ".gradle/",
        "*.md"
    ]
}
```

---

#### PHP / Laravel

```dockerfile
# Build stage — install Composer dependencies
FROM composer:2.7 AS composer
WORKDIR /app
COPY ./composer.json ./composer.lock ./
RUN composer install \
    --no-dev \
    --no-scripts \
    --no-autoloader \
    --prefer-dist \
    --ignore-platform-reqs
COPY ./src ./src
RUN composer dump-autoload --optimize --no-dev

# Runtime stage
FROM php:8.3-fpm-alpine

# Install required PHP extensions
RUN apk add --no-cache \
        libpng-dev \
        libjpeg-turbo-dev \
        libwebp-dev \
        oniguruma-dev \
        libxml2-dev \
        zip \
        unzip \
    && docker-php-ext-install \
        pdo \
        pdo_mysql \
        mbstring \
        xml \
        pcntl \
        bcmath

WORKDIR /var/www

# Copy app source
COPY --from=composer /app/vendor ./vendor
COPY ./src /var/www
COPY ./start.sh /var/www/start.sh

RUN chmod +x /var/www/start.sh \
    && chown -R www-data:www-data /var/www/storage \
    && chown -R www-data:www-data /var/www/bootstrap/cache
```

`start.sh`:
```bash
#!/bin/sh
set -e

# Run Laravel migrations on startup
php /var/www/artisan migrate --force

# Start PHP-FPM
exec php-fpm
```

`service.json`:
```json
{
    "tag": "my-laravel-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 134217728,
            "disk_space": 2147483648
        },
        "at_most": {
            "mem_limit": 536870912,
            "disk_space": 10737418240
        }
    },
    "init": {
        "entry_path": ["var", "www", "start.sh"]
    },
    "api": [
        {
            "port": 9000,
            "transport": "tcp",
            "protocol": ["fastcgi"],
            "gas_amount_per_call": {
                "request": 50
            }
        }
    ]
}
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "composer.json",
        "composer.lock",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "vendor/",
        "node_modules/",
        "tests/",
        "*.md",
        ".env",
        ".env.*",
        "storage/logs/*",
        "storage/framework/cache/*"
    ]
}
```

> **Important:** Never include `.env` files in the package. Laravel environment configuration should be injected at runtime via the service configuration mechanism (declare variable names with `service.json → envs`).

---

#### Rust

```dockerfile
# Build stage
FROM rust:1.78-slim AS builder
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache dependencies by building only the dependency graph first
COPY ./Cargo.toml ./Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Build actual source
COPY ./src ./src
# Touch main.rs to force rebuild
RUN touch src/main.rs
RUN cargo build --release

# Runtime stage — minimal image
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/target/release/myservice /app/myservice
COPY ./start.sh /app/start.sh
RUN chmod +x /app/myservice /app/start.sh
```

`start.sh`:
```bash
#!/bin/sh
exec /app/myservice
```

`service.json`:
```json
{
    "tag": "my-rust-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 33554432,
            "disk_space": 536870912,
            "cpu_period": 100000,
            "cpu_quota": 50000
        },
        "at_most": {
            "mem_limit": 268435456,
            "disk_space": 2147483648,
            "cpu_period": 100000,
            "cpu_quota": 400000
        }
    },
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 50051,
            "transport": "tcp",
            "protocol": ["grpc"],
            "gas_amount_per_call": {
                "Process": 75,
                "ProcessStream": 150
            }
        }
    ]
}
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "Cargo.toml",
        "Cargo.lock",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "target/",
        "tests/",
        "benches/",
        "*.md",
        ".env"
    ]
}
```

> **Tip:** The Rust binary produced in the build stage is fully self-contained (statically linked against musl libc if you use `rust:alpine` as the builder). For even smaller images, use `FROM scratch` as the runtime stage if your binary is fully static:
>
> ```dockerfile
> FROM rust:1.78-alpine AS builder
> RUN apk add --no-cache musl-dev
> WORKDIR /build
> COPY ./Cargo.toml ./Cargo.lock ./
> RUN mkdir src && echo "fn main() {}" > src/main.rs
> RUN cargo build --release --target x86_64-unknown-linux-musl
> RUN rm -rf src
> COPY ./src ./src
> RUN touch src/main.rs
> RUN cargo build --release --target x86_64-unknown-linux-musl
>
> # Completely empty filesystem — only your binary
> FROM scratch
> COPY --from=builder /build/target/x86_64-unknown-linux-musl/release/myservice /myservice
> ```
>
> `service.json` entry_path in this case:
> ```json
> { "init": { "entry_path": ["myservice"] } }
> ```

---

#### Node.js (Express / generic)

```dockerfile
# Build stage — install and prune dependencies
FROM node:22-alpine AS builder
WORKDIR /build
COPY ./package.json ./package-lock.json ./
RUN npm ci --omit=dev

# Runtime stage
FROM node:22-alpine
WORKDIR /app

# Copy pruned node_modules from builder
COPY --from=builder /build/node_modules ./node_modules

# Copy application source
COPY ./src ./src
COPY ./package.json ./
COPY ./start.sh ./start.sh

RUN chmod +x /app/start.sh
```

`start.sh`:
```bash
#!/bin/sh
exec node /app/src/index.js
```

`service.json`:
```json
{
    "tag": "my-node-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 134217728,
            "disk_space": 1073741824
        },
        "at_most": {
            "mem_limit": 536870912,
            "disk_space": 5368709120
        }
    },
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 3000,
            "transport": "tcp",
            "protocol": ["http1.1", "rest"],
            "gas_amount_per_call": {
                "POST /process": 80,
                "GET /health": 5
            }
        }
    ]
}
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "package.json",
        "package-lock.json",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "node_modules/",
        "tests/",
        "**/*.test.js",
        "**/*.spec.js",
        "*.md",
        ".env",
        ".env.*",
        "coverage/"
    ]
}
```

---

#### Node.js (TypeScript)

```dockerfile
# Build stage — compile TypeScript
FROM node:22-alpine AS builder
WORKDIR /build
COPY ./package.json ./package-lock.json ./tsconfig.json ./
RUN npm ci
COPY ./src ./src
RUN npm run build

# Dependency stage — production only
FROM node:22-alpine AS deps
WORKDIR /deps
COPY ./package.json ./package-lock.json ./
RUN npm ci --omit=dev

# Runtime stage
FROM node:22-alpine
WORKDIR /app
COPY --from=deps /deps/node_modules ./node_modules
COPY --from=builder /build/dist ./dist
COPY ./package.json ./
COPY ./start.sh ./start.sh
RUN chmod +x /app/start.sh
```

`start.sh`:
```bash
#!/bin/sh
exec node /app/dist/index.js
```

`service.json`:
```json
{
    "tag": "my-ts-service",
    "architecture": "linux/amd64",
    "resources": {
        "at_init": {
            "mem_limit": 134217728,
            "disk_space": 1073741824
        },
        "at_most": {
            "mem_limit": 536870912,
            "disk_space": 5368709120
        }
    },
    "init": {
        "entry_path": ["app", "start.sh"]
    },
    "api": [
        {
            "port": 3000,
            "transport": "tcp",
            "protocol": ["http1.1", "rest"]
        }
    ]
}
```

`pack_config.json`:
```json
{
    "include": [
        "src",
        "package.json",
        "package-lock.json",
        "tsconfig.json",
        "start.sh",
        ".service/pack_config.json"
    ],
    "ignore": [
        "node_modules/",
        "dist/",
        "**/*.test.ts",
        "**/*.spec.ts",
        "*.md",
        ".env",
        "coverage/"
    ]
}
```

> **Note:** The compiled `dist/` output lives only inside the Docker build stage. There is no need to include it in `pack_config.json` — it is never part of the source package, only of the final exported filesystem.

---

### Resource Reference by Language

The following table provides a starting point for resource configuration based on typical language runtime overhead. Adjust values based on your actual workload.

| Language / Runtime | Typical `at_init` mem | Typical `at_most` mem | Notes |
|--------------------|-----------------------|-----------------------|-------|
| Python | 30–80 MB | 200–500 MB | Depends heavily on loaded libraries |
| Java (JVM) | 200–400 MB | 512 MB–2 GB | Use `-XX:+UseContainerSupport` |
| PHP-FPM | 64–128 MB | 256–512 MB | Per worker process |
| Rust (native) | 4–32 MB | 64–256 MB | Extremely low baseline |
| Node.js | 64–128 MB | 256–512 MB | V8 heap overhead |
| Go | 16–64 MB | 128–512 MB | Low baseline, GC dependent |

---

### Filesystem Parsing Behaviour

Once the Docker build produces the filesystem tar, the packer recursively parses every file and directory according to these rules:

| Entry type | Behaviour |
|------------|-----------|
| Regular file (small) | Embedded directly as raw bytes in the protobuf |
| Regular file (large, ≥ `MIN_BUFFER_BLOCK_SIZE`) | Stored as a separate content-addressed block; referenced by hash |
| Directory | Recursively parsed |
| Symlink | Stored with source and destination paths |
| Device node (block/char) | Stored as a file placeholder; recovered via xattrs during build |
| Whiteout file (`.wh..wh..opq`) | Skipped (OCI layer opaque whiteout marker) |

> **Block storage:** Large files are stored as blocks identified by their content hash. This deduplicates identical large files across services and avoids embedding huge blobs directly in the protobuf.

---

### Dockerfile Best Practices for This Packer

1. **Always use multi-stage builds** to keep the exported filesystem minimal
2. **`CMD`, `ENTRYPOINT`, and `EXPOSE` are ignored** — the entrypoint comes from `service.json → init.entry_path`, and ports from `service.json → api`
3. **Make your entrypoint script executable** (`chmod +x`) inside the Dockerfile, since file permissions are preserved in the exported filesystem
4. **Minimize the number of layers** in the final stage to keep the filesystem clean
5. **Use slim or minimal base images** (`-slim`, `alpine`, `distroless`) to reduce the final package size
6. **Do not include build tools in the final stage** — use multi-stage builds to compile and then copy only the artifacts
7. **Avoid writing to `/tmp` at build time** if those files are not needed at runtime — they will be included in the exported filesystem

---

## Service Preparation Process

### 1. Directory Preparation (`prepare_directory`)

```
Input: local directory or Git repo URL
           │
           ▼
   Create cache directory
   with unique identifier
           │
           ▼
   Does .service/ exist?
      │           │
     Yes          No
      │           │
      │    Create .service/
      │    Copy Dockerfile,
      │    service.json
      │    (.dockerignore is NOT copied)
      │    Create default pack_config.json
      │           │
      └─────┬─────┘
            │
            ▼
   Read .dockerignore and merge its
   patterns into pack_config.json ignore
   list (the file itself is never copied,
   so Docker never sees it)
            │
            ▼
   Adjust Dockerfile COPY commands
   (./relative → service/relative)
```

### 2. Service ZIP Generation (`generate_service_zip`)

```
project_directory/
        │
        ▼
Clean previous artifacts
(.service.zip, service/)
        │
        ▼
Read pack_config.json
        │
        ├── include defined? ──Yes──► Copy only listed files to service/
        └── No ──────────────────────► Copy all files (except .service/) to service/
        │
        ▼
Apply ignore patterns
        │
        ▼
Export dependencies:
  ├── Copy service deps  → service/__services__/
  │     └── strip wbp.bin if ignore_loadable_protobuf: true
  ├── Copy metadata      → service/__metadata__/
  ├── Copy blocks        → service/__block__/
  └── Write .dependencies if dependencies_env: true
        │
        ▼
zip: true? ──Yes──► Compress __services__, __metadata__, __block__
        │           into services.zip and remove originals
        No
        │
        ▼
Create final .service.zip (zip of entire .service/ directory)
        │
        ▼
Remove temp service/ directory
        │
        ▼
Return path: .service/.service.zip
```

### 3. Packing Process

Once the `.service.zip` is received, the packer extracts it and begins a multi-stage process to convert the service source into a fully specified, content-addressed service artifact.

```
.service.zip
        │
        ▼
┌─────────────────────────────┐
│       EXTRACTION            │
│                             │
│  Unzip to isolated          │
│  temporary directory        │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│     VALIDATION              │
│                             │
│  Read service.json          │
│  Validate architecture      │
│  field against supported    │
│  platform list              │
│                             │
│  Verify host machine arch   │
│  matches target arch        │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│     DOCKER BUILD            │
│                             │
│  docker buildx build        │
│  --platform <arch>          │
│  --output type=tar          │
│                             │
│  Streams build logs         │
│  in real time               │
│                             │
│  On failure → abort with    │
│  full build log             │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│   FILESYSTEM EXPORT         │
│                             │
│  Extract filesystem.tar     │
│  to temporary directory     │
│                             │
│  Measure total size of      │
│  exported files to          │
│  calculate RAM budget       │
│  for the next stage         │
└────────────┬────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────┐
│              FILESYSTEM PARSING                  │
│                                                  │
│  Traverse every entry recursively:               │
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │ For each entry:                         │     │
│  │                                         │     │
│  │  Symlink?  ──► store src + dst paths    │     │
│  │                                         │     │
│  │  Device?   ──► store as placeholder,    │     │
│  │                recover via xattrs       │     │
│  │                                         │     │
│  │  Small     ──► embed raw bytes          │     │
│  │  file?         directly in spec         │     │
│  │                                         │     │
│  │  Large     ──► write to content-        │     │
│  │  file?         addressed block,         │     │
│  │                store reference hash     │     │
│  │                                         │     │
│  │  Directory ──► recurse                  │     │
│  │                                         │     │
│  │  Whiteout  ──► skip                     │     │
│  │  marker?                                │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
│  File permissions and metadata preserved         │
│  via extended attributes (xattrs) on each entry  │
└────────────┬─────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────┐
│            METADATA PARSING                      │
│                                                  │
│  From service.json:                              │
│                                                  │
│  Resources                                       │
│  ├── at_init: mem, disk, cpu, blkio              │
│  └── at_most: mem, disk, cpu, blkio              │
│      (clamped to be ≥ at_init values)            │
│                                                  │
│  Entrypoint                                      │
│  └── entry_path segments + xattrs               │
│                                                  │
│  Config declaration path                         │
│                                                  │
│  Architecture tags                               │
│                                                  │
│  API slots                                       │
│  ├── port + transport protocol                   │
│  ├── application protocol stack                  │
│  └── gas cost per method                         │
│                                                  │
│  Environment variables                           │
│  └── names only (envs); no descriptors embedded  │
│                                                  │
│  Network requirements                            │
│  └── tags + prose per network entry              │
└────────────┬─────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────┐
│         SERVICE SPECIFICATION STRUCTURE          │
│                                                  │
│  Service                                         │
│  ├── container                                   │
│  │   ├── architecture                            │
│  │   │   └── tags (e.g. "linux/amd64")           │
│  │   │                                           │
│  │   ├── filesystem  ◄── parsed from Docker      │
│  │   │   └── branch[]                            │
│  │   │       ├── name                            │
│  │   │       ├── xattrs (permissions, metadata)  │
│  │   │       └── item (oneof):                   │
│  │   │           ├── file (bytes / block ref)    │
│  │   │           ├── link (src + dst)            │
│  │   │           └── filesystem (recurse)        │
│  │   │                                           │
│  │   ├── init                                    │
│  │   │   ├── entry_path[]                        │
│  │   │   └── xattrs                              │
│  │   │                                           │
│  │   ├── resources                               │
│  │   │   ├── at_init (mem, disk, cpu, blkio)     │
│  │   │   └── at_most (mem, disk, cpu, blkio)     │
│  │   │                                           │
│  │   └── config_declaration                      │
│  │       ├── path[]                              │
│  │       └── format                              │
│  │                                               │
│  ├── api                                         │
│  │   │   (envs declares names only; no field     │
│  │   │    for environment_variables descriptors) │
│  │   │                                           │
│  │   └── slot[]                                  │
│  │       ├── port                                │
│  │       ├── transport                           │
│  │       │   └── Protocol { tags[] }             │
│  │       ├── protocol_stack[]                    │
│  │       │   └── Protocol { tags[] }             │
│  │       └── gas_amount_per_call{}               │
│  │           └── method → GasAmount              │
│  │                                               │
│  └── network[]                                   │
│      ├── tags[]                                  │
│      └── prose                                   │
└────────────┬─────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────┐
│              HASHING & STORAGE                   │
│                                                  │
│  Serialize Service specification                 │
│                                                  │
│  Service id: save() ALWAYS builds a              │
│  multiblock directory and streams all            │
│  blocks to compute the hash (no shortcut).       │
│                                                  │
│  The Case A / Case B split below applies         │
│  only to the *filesystem* HashTag, not the       │
│  service id:                                     │
│  ├── Case A — no large file blocks:              │
│  │   └── hash the raw filesystem bytes           │
│  └── Case B — contains large file blocks:        │
│      └── hash the reconstructed multiblock       │
│          directory contents                      │
│                                                  │
│  Metadata                                        │
│  ├── hashtag                                     │
│  │   ├── hash[]                                  │
│  │   │   ├── Configured algo (e.g. BLAKE3)       │
│  │   │   └── SHA3-256 (universal fallback)       │
│  │   ├── tag[]  ◄── from service.json "tag"      │
│  │   └── attr_hashtag[]                          │
│  │       └── key=1 (container attr)              │
│  │           └── key=2 (filesystem hash)         │
│  │                                               │
│  Validate no duplicate hash types in metadata    │
└────────────┬─────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────┐
│        CLEANUP              │
│                             │
│  Remove temporary build     │
│  and extraction directories │
└────────────┬────────────────┘
             │
             ▼

     (service_id, metadata, service_directory)
```

---

#### Stage Details

**Extraction**
The zip is unpacked into an isolated temporary directory unique to this packing job, preventing collisions between concurrent packing processes.

**Validation**
The `architecture` field from `service.json` is matched against the list of supported platforms. If no match is found, or if the host machine's architecture does not match the target, the process is aborted immediately before any Docker build is attempted.

**Docker Build**
The build is executed using `docker buildx` in a dedicated builder instance configured with host networking. The output is not a Docker image — it is a raw filesystem tar archive. Build logs are streamed line by line in real time. If the build fails for any reason, the full log output is captured and returned as the error message.

**Filesystem Export**
The tar archive is extracted to a local directory. The total size of all exported files is measured at this point and used to calculate how much RAM to reserve for the parsing stage, based on a configurable memory size factor.

**Filesystem Parsing**
Every file, directory, symlink, and device node in the exported filesystem is traversed recursively. File permissions and ownership metadata are captured and stored as extended attributes on each entry. Files below a configured size threshold are embedded directly as raw bytes in the service specification. Files above that threshold are written to separate content-addressed blocks stored on disk, with only a reference hash kept in the specification. This deduplicates large identical files across services and keeps the specification itself compact.

**Metadata Parsing**
All runtime configuration declared in `service.json` is read and embedded into the service specification: resource limits, entrypoint path, config file location, architecture, API slots with their transport and protocol tags, gas costs per method, environment-variable names (declared via `envs`; per-variable `.field` descriptors are not embedded — no target field in `pack.proto`), and network access requirements.

**Service Spec., Hashing & Storage**
The service identifier is generated by hashing the fully serialized Service definition—including container specification, API, and network requirements—where filesystem hashing incorporates either the raw filesystem bytes or the reconstructed multiblock directory contents, after which the resulting digests, tags, and nested filesystem hash are stored in a HashTag tree structure with duplicate-hash-type validation enforced before finalization.

**Cleanup**
All temporary directories created during extraction, building, and filesystem export are removed. Only the final service directory and metadata are returned to the caller.


## Best Practices

### File Organization
- Keep all configuration in `.service/`
- Use `include` for explicit control over packaged files
- Keep root directory clean

### Dockerfile
- Always use multi-stage builds
- `CMD`, `ENTRYPOINT`, and `EXPOSE` are ignored — the entrypoint comes from `service.json → init.entry_path`
- Use minimal base images for the final stage
- Ensure entrypoint scripts are executable inside the Dockerfile

### service.json
- Always specify `architecture` explicitly
- Set realistic `at_init` and `at_most` resource values
- Use `init.entry_path` (not the legacy `entrypoint` field)
- Define all API slots accurately, including gas costs

### Dependencies
- Use dictionary format for `dependencies` when `dependencies_env: true`
- Use `ignore_loadable_protobuf: true` when protobuf binaries are not needed
- Use `zip: true` for large dependency trees

### Build Size Optimization

| Strategy | Configuration |
|----------|--------------|
| Multi-stage Dockerfile | Separate build and runtime stages |
| Explicit include list | `"include": ["src", "start.sh"]` |
| Exclude test files | `"ignore": ["tests/"]` |
| Zip dependencies | `"zip": true` |
| Strip protobuf | `"ignore_loadable_protobuf": true` |
| Minimal base image | Use `FROM python:3.11-slim` instead of `FROM python:3.11` |

---

## Common Issues and Solutions

### 1. Unsupported Architecture
**Symptom:** `Can't pack this service, not supported architecture.`

**Solution:** Ensure `architecture` in `service.json` is a supported value and matches the host machine architecture.

```json
// ✅ Correct
{ "architecture": "linux/amd64" }
```

---

### 2. Docker Build Failure
**Symptom:** `Critical build error: Command [...] returned non-zero exit status`

**Solutions:**
- Check COPY paths in Dockerfile — if the Dockerfile was moved to `.service/`, relative paths must use `service/` prefix (this is done automatically, but verify)
- Ensure base images are available and accessible
- Check that all files referenced in COPY instructions are present in the `include` list of `pack_config.json`

---

### 3. Missing Entrypoint File in Filesystem
**Symptom:** Service starts but the entrypoint binary/script is not found.

**Solutions:**
- Verify the script is copied in the Dockerfile and marked as executable:
  ```dockerfile
  COPY ./start.sh /app/start.sh
  RUN chmod +x /app/start.sh
  ```
- Verify `init.entry_path` in `service.json` matches the actual path in the container:
  ```json
  { "init": { "entry_path": ["app", "start.sh"] } }
  ```

---

### 4. `dependencies_env` with Array Format
**Symptom:** `Without keys, write env doesn't have sense` exception.

```json
// ❌ Wrong
{ "dependencies": ["dep/path"], "dependencies_env": true }

// ✅ Correct
{ "dependencies": { "MY_DEP": "dep/path" }, "dependencies_env": true }
```

---

### 5. Files Missing from Package
**Symptom:** The final `.service.zip` is missing expected files.

**Solutions:**
- If using `include`, ensure all required files are listed
- Check `ignore` patterns are not too broad
- Verify `.dockerignore` patterns are not accidentally merged into `pack_config.json ignore`

---

### 6. Package Too Large
**Symptom:** The generated `.service.zip` or service is unexpectedly large.

```json
{
    "zip": true,
    "ignore_loadable_protobuf": true,
    "include": ["src", "start.sh"],
    "ignore": ["tests/", "*.pyc", "__pycache__/", "*.md"]
}
```

Also review the Dockerfile:
```dockerfile
# Use multi-stage to avoid including build tools
FROM python:3.11 AS builder
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /install /usr/local
COPY ./src /app/src
```

---

### 7. Blocks Not Found
**Symptom:** Blocks are missing from the final package.

**Cause:** Blocks are resolved from each dependency's `_.json` manifest.

**Solution:** Ensure each dependency in the registry has a valid `_.json` file:
```json
[
    ["block-abc123", "some-metadata"],
    ["block-def456", "other-metadata"]
]
```
