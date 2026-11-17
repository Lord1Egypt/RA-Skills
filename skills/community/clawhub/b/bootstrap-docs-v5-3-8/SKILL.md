---
name: bootstrap-docs-v5-3-8
description: "Documentation reference for Bootstrap 5.3.8. Use to look up the correct syntax, classes, and usage for Bootstrap components, utilities, layout, forms, and Sass variables. Not a coding tutor — only a reference lookup. Example triggers: \"Can I put mt-2 on an input?\", \"What does navbar-expand-lg do?\", \"What are the available button classes?\""
version: 1.0.0
homepage: https://getbootstrap.com/docs/5.3/
license: MIT
required_commands: []
required_environment_variables: []
required_privileges: none
metadata: {"hermes":{"emoji":"📚","category":"knowledge"},"required_binaries":[]}
---

# Bootstrap 5.3.8 Documentation Reference

Look up Bootstrap 5.3.8 syntax, classes, components, utilities, and variables from the official docs.

## Requirements

- None. This skill is a read-only documentation reference.

## Quick Reference

| User wants... | Do this |
|---------------|---------|
| Component docs (button, card, modal, etc.) | Search `scripts/bootstrap-reference.json` by component name |
| Utility classes (margin, padding, colors) | Search `scripts/bootstrap-reference.json` utilities category |
| Layout/grid system | Search `scripts/bootstrap-reference.json` layout/grid content |
| Form controls | Search `scripts/bootstrap-reference.json` forms category |
| Customization (variables, mixins) | Search `scripts/bootstrap-reference.json` customize content |
| Sass variables ($primary, $spacer, etc.) | Search `scripts/bootstrap-variables.json` by variable name |
| Migration from v4 | Read `migration` content in `scripts/bootstrap-reference.json` |
| Getting started guide | Read getting-started category in `scripts/bootstrap-reference.json` |
| Bootstrap source code examples | Search `scripts/bootstrap-reference.json` extend/customize |

## Important Rules

1. **This is a reference lookup skill, not a coding teacher.** Use it to verify class names, syntax, and behavior. Do not use it to generate entire sites from scratch.
2. **Always** search `scripts/bootstrap-reference.json` first before answering Bootstrap-related questions
3. **Cite** the specific category and slug when providing Bootstrap guidance (e.g., "components-card" for Card component)
4. **Distinguish** between Bootstrap v4 and v5 — this skill only covers v5.3.8
5. **Include** actual Bootstrap classes in examples (e.g., `btn btn-primary`, `card card-body`)
6. **FLAG** deprecated features if mentioned (search customize/deprecations content)
7. **Sass variables** — for `$variable` questions, use `scripts/bootstrap-variables.json` instead of guessing defaults

## Usage Guide

This skill provides read-only access to the official Bootstrap 5.3.8 documentation. Use it to answer questions like:

- "Can `mt-2` be applied to an `<input>`?"
- "What does `navbar-expand-lg` do?"
- "What's the difference between `btn-primary` and `btn-outline-primary`?"
- "Which utility class sets horizontal padding?"

Do not use this skill to teach Bootstrap from scratch or to generate whole projects.

### Basic Pattern

```javascript
// In your code
const fs = require('fs');
const reference = JSON.parse(fs.readFileSync('{baseDir}/scripts/bootstrap-reference.json', 'utf8'));
const variables = JSON.parse(fs.readFileSync('{baseDir}/scripts/bootstrap-variables.json', 'utf8'));

// Search for specific component
const result = reference.find(item => 
  item.category === "components" && 
  item.slug.includes("card")
);

// Look up a Sass variable
const primary = variables['_variables.scss']['primary'];
```

### Component Documentation

The `scripts/bootstrap-reference.json` contains entries from these categories:

- **about** - Bootstrap overview and ecosystem
- **components** - All Bootstrap components (alerts, badges, buttons, cards, carousels, dropdowns, modals, navs, navbars, offcanvas, pagination, popovers, progress, spinners, toasts, tooltips)
- **content** - Typography, images, tables, figures
- **customize** - Sass variables, color system, components, options, color modes
- **extend** - Approach, icons, JavaScript, Sass, webpack
- **forms** - Overview, form controls, select, checks & radios, range, input groups, floating labels, validation
- **getting-started** - Introduction, download, contents, webpack, parcel, vite
- **helpers** - Colored links, ratio, position, stacking, visibility, vertical rule
- **layout** - Breakpoints, containers, grid, columns, gutters, utilities, Z-index
- **utilities** - API, background, borders, colors, display, flex, float, interactions, overflow, position, shadows, sizing, spacing, text, vertical align, visibility
- **migration** - Major changes from v4 to v5

### Search Strategy

1. **Component lookup** → `category="components"`, slug contains component name
2. **Utility classes** → `category="utilities"`, search by utility type (e.g., "spacing", "colors")
3. **Forms** → `category="forms"`, specific control name
4. **Layout** → `category="layout"`, "grid" or "breakpoints"
5. **Customization** → `category="customize"`, "variables" or "sass"
6. **Sass variables** → `scripts/bootstrap-variables.json`, key = `$variable-name`

## Key Components Reference

| Component | Slug pattern | Key classes |
|-----------|-------------|-------------|
| Button | `components-button` | `btn`, `btn-primary`, `btn-lg`, `btn-group` |
| Card | `components-card` | `card`, `card-body`, `card-title`, `card-footer` |
| Modal | `components-modal` | `modal`, `modal-dialog`, `modal-content` |
| Navbar | `components-navbar` | `navbar`, `navbar-brand`, `navbar-nav`, `nav-item` |
| Form | `forms-overview` | `form-control`, `form-label`, `form-check` |
| Alert | `components-alert` | `alert`, `alert-primary`, `alert-dismissible` |
| Badge | `components-badge` | `badge`, `badge-primary` |
| Grid | `layout-grid` | `container`, `row`, `col-*`, `col-md-*` |

## Common Usage Examples

### Card with button

```html
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

### Responsive grid

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">Column 1</div>
    <div class="col-12 col-md-6 col-lg-4">Column 2</div>
    <div class="col-12 col-lg-4">Column 3</div>
  </div>
</div>
```

### Form with validation

```html
<div class="mb-3">
  <label for="email" class="form-label">Email</label>
  <input type="email" class="form-control is-valid" id="email">
  <div class="valid-feedback">Looks good!</div>
</div>
```

## Gotchas

- **Bootstrap requires Popper.js** for dropdowns, tooltips, and popovers — don't forget to include it
- **Container classes** have different behaviors: `.container` (responsive fixed width) vs `.container-fluid` (full width)
- **Grid columns without `.row`** will have incorrect gutters — always wrap in `.row`
- **Custom CSS** should override Bootstrap variables in Sass, not use `!important`
- **JavaScript components** require Bootstrap's JS bundle — they won't work with CSS-only

## Further Reading

- `{baseDir}/scripts/bootstrap-reference.json` — Complete Bootstrap 5.3.8 documentation index (embedded in skill)
- `{baseDir}/scripts/bootstrap-variables.json` — Sass variables and defaults from `_variables.scss` and `_utilities.scss`
- [Bootstrap official docs](https://getbootstrap.com/docs/5.3/) — Live documentation
