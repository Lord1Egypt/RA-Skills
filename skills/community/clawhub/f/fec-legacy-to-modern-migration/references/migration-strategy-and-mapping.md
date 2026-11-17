# Migration strategy and concept mapping

## Migration strategy selection

| Strategy | Applicability | Advantages | Risks |
| --------------------------- | ------------------------------------ | ---------------------------- | ---------------------------- |
| **Progressive (Strangler Fig)** | Large-scale projects, requiring continuous delivery, and insufficient team familiarity | Risks are controllable, can be launched in batches, and can be rolled back | Old and new coexist for a long time, and two sets of codes need to be maintained |
| **One-time rewrite** | Small and medium-sized projects, stable business, sufficient time window | Clear target architecture, no historical baggage | Long cycle, high pressure to go online, difficult rollback |

**Recommendation**: Prioritize the incremental approach unless the project is small and the business is simple.

## Concept mapping

### jQuery → React

| Legacy Patterns | React Correspondence |
| ------------------------------------------ | -------------------------------------- |
| `$(selector).html(content)` | Declarative JSX + state-driven rendering |
| `$(document).on('click', '.btn', handler)` | `onClick` + event delegation is handled by React |
| `$.ajax()` / `$.get()` | Project request layer, `fetch` / `axios`, can be connected to TanStack Query or SWR on demand |
| Global variables/namespace storage state | Local state, Context or the existing store of the project can be used as needed Zustand/Redux |
| `$(el).show()` / `$(el).hide()` | Conditional rendering `{visible && <Component />}` |
| Manual DOM operations `append` / `remove` | Data-driven, triggering re-rendering through setState |
| Template string concatenation HTML | JSX component + props |
| Multiple pages + server-side routing | React Router client-side routing |

### jQuery → Vue 3

| Legacy Mode | Vue 3 Compatibility |
| ------------------------------------------ | -------------------------------------------------- |
| `$(selector).html(content)` | Template + `ref` / `reactive` driven rendering |
| `$(document).on('click', '.btn', handler)` | `@click` + event modifier |
| `$.ajax()` / `$.get()` | Project request layer, `fetch` / `axios`, can be connected to VueUse, Nuxt `useFetch` or TanStack Query Vue adapter as needed |
| Global variables / Namespace storage state | `ref` / `reactive` / Pinia |
| `$(el).show()` / `$(el).hide()`            | `v-show` / `v-if`                                  |
| Manual DOM manipulation | Data-driven, with responsive view updates |
| Template string concatenation HTML | Single file component `<template>` + props |
| Multiple pages + server-side routing | Vue Router client-side routing |

### Universal mapping

| Legacy Concepts | Modern Correspondence |
| --------------------------------- | ------------------------------------------ |
| Page-level JS entry (one script per page) | Routing/page entry + lazy loading module, or retain MPA entry and modernize packaging |
| Public JS modules (utils, ajax packaging) | `services/`, `utils/`, typed API layer |
| Inline styles / page-level CSS | Target project style system, such as CSS Modules, Tailwind, global style layering or component library styles |
| Server-side template variables | Obtain via API, SSR/loader injection, or preserve server-side template boundaries and typed data |
| Form submission + full page refresh | Form library + client verification + API call |
