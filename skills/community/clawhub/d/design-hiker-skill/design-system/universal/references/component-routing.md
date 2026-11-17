# Component Routing and Binding Protocol

Use this file before writing `preview.html`. Its job is to prevent freehand UI:
every visible module must be routed to a known layout pattern, a known component
source, or an explicitly declared structural container.

## Core Rule

Do not start HTML until the page has a binding map.

For each visible module, decide:

```json
{
  "module": "checkout footer",
  "raw_phrase": "bottom buy bar",
  "layout_pattern": "detail-view",
  "final_source": "button + section-header-page-layout",
  "instance_name": "checkout-action-bar",
  "variant": "primary button in sticky bottom action area",
  "size": "mobile button height",
  "states": "default,pressed,loading,disabled",
  "token_sources": ["tokens.css", "component-tokens.css", "components.md"],
  "ownership": {
    "layout": "layout-patterns.md detail-view bottom action bar",
    "component_style": "components.md button",
    "interaction": "interaction-patterns.md button state machine"
  },
  "rejected": ["bottom-navigation: peer page switching, not purchase action"]
}
```

No binding map means the design is not ready for L2 generation.

## Legal Component Sources

Use only these values in `data-spec-source`:

| Source | Canonical doc |
|---|---|
| `button` | `design-system/universal/components.md#button` |
| `input-textfield` | `design-system/universal/components.md#input--textfield` |
| `card` | `design-system/universal/components.md#card` |
| `navigation-bar` | `design-system/universal/components.md#navigation-bar-top` |
| `bottom-navigation` | `design-system/universal/components.md#bottom-navigation-mobile` |
| `tab-bar` | `design-system/universal/components.md#tab-bar` |
| `badge-tag` | `design-system/universal/components.md#badge--tag` |
| `toggle-switch` | `design-system/universal/components.md#toggle--switch` |
| `checkbox` | `design-system/universal/components.md#checkbox` |
| `radio-button` | `design-system/universal/components.md#radio-button` |
| `modal-dialog` | `design-system/universal/components.md#modal--dialog` |
| `toast-snackbar` | `design-system/universal/components.md#toast--snackbar` |
| `list-item` | `design-system/universal/components.md#list-item` |
| `section-layout` | `design-system/universal/components.md#section-header--page-layout` |
| `select-dropdown` | `design-system/universal/components.md#select--dropdown` |
| `search-bar` | `design-system/universal/components.md#search-bar` |
| `avatar` | `design-system/universal/components.md#avatar` |
| `progress-bar` | `design-system/universal/components.md#progress-bar` |
| `skeleton-loader` | `design-system/universal/components.md#skeleton-loader` |
| `stepper-steps` | `design-system/universal/components.md#stepper--steps` |
| `bottom-sheet` | `design-system/universal/components.md#bottom-sheet` |
| `structural-container` | `layout-patterns.md`, only for page regions with no component styling of their own |
| `platform-chrome` | `token-exceptions.md`, only for native frame/status/titlebar constants |
| `inline-svg-icon` | `references/icon-policy.md`, only for sourced UI icons using `currentColor` |

`data-component` may be product-specific (`product-card`, `toolbar-title`), but
`data-spec-source` must be one of the legal sources above.

Functional icon leaves additionally require `data-icon-source` and
`data-icon-name` from `references/icon-policy.md`. A legal outer component does
not make an unsourced glyph or CSS-built icon legal.

## Routing Table

| User phrase / module | Route to | Reject |
|---|---|---|
| top title, back, right action, navbar, header | `navigation-bar` | `section-layout` if it navigates |
| bottom tabs, 2-5 peer destinations | `bottom-navigation` | `button`, `tab-bar` |
| buy, submit, pay, confirm, primary CTA | `button` inside `section-layout` or sticky detail action area | `bottom-navigation` |
| category tabs, content switch, segment control | `tab-bar` | `bottom-navigation` unless it switches pages at bottom |
| text entry, search-as-field, form input | `input-textfield` | `search-bar` unless the task is search/discovery |
| search entry, query bar, search results header | `search-bar` | `input-textfield` |
| row in list, message, setting, menu item | `list-item` | `card` if it is a uniform row stream |
| object summary with independent surface | `card` | `list-item` if all rows share one list surface |
| tag, pill, status label, coupon label | `badge-tag` | `button` unless it is clickable action |
| unread count, small count marker | `badge-tag` | decorative dot without semantic state |
| on/off setting | `toggle-switch` | `checkbox` |
| multi-select, checked option | `checkbox` | `inline-svg-icon` alone |
| single-select option | `radio-button` | `checkbox` |
| dropdown, picker, select menu | `select-dropdown` | `modal-dialog` unless blocking |
| blocking confirmation | `modal-dialog` | `toast-snackbar`, `bottom-sheet` |
| short feedback, undo bar | `toast-snackbar` | `modal-dialog` |
| bottom modal sheet, mobile action sheet | `bottom-sheet` | `modal-dialog` if it slides from bottom |
| step process, onboarding progress | `stepper-steps` | decorative timeline |
| progress, loading percent | `progress-bar` | decorative chart |
| profile image, initials circle | `avatar` | generic image |
| loading placeholder | `skeleton-loader` | random grey boxes without loading meaning |

If a phrase matches two routes, decide by task ownership:

- Navigation ownership wins for page movement.
- Form ownership wins for collecting user input.
- Feedback ownership wins for transient messages.
- Layout ownership wins only when no component source owns internal style.

## Binding Gate

Before L2 generation, create a compact internal table:

| Field | Required |
|---|---|
| `module` | Visible region name |
| `page_role` | The job this module does for the user |
| `layout_pattern` | One of the 8 patterns from `layout-patterns.md` |
| `data-component` | Product-specific instance name |
| `data-spec-source` | One legal source from this file |
| `variant / size / state` | Exact values from component specs, or `n/a` for structural containers |
| `tokens` | Token families needed for this module |
| `rejected` | At least one nearby wrong choice for high-risk modules |

High-risk modules require a rejection reason:

- `header`, `footer`, `navbar`, `tabs`, `card`, `form`, `picker`, `modal`,
  `alert`, `tag`, `search`, `table`, `dashboard`, `hero`.

## HTML Requirements

Every visible module must include:

```html
<section
  data-component="product-card"
  data-spec-source="card"
  data-spec-size="auto"
  data-spec-padding="var(--spacing-md)"
  data-spec-states="default,hover">
</section>
```

For purely structural wrappers:

```html
<main
  data-component="page-shell"
  data-spec-source="structural-container"
  data-spec-layout="layout-pattern:list-view">
</main>
```

Do not create new component sources during generation. If a needed component
source is missing, either route it to `structural-container` with no internal
component styling, or stop and record the missing design-system component in
`assumptions.log`.

## Stop Conditions

Stop before HTML and ask for better design-system input when:

- A primary user-facing module cannot be routed to any legal source.
- The requested brand standard conflicts with loaded component specs.
- A component needs a size, state, or variant not present in its source doc.
- The design depends on decorative art, fake data, or visual flourish to look complete.

Do not "make it look nice" by inventing components, gradients, badges, or
illustrations. Use approved references, layout patterns, and component sources.
