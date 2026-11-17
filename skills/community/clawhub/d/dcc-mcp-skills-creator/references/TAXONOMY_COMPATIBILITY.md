## Gateway-Facing Tag Taxonomy

Gateway search treats `tags` as a narrowing filter. Use a small shared vocabulary
so pipeline, production-tracking, and documentation connectors rank and filter
consistently across hosts. When authoring `SKILL.md` frontmatter, include the
appropriate tags under `metadata.dcc-mcp.tags`:

| Tag | Use for |
|-----|---------|
| `pipeline` | Studio pipeline systems, publish/intake/review automation, and production data hand-offs. |
| `production-tracking` | Shot/asset/task/status tracking systems regardless of vendor. |
| `shotgrid` | Autodesk Flow Production Tracking / ShotGrid-specific tools. |
| `ftrack` | ftrack-specific tools. |
| `docs` | Documentation, product help, reference lookup, and guide resources. |
| `read-only` | Discovery/read operations. Also set MCP `readOnlyHint` (`annotations.read_only_hint: true` in `tools.yaml`); the tag is for search, not policy. |
| `destructive` | Mutating or irreversible operations. Also set MCP `destructiveHint` (`annotations.destructive_hint: true` in `tools.yaml`); the tag is for search, not policy. |

**Filter semantics:**
- `dcc_type` (singular) + `dcc_types[]` — **OR**: a result matching any listed
  DCC family passes. Include `dcc_type: "maya"` with `dcc_types: ["blender"]`
  to match records from either host in one request.
- `tags[]` — **AND**: a result must carry every listed tag. Use `pipeline` +
  `production-tracking` to narrow to records that carry both.
- `tags_any[]` — **OR**: a result carrying any listed tag passes. Combines with
  the AND filter above: `tags: ["pipeline"]` + `tags_any: ["read-only", "docs"]`
  returns pipeline records that are read-only OR documentation.

**Vendor tags** can be added when they sharpen routing without replacing the
canonical tags. For example, Autodesk Product Help should use `docs`,
`read-only`, and the vendor tag `autodesk`. Do not add `docs` to a
production-tracking search unless the user explicitly asks for help or reference
material.

### Python 3.7 Policy

All authored skills must declare `compatibility: "Python 3.7+"` in their
frontmatter when they are installed into an LTS DCC host. This applies to every
skill that is installed into a DCC host embedding Python 3.7 (Maya 2022,
Blender 2.83, 3ds Max 2022, etc.). `py37-lite` is a supported fallback but
does not replace the native Linux and Windows cp37 compatibility gates. See
ADR 011 and `compatibility/python.json` for the deprecation and CI contract.
In lite mode, `create_skill_server()` supports local metadata discovery
(`list_skills`, `search_skills`, and `get_skill`) only. The Rust sidecar is
dispatch-only, so gateway discovery and declarative `load_skill` execution
require a native Python 3.7 wheel; lite activation fails explicitly.

For hermetic CI or tests, set `DCC_MCP_DISABLE_DEFAULT_SKILL_PATHS=1` so an
operator's local/platform defaults, marketplace installs, and Admin custom
paths cannot alter discovery results. Explicit, bundled, and
`DCC_MCP_*_SKILL_PATHS` paths remain active under this mode.

**Skill SKILL.md example** (frontmatter excerpt):

```yaml
metadata:
  dcc-mcp:
    dcc: shotgrid
    layer: domain
    tags: [pipeline, production-tracking, shotgrid]
    search-hint: "ShotGrid task status, find shots, update task assignments"
    tools: tools.yaml
```

```yaml
# Read-only docs connector (SKILL.md excerpt)
metadata:
  dcc-mcp:
    dcc: autodesk-help
    layer: infrastructure
    tags: [docs, autodesk, read-only, infrastructure]
    search-hint: "Autodesk Product Help, Maya help, 3ds Max help, API reference"
    tools: tools.yaml
```

Individual read tools should also carry `read-only` in their tool-level tags;
mutating publish/update tools should carry `destructive` when applicable.
