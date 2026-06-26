# Visual Enhancement Plan — Borrowing from fireworks-tech-graph & Cocoon-AI

## Background

After comparing `kai-business-blueprint` with two open-source projects, we identified features worth integrating. This document defines what to borrow, what to skip, and the implementation plan.

**Source projects:**
- [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) — Semantic SVG tech architecture diagrams with arrow system, shape vocabulary, and visual styles
- [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) — Template-driven HTML architecture diagram generation

## Current State

| Feature | Status in kai-business-blueprint |
|---------|-----------------------------------|
| Arrow rendering | Solid/dashed, single color. No per-type differentiation. |
| Node shapes | All `<rect>` with different `rx` values. No semantic shape differentiation. |
| Color themes | Light/Dark only. No industry-specific palettes. |
| Visual regression tests | None. Manual SVG inspection only. |
| HTML template | Python string concatenation in `export_html.py` (244 lines of f-strings). |
| Summary cards | Already implemented (Systems, Capabilities, Actors, Flow Steps, Coverage). |
| System category colors | 7 categories (frontend/backend/database/cloud/security/message_bus/external). |

## What to Borrow

### 1. Semantic Arrow System (from fireworks-tech-graph)

**Priority:** High | **Effort:** Low

Currently arrows are either solid (main color) or dashed (muted color). Fireworks encodes relationship *type* with distinct visual styles:

| Relation type | Stroke color | Dash pattern | Marker |
|---------------|-------------|--------------|--------|
| `supports` | `#34D399` (emerald) | solid | filled arrow |
| `depends-on` | `#94A3B8` (gray) | `6,4` | open arrow |
| `flows-to` | `#60A5FA` (blue) | solid | filled arrow |
| `owned-by` | `#FBBF24` (amber) | `3,3` | filled dot |

**Current code location:** `export_svg.py` lines 186-225 (`_arrow_line`, `_arrow_label`, `_render_arrow_line`).

**Changes:**
1. Add `ARROW_STYLES` dict mapping relation type → (color, dash, marker)
2. Add 2 new SVG markers: `arrow-open` (no fill) and `arrow-dot` (filled circle)
3. Update `_render_arrow_line()` to look up `ARROW_STYLES[arrow.get("type", "supports")]`
4. Update legend to show arrow type meanings

**Files:** `export_svg.py` only.

---

### 2. Semantic Shape Vocabulary (from fireworks-tech-graph)

**Priority:** Medium | **Effort:** Medium

Currently all nodes are rectangles with different corner radii. Fireworks uses distinct shapes per entity type:

| Entity type | Shape | SVG element |
|-------------|-------|-------------|
| `capability` | Rounded rectangle | `<rect rx="8">` (current) |
| `system` | Rectangle with icon area | `<rect rx="4">` + left icon strip |
| `actor` | Circle/pill | `<rect rx="22">` (current) → consider `<ellipse>` for single actor |
| `flowStep` | Diamond | `<polygon>` with rotated square |

**Current code location:** `export_svg.py` lines 159-183 (`_node_svg`).

**Changes:**
1. Add `_node_svg_flowstep()` — diamond shape using `<polygon>` transform
2. Add `_node_svg_system()` — rect with 4px-wide left color strip (category indicator)
3. Update `_node_svg()` to dispatch by kind

**Files:** `export_svg.py` only.

---

### 3. Visual Regression Fixtures (from fireworks-tech-graph)

**Priority:** Medium | **Effort:** Low

Fireworks uses sample JSON + expected SVG pairs. We have none.

**Changes:**
1. Create `tests/fixtures/` directory
2. Add 3 fixture pairs:
   - `retail-basic.blueprint.json` + `retail-basic.expected.svg`
   - `multi-relation.blueprint.json` + `multi-relation.expected.svg`
   - `empty-skeleton.blueprint.json` + `empty-skeleton.expected.svg`
3. Add `tests/test_visual_regression.py`:
   - Loads each fixture JSON
   - Runs `export_svg()` to generate actual SVG
   - Compares node count, arrow count, color tokens, text labels
   - Does NOT do pixel comparison (too fragile across platforms)

**Test checks per fixture:**
```
- Correct number of <g class="node"> elements
- Correct number of <line> elements with marker-end
- All expected text labels present
- Expected fill/stroke colors present
- SVG viewBox dimensions within tolerance
```

**Files:** New `tests/fixtures/` dir, new `tests/test_visual_regression.py`.

---

### 4. Industry Color Themes (from fireworks-tech-graph)

**Priority:** Low | **Effort:** Low

Fireworks offers per-industry color palettes. Currently we have Light/Dark only.

**Proposed industry accent colors:**

| Industry | Primary accent | Capability fill | System fill | Actor fill |
|----------|---------------|----------------|-------------|------------|
| `retail` | `#F97316` (orange) | `#FFF7ED` | `#FFF7ED` | `#FEF3C7` |
| `finance` | `#3B82F6` (blue) | `#EFF6FF` | `#EFF6FF` | `#DBEAFE` |
| `manufacturing` | `#6B7280` (slate) | `#F3F4F6` | `#F3F4F6` | `#E5E7EB` |
| `common` | `#0B6E6E` (teal) | current | current | current |

**Implementation:**
1. Add `INDUSTRY_THEMES` dict to `export_svg.py`
2. `_resolve_theme()` accepts optional `industry` parameter
3. When `industry` provided, overlay industry accent onto base theme
4. `cli.py --export` passes `industry` from blueprint `meta.industry`
5. `export_html.py` reads industry from blueprint and passes through

**Files:** `export_svg.py`, `export_html.py`, `cli.py`.

---

### 5. Template-Driven HTML (from Cocoon-AI)

**Priority:** Low | **Effort:** Medium

`export_html.py` is 244 lines of Python f-strings. Hard to maintain. Cocoon-AI uses HTML template files with placeholders.

**Changes:**
1. Create `business_blueprint/templates/html-viewer.html` with `{{PLACEHOLDER}}` markers
2. Refactor `export_html.py` to load template + substitute values
3. Template sections:
   - Header (title, version, download button)
   - Summary cards (N systems, N capabilities, etc.)
   - SVG viewer area
   - Description cards (goals, scope, assumptions, constraints)
   - JavaScript (blueprint JSON, download function)

**Benefits:** Easier to customize HTML output, non-Python developers can edit the template.

**Files:** New `business_blueprint/templates/html-viewer.html`, refactored `export_html.py`.

---

## What NOT to Borrow

| Feature | Source | Reason |
|---------|--------|--------|
| rsvg-convert PNG export | fireworks-tech-graph | System dependency (`librsvg`), not sandbox-friendly |
| No data model (pure prompt) | Cocoon-AI | JSON schema is our strength, not a weakness |
| 14 UML diagram types | Cocoon-AI | Doesn't match business blueprint positioning |
| Product icons (40+) | fireworks-tech-graph | Too large a scope, no immediate need |
| Mermaid-as-output | fireworks-tech-graph | Already implemented in `export_mermaid.py` |

---

## Implementation Plan

### Phase 1: Semantic Arrows + Regression Fixtures

**Goal:** Better arrow visuals + test safety net before bigger changes.

| Step | File | Description |
|------|------|-------------|
| 1.1 | `export_svg.py` | Add `ARROW_STYLES` dict + 2 new markers |
| 1.2 | `export_svg.py` | Update `_render_arrow_line()` for type-based rendering |
| 1.3 | `export_svg.py` | Update `_legend_svg()` to show arrow types |
| 1.4 | `tests/fixtures/` | Create 3 fixture JSON + SVG pairs |
| 1.5 | `tests/test_visual_regression.py` | Structural SVG comparison tests |
| 1.6 | all | Run full test suite, verify no regressions |

### Phase 2: Semantic Shapes

**Goal:** Diamond flowStep, system with category strip.

| Step | File | Description |
|------|------|-------------|
| 2.1 | `export_svg.py` | Add `_node_svg_flowstep()` with diamond `<polygon>` |
| 2.2 | `export_svg.py` | Add `_node_svg_system()` with left color strip |
| 2.3 | `export_svg.py` | Update `_node_svg()` dispatch |
| 2.4 | `tests/fixtures/` | Update expected SVGs for new shapes |
| 2.5 | all | Run full test suite |

### Phase 3: Industry Themes

**Goal:** Per-industry accent colors.

| Step | File | Description |
|------|------|-------------|
| 3.1 | `export_svg.py` | Add `INDUSTRY_THEMES` + update `_resolve_theme()` |
| 3.2 | `cli.py` | Pass `industry` from blueprint meta |
| 3.3 | `export_html.py` | Read industry, pass to theme resolver |
| 3.4 | `tests/fixtures/` | Add industry-specific fixture |
| 3.5 | all | Run full test suite |

### Phase 4: HTML Template (optional)

**Goal:** Replace f-strings with template file.

| Step | File | Description |
|------|------|-------------|
| 4.1 | `templates/html-viewer.html` | Extract HTML to template file |
| 4.2 | `export_html.py` | Refactor to template loader |
| 4.3 | tests | Verify HTML output identical |

---

## Dependency Graph

```
Phase 1 (arrows + fixtures)
    ├── Phase 2 (shapes) — depends on 1.4 fixtures for regression safety
    └── Phase 3 (themes) — depends on 1.2 arrow styles

Phase 4 (HTML template) — independent, can run anytime
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Arrow style changes break existing SVGs | Low | Medium | Fixtures in Phase 1 catch regressions |
| Diamond shape too complex for short labels | Medium | Low | Fallback to rect if label > 6 chars |
| Industry themes look bad with dark mode | Medium | Low | Use HSL lightness shift, not fixed colors |
| HTML template breaks viewer functionality | Low | High | Structural comparison test on output |

## Success Criteria

- Phase 1: 4 arrow types visually distinct in exported SVG, 3 regression fixtures pass
- Phase 2: flowStep nodes render as diamonds, system nodes show category color strip
- Phase 3: `retail` blueprint exports with warm orange accent, `finance` with deep blue accent
- Phase 4: `export_html.py` < 80 lines, all HTML in template file
