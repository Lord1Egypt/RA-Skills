# Design Token Contract

Style systems must be reproducible design systems, not mood labels.

## Required Contract

Every `style-contract.json` must validate against `schemas/style-contract.schema.json` and include:

- `schema_version`
- `style_id`
- `display_name`
- `colors`
- `typography`
- `grid`
- `spacing`
- `shape_tokens`
- `shadow_tokens`
- `card_tokens`
- `table_tokens`
- `chart_tokens`
- `diagram_tokens`
- `image_tokens`
- `icon_tokens`
- `footer_tokens`
- `density_limits`
- `allowed_effects`
- `forbidden_drift`
- `compatibility_aliases`

Legacy `style_system`, `palette_name`, `spacing_scale_in`, `component_variants`, and `footer` may appear in old artifacts only. Migrate them with `scripts/migrate_style_contract_v1_to_v2.py`.

## Builder Rules

Builders must not invent design parameters at build time. Read from the contract for:

- colors and allowed opacity
- font stacks and type sizes
- page grid, margins, title zone, footer zone, and safe zone
- spacing scale and spacing rules
- card radius, borders, padding, shadows, and variants
- table header/body styles, row alternation, borders, padding, and highlights
- chart series colors, axes, labels, gridlines, markers, and legend behavior
- diagram node, boundary, connector, and relation styles
- image crop, caption, overlay, and generated-image constraints
- footer height, type, divider, and quiet color
- density diagnostic limits

If a builder cannot satisfy a token, record the fallback in the build manifest or fail the route before drawing.

## Color Rules

Builders must use semantic color tokens such as `primary`, `accent`, `surface_1`, `text_primary`, and `border`. Do not place raw hex values in page objects unless they are recorded under `colors`.

Allowed color sources:

- exact tokens from `colors`
- `data_series` entries
- opacity values from `colors.allowed_opacity`
- user-supplied brand colors recorded in the contract

QA must flag unapproved colors as `STYLE_UNKNOWN_TOKEN_REFERENCE` or `STYLE_INVALID_HEX`.

## Typography Rules

Font fields must be ordered fallback stacks and end with a generic family such as `sans-serif`, `serif`, or `monospace`.

Text sizes must respect:

- `minimum_body_size_pt`
- `minimum_footnote_size_pt`
- semantic `title_sizes_pt`
- semantic `body_sizes_pt`
- `line_height`
- `paragraph_spacing_pt`
- non-negative `letter_spacing_pt`
- standard font weights

## Grid And Spacing Rules

Grid defines the usable page coordinate system. Components must not silently replace:

- columns and rows
- margins
- horizontal and vertical gutters
- title and footer zones
- safe-zone inset

Spacing between components should reference `spacing.scale` through `spacing.rules`. Unregistered spacing values are style drift unless explicitly recorded as an override.

## Component Tokens

Each style should define tokens for:

- cards: `default`, `highlight`, `metric`, `risk`, `quote`, `comparison`, `source`
- tables: `default`, `matrix`, `minimal`
- charts: series colors, axes, labels, highlight, and chart border/legend/gridline defaults
- diagrams: node, primary node, connector, boundary, and relation styles
- images: crop mode, caption style, overlay, grayscale/duotone policy
- icons: stroke width, colors, and allowed styles
- footer: height, color, font size, divider

## Palette Naming

Keep old palette aliases for migration, but prefer neutral internal style IDs:

- `mckinsey` -> `consulting-light`
- `bcg` -> `consulting-light`
- `linear` -> `product-report`
- `stripe` -> `product-report`
- `ibm-whitepaper` -> `technical-blueprint`
- `deep-amber` -> `consulting-blueprint-hybrid`
- `warm-paper` -> `editorial-knowledge`

Do not imply that generated decks are official brand templates.
