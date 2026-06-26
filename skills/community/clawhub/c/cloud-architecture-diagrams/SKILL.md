---
name: cloud-architecture-diagrams
description: "Build editable cloud architecture diagrams (Azure/Microsoft, AWS, GCP, Microsoft Fabric) using official vendor icons, output as both .excalidraw and .drawio with icons embedded and labeled arrows. Use to create, draw, recreate, or lay out a cloud or Microsoft Fabric architecture or solution diagram from a text description or by uploading a screenshot to reproduce."
homepage: https://github.com/hansraj316/cloud-arch-marketplace
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["python3"] },
        "os": ["darwin", "linux"],
      },
  }
---

# Cloud Architecture Diagrams (Azure / AWS / GCP)

Generate professional cloud architecture diagrams that match the house style of
the official vendor reference architectures: dashed grouping zones (Power
Platform / Azure / Data Source, or VPC / Subnet / Region), white rounded
"cards" with a real product icon plus a bold title and a small description,
directional and bidirectional arrows with labels, and optional numbered step
badges.

The output is two editable files from one spec:
- `<name>.excalidraw` — JSON, opens at excalidraw.com (icons embedded as base64)
- `<name>.drawio` — mxGraph XML, opens at app.diagrams.net (icons embedded as data URIs)

Both are self-contained: the icons travel inside the file, so they render
offline and survive being shared.

## Why a spec + script instead of hand-placing shapes

Drawing the JSON/XML by hand is error-prone and the two formats drift apart.
Instead you write ONE small **spec** (zones, nodes, edges) and a bundled
script renders both files identically, fetches the right icons, embeds them,
and routes the arrows. You spend your effort on the part that needs judgment —
choosing icons and laying things out — not on file plumbing.

## Icon sources (providers)

The skill knows ~5,500 icons across five providers, all bundled offline. Pick
the one that matches what you're drawing:

| Provider | What it covers | Where the icons live |
|----------|----------------|----------------------|
| `aws` | Official AWS Architecture Icons — EC2, S3, Lambda, VPC, ECS/EKS, RDS, DynamoDB, etc. (~800) | **bundled** in `assets/icons/aws/` (offline) |
| `azure` | Official Microsoft Azure service icons V23 (~626) | **bundled** in `assets/icons/azure/` (offline) |
| `gcp` | Official Google Cloud icons — Compute Engine, GKE, BigQuery, Cloud Run, Vertex AI, Cloud Storage, etc. (a curated ~45-icon set of core products + category tiles) | **bundled** in `assets/icons/gcp/` (offline) |
| `microsoft` | The broadest Microsoft set, **bundled offline** (~2,430): Power Platform (Power Apps, Power Automate, Power Pages, Copilot Studio, AI Builder, Dataverse, Agent 365), Dynamics 365 (Sales, Customer Service, Field Service, Finance, Business Central, Commerce, Supply Chain, Customer Insights, …), plus Azure services, Microsoft Fabric brand tiles, Teams, Entra, Intune, Purview, Planner | **bundled** in `assets/icons/microsoft/` (offline) |
| `fabric` | Official **Microsoft Fabric** Fluent icon set (`@fabric-msft`, ~1,580): Lakehouse, Warehouse, Data Factory, Data Engineering, Data Science, Power BI, Eventhouse, Real-Time, Purview, Copilot, etc. Ships **every size (12/16/20/24/28/32/40/48/64 px) and variant (color, item, filled, regular)** of each icon | **bundled** in `assets/icons/fabric/` (offline) |

**Always pin the provider in the spec** (`"provider": "aws"`, `"azure"`, `"gcp"`,
`"microsoft"`, or `"fabric"`). For mixed Microsoft work (Power Platform + Azure)
use `"microsoft"` or `"providers": ["azure","microsoft"]`. A single node can
override with its own `"provider"` (e.g. a `fabric` diagram that also shows an
Entra ID logo → that node uses `microsoft`).

**Fabric sizing:** because the `fabric` pack carries every size, a bare query
like `"Data Warehouse"` returns the diagram-friendly **48px color** variant by
default; pin a specific one with `"icon": "Data Warehouse 24 color"` or
`"Lakehouse 32 item"` if you need it.

> **GCP coverage is partial.** The bundled Google set is a curated subset (core
> products + category tiles). Services not in it (e.g. Pub/Sub, Cloud Functions,
> Firestore, Dataflow) will fall back to labeled boxes. To get full coverage,
> download Google's complete official icon pack and import it with
> `add_icon_pack.py --provider gcp` (see "Refreshing or adding icon packs").

## Workflow

### 0. Confirm which cloud (ASK if it's not obvious)

Before anything else, settle on the provider. If the user already made it clear
— they said "AWS"/"Azure"/"GCP", named provider-specific services (S3, BigQuery,
Power Automate…), or uploaded an image whose icons identify the cloud — just use
that. **If it's ambiguous, ask before building:**

> Which icon set should I use — **Azure / Microsoft**, **AWS / Amazon**, or
> **GCP / Google**?

Don't guess when it's unclear; the wrong icon set means redrawing the whole
thing.

### 1. Understand the architecture

**If the user described it in words:** identify the logical groups (these
become *zones*), the components in each (these become *nodes*), and how data
flows between them (these become *edges*). Note any numbered sequence.

**If the user uploaded an image of a diagram to recreate:** read it carefully.
List every grouping container, every icon/box (its title + any subtitle), the
arrows (direction, any labels, any color coding), and any numbered step badges.
Reproduce the *structure and intent*, not necessarily pixel positions. It's
fine to tidy up spacing.

When the architecture is ambiguous or large, briefly confirm the component
list and grouping with the user before generating — re-rendering is cheap but
confirming intent first saves a wasted pass.

### 2. Resolve the icons (do this before writing the full spec)

Use the finder, scoped to the provider you're drawing, to pick the right icon
for each component:

```bash
python scripts/find_icon.py "S3" --provider aws -n 4
python scripts/find_icon.py "BigQuery" --provider gcp -n 4
python scripts/find_icon.py "Azure AI Search" --provider azure,microsoft -n 4
```

It prints scored candidates with their provider and location. Pick deliberately:
- A score around 2+ or an exact name match is a confident hit.
- A score below ~0.9 means there's probably no good icon — plan to fall back
  to a plain labeled box (omit `icon` for that node), and tell the user.
- **AWS** abbreviations work directly: `S3`, `EC2`, `VPC`, `IAM`, `SNS`, `SQS`,
  `ECS`, `EKS`, `RDS`, `ELB` all resolve to the canonical service icon.
- **GCP** full names and short forms work: `BigQuery`/`BQ`, `Compute Engine`/`GCE`,
  `Cloud Storage`/`GCS`, `GKE`, `Cloud Run`, `Vertex AI`. Coverage is partial —
  if a service isn't found, fall back to a labeled box (or import the full pack).
- **Microsoft** renames things. If a modern name misses, try the legacy name.
  See the synonym list in `references/spec-format.md` (e.g. *Azure AI Search*
  is filed under *Cognitive Search*; *Azure OpenAI* under *Open AI*).
- Always pass `--provider` so an AWS query can't match an Azure icon (and vice
  versa).

If you're confident about a specific icon, pin it in the spec with `"icon_url"`
(a msicons.com URL) to skip matching for `microsoft`; for bundled providers,
just naming the service is reliable.

### 3. Write the spec

Create a JSON spec following `references/spec-format.md`. Set the spec
`"provider"`, then lay it out using the conventions documented there
(left-to-right flow, zones as dashed containers, ~40px gaps, card size ~230×84).
Keep coordinates on a rough grid so the result looks deliberate.

Start from `assets/spec-example.json` as a template — it's a real worked
example you can adapt.

### 4. Generate both files

```bash
python scripts/build_diagram.py my_spec.json --out-prefix /mnt/user-data/outputs/my_diagram
```

This writes `my_diagram.excalidraw` and `my_diagram.drawio`, fetching and
embedding every icon. It prints an icon-resolution report to stderr — **read
it**: it tells you which query mapped to which icon and flags weak matches that
fell back to a labeled box. Fix any wrong matches by editing the `icon` value
(or pinning `icon_url`) and re-running.

Use `--only excalidraw` or `--only drawio` if the user wants just one.

#### Optional: native draw.io shapes

By default both files embed the icons as SVG (identical look, works everywhere).
You can instead have the **.drawio** use draw.io's own built-in vector stencils
— add `"drawio_shapes": true` to the spec (or pass `--drawio-shapes`):

```bash
python scripts/build_diagram.py my_spec.json --out-prefix out/dia --drawio-shapes
```

What this changes (drawio only — Excalidraw always stays embedded SVG):
- **AWS** → the official colored `resourceIcon` squares (`mxgraph.aws4.*`) with the
  correct category color baked in.
- **GCP** → self-colored `mxgraph.gcp2.*` stencils.
- **Azure** → `mxgraph.azure.*` (monochrome; limited set) — most Azure nodes have
  no native stencil and fall back to embedded SVG. `microsoft` (Power Platform,
  Dynamics 365, etc.) has no native draw.io vector stencils, so it always uses
  the bundled official SVGs — which are full-color and render in both formats.

Why use it: the shapes become first-class draw.io objects the user can recolor
and restyle, and the file is much smaller (no base64). Why not: matching is
best-effort against draw.io's version-specific stencil names, so **preview the
mapping first**:

```bash
python scripts/find_drawio_shape.py "IAM" --provider aws -n 5
```

If a match is wrong, pin the exact stencil on that node with
`"drawio_shape": "mxgraph.aws4.identity_and_access_management_iam"`. Nodes
without a confident native match automatically fall back to embedded SVG, so the
diagram is never broken. (Note: I can't render .drawio to PNG here — the preview
PNG shows the embedded-SVG version; confirm native shapes in diagrams.net.)

### 5. Preview and check

The inline Excalidraw tool can't show the embedded icons, so render a PNG:

```bash
python scripts/preview_png.py /mnt/user-data/outputs/my_diagram.excalidraw -o /tmp/preview.png
```

Open the PNG and check for: overlapping boxes, clipped arrow labels (short
arrows can't hold long labels — widen the gap or shorten the label), arrows
crossing through cards (add `waypoints` to that edge), and wrong/missing icons.
Iterate on the spec until it's clean. Show the user this preview so they can
see it without opening a file.

### 6. Deliver

Use `present_files` to give the user both files (and optionally the preview
PNG). Tell them which opens where (excalidraw.com / app.diagrams.net) and that
the icons are embedded so they can edit freely.

## Refreshing or adding icon packs

The skill ships with a prebuilt index (`references/icon-index.json`) plus the
bundled AWS and Azure SVGs, so normal use needs no network.

- Refresh the msicons.com (`microsoft`) set: `python scripts/build_icon_index.py`
- Add or update a bundled pack from a folder of SVGs you downloaded (e.g. a
  newer AWS Architecture Icons release, or an Azure icon pack):

  ```bash
  python scripts/add_icon_pack.py --source /path/to/unzipped/pack --provider aws
  ```

  It auto-detects AWS-style and Azure-style filenames, copies the chosen SVGs
  into `assets/icons/<provider>/`, and merges them into the index (replacing any
  prior entries for that provider). To add a brand-new cloud (e.g. GCP), unzip
  its SVGs and import them under a new provider id.

## What this skill does NOT do

- It won't invent icons that don't exist. Some logos simply aren't in any pack
  (msicons has no standalone SharePoint/Teams *logo*, for instance). When
  there's no good match, the node becomes a clean labeled box — say so.
- It draws from official **vendor** icon sets: AWS, Microsoft/Azure, and a
  curated Google Cloud set out of the box. GCP coverage is partial — import the
  full Google pack (or any other cloud) with `add_icon_pack.py` when needed.
- Don't mix providers blindly: pass `--provider` / set the spec `provider` so an
  AWS query can't pull an Azure or GCP icon.

## Files in this skill

- `scripts/find_icon.py` — search/fetch icons by service name (`--provider` aware)
- `scripts/build_diagram.py` — spec → `.excalidraw` + `.drawio` (the engine)
- `scripts/preview_png.py` — render a `.excalidraw` to PNG for visual check
- `scripts/build_icon_index.py` — (re)build the msicons.com index
- `scripts/add_icon_pack.py` — import a local SVG pack as a new/updated provider
- `scripts/bundle_microsoft.py` — bundle the Microsoft set offline (official Power Platform + Dynamics 365 packs + msicons.com)
- `scripts/find_drawio_shape.py` — preview native draw.io stencil matches
- `scripts/build_drawio_shape_index.py` — (re)build the native-shape index from draw.io's stencil source
- `references/spec-format.md` — full spec schema, layout cookbook, icon synonyms
- `references/icon-index.json` — prebuilt unified icon index (aws + azure + gcp + microsoft)
- `references/drawio-shape-index.json` — native draw.io stencil index (aws + gcp + azure)
- `assets/icons/aws/`, `assets/icons/azure/`, `assets/icons/gcp/`, `assets/icons/microsoft/` — bundled official SVGs (offline)
- `assets/spec-example.json`, `assets/aws-spec-example.json`, `assets/gcp-spec-example.json` — worked examples
