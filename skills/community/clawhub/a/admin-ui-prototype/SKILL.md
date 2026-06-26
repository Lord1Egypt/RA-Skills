---
name: admin-ui-prototype
description: Query project-specific Arco Design usage patterns and generate Vue 3 admin page prototypes with mock data, scaffold files, and route snippets. Use when Codex needs to answer how a component is used in this admin UI, draft a list/form/detail/dashboard/empty-state page, or bootstrap/update a minimal `webui/admin-ui` preview project.
---

# Admin UI Prototype

Use this skill for two tasks:

- Look up how Arco Design components are used in this admin UI.
- Generate a runnable Vue 3 admin page prototype with realistic mock data.

## Load only what is needed

- Read `knowledge/components/README.md` first to locate component docs.
- Read only the component docs needed for the request.
- Read `knowledge/ui-conventions.md` for page structure, naming, and styling rules.
- Read `knowledge/page-templates.md` for ready-made page and route templates.
- Read `knowledge/scaffold.md` only when `webui/admin-ui` needs to be initialized.

## Answer component-usage questions

1. Read `knowledge/components/README.md`.
2. Open the matching component docs under `knowledge/components/`.
3. Open `knowledge/ui-conventions.md` if layout or page-level context matters.
4. Answer with project conventions and concrete patterns from the bundled docs, not generic framework advice.
5. If a new pattern is discovered from real project code, append it to the relevant component doc and update the component index when a new component is added. Never store secrets.

## Generate a page prototype

1. Parse the request into:
   - page type
   - business entity
   - fields to show or edit
   - filters and table actions
   - special interactions such as batch actions, tabs, charts, or nested forms
2. If missing details would materially change the layout or data model, ask a short clarifying question. Otherwise make reasonable assumptions.
3. Read `knowledge/ui-conventions.md`.
4. Read `knowledge/page-templates.md`.
5. Read only the component docs required for the page type:

| Page type | Required docs |
|---|---|
| List | `table.md`, `form.md`, `button.md`, `modal.md`, `tag.md`, `space.md`, `grid.md` |
| Form | `form.md`, `input.md`, `select.md`, `date-picker.md`, `checkbox.md`, `radio.md`, `divider.md` |
| Detail | `descriptions.md`, `card.md`, `tag.md`, `button.md` |
| Dashboard | `statistic.md`, `card.md`, `grid.md` |
| Modal form | `modal.md`, `form.md`, `input.md`, `select.md`, `spin.md`, `feedback-api.md` |

## Initialize or update the preview project

- If `webui/admin-ui/package.json` does not exist:
  - follow `knowledge/scaffold.md`
  - create the scaffold files under `webui/admin-ui`
  - replace `{{pageTitle}}`, `{{viewImportPath}}`, and `{{ViewComponent}}`
  - run `pnpm install` in `webui/admin-ui`
- If the preview project already exists:
  - update `webui/admin-ui/src/App.vue`
  - update `webui/admin-ui/index.html`

## Output requirements

- Create the main page at `webui/admin-ui/src/views/{kebab-case-module}/index.vue`.
- Create child components under `webui/admin-ui/src/views/{kebab-case-module}/components/` when the page benefits from splitting dialogs or sections.
- Provide the route snippet from `knowledge/page-templates.md`.
- Keep the output runnable with mock data unless the user explicitly asks for API wiring only.

## Generation rules

1. Use `<script setup lang="ts">`.
2. Include runnable mock data with at least 5 records when the page type needs a dataset.
3. Wrap mock loading in `mockFetch` with a 300 ms timeout for list-like data flows.
4. Add `// TODO: 替换为真实 API 调用` at each mock or placeholder API call.
5. Use Arco Design Vue components for interaction controls.
6. Use CSS variables such as `var(--color-*)` instead of hard-coded colors.
7. Use scoped LESS styles.
8. Use snake_case in DTO fields to stay aligned with backend APIs, and camelCase for frontend variables.
9. Keep UI copy in Chinese unless the user asks for another language.
10. Default the page file to `src/views/{kebab-case-module}/index.vue`.

## Final response

- List the generated files.
- Mention whether the scaffold was created or reused.
- Include the route registration snippet.
- Call out the remaining `// TODO` placeholders.
- Start `pnpm dev` and share the local URL only when the user asks for a preview or when local validation is required.
