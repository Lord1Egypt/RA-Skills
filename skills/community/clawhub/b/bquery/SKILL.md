---
name: bquery
description: Use this skill when working with @bquery/bquery, bQuery apps, or the bQuery ecosystem. It helps the agent choose the right bQuery module, write idiomatic code, and use the library across core DOM APIs, reactivity, concurrency workers, Web Components, motion, security, platform helpers, router, store, declarative views, forms, i18n, accessibility, drag-and-drop, media observers, plugins, devtools, testing, Storybook, and SSR.
version: 1.0.0
metadata: {"openclaw":{"emoji":"🧩","homepage":"https://bquery.flausch-code.de/"}}
---

# bQuery Skill

Use this skill whenever a task involves `@bquery/bquery`.

bQuery is a modular, TypeScript-first, zero-build-capable browser library
that combines jQuery-style DOM ergonomics with signals, async workflows,
Web Components, motion, routing, stores, declarative views, forms,
accessibility helpers, media observers, plugins, devtools, testing, and
SSR.

Current documented baseline to keep in mind:

- `watchDebounce()` and `watchThrottle()` are public reactive APIs
- `bq-error` and `bq-aria` are part of the view surface
- `useIntersectionObserver()`, `useResizeObserver()`, and
  `useMutationObserver()` are public media composables
- the concurrency module includes worker helpers, RPC helpers, pools,
  reactive worker wrappers, and higher-level helpers like `parallel()`,
  `batchTasks()`, `map()`, `filter()`, `reduce()`, and `pipeline()`

## When to use this skill

Activate this skill when any of the following are true:

- `package.json` includes `@bquery/bquery`
- imports use `@bquery/bquery` or subpaths like:
  - `@bquery/bquery/core`
  - `@bquery/bquery/reactive`
  - `@bquery/bquery/component`
  - `@bquery/bquery/view`
- the user mentions:
  - bQuery
  - `bq-*` directives
  - signals
  - Web Components
  - zero-build browser apps
  - bQuery router/store/forms/motion/testing/SSR
- the repository already uses bQuery conventions

## Primary rules

1. Prefer TypeScript unless the repository is clearly plain JavaScript.
2. Prefer subpath imports over the root bundle.
3. Use the smallest bQuery module that solves the task.
4. Prefer browser-native patterns over framework-specific abstractions.
5. Add cleanup for effects, watchers, observers, sockets, workers, and
   listeners where relevant.
6. Sanitize untrusted HTML before rendering it.
7. If using the `view` module, mention CSP implications:
   the view evaluator uses `new Function()` and requires `unsafe-eval`.
8. Be accessibility-aware by default.
9. Respect reduced motion for non-trivial animation.
10. Do not add React/Vue/Svelte unless the user explicitly asks.

## Import strategy

Prefer targeted imports:

```ts
import { $, $$ } from '@bquery/bquery/core';
import {
  signal,
  computed,
  effect,
  watch,
  watchDebounce,
  watchThrottle,
} from '@bquery/bquery/reactive';
import { component, html } from '@bquery/bquery/component';
```

Use the root entry only for broad demos:

```ts
import {
  $,
  signal,
  component,
  registerDefaultComponents,
} from '@bquery/bquery';
```

## Module chooser

| Need | Use |
| --- | --- |
| DOM selection, traversal, classes, attrs, events | `@bquery/bquery/core` |
| Signals, computed values, effects, async data, HTTP, sockets | `@bquery/bquery/reactive` |
| Worker tasks, RPC workers, pools, pipelines | `@bquery/bquery/concurrency` |
| Web Components | `@bquery/bquery/component` |
| Storybook helpers | `@bquery/bquery/storybook` |
| Animation and transitions | `@bquery/bquery/motion` |
| Sanitization, Trusted Types, CSP helpers | `@bquery/bquery/security` |
| Storage, cookies, page meta, announcers | `@bquery/bquery/platform` |
| SPA routing | `@bquery/bquery/router` |
| App-level state | `@bquery/bquery/store` |
| Declarative DOM with `bq-*` directives | `@bquery/bquery/view` |
| Form state and validation | `@bquery/bquery/forms` |
| Internationalization | `@bquery/bquery/i18n` |
| Focus and keyboard UX | `@bquery/bquery/a11y` |
| Drag and drop | `@bquery/bquery/dnd` |
| Viewport, clipboard, observers, device/browser signals | `@bquery/bquery/media` |
| Plugins/custom directives | `@bquery/bquery/plugin` |
| Debugging helpers | `@bquery/bquery/devtools` |
| Test helpers | `@bquery/bquery/testing` |
| Server rendering and hydration | `@bquery/bquery/ssr` |

## Module guidance

### Core

Use `core` for direct DOM work:

- `$()`, `$$()`
- traversal and manipulation
- event binding and delegation
- `css()` getter/setter
- `is(selector)`
- `find(selector)`
- utilities like `debounce()`, `throttle()`, `uid`, `merge`, `once`

Prefer this for:

- progressive enhancement
- small widgets
- DOM-heavy tasks without a component or view layer

### Reactive

Use `reactive` for state and async workflows:

- `signal()`, `computed()`, `effect()`, `batch()`
- `watch()`, `watchDebounce()`, `watchThrottle()`
- `linkedSignal()`, `persistedSignal()`, `readonly()`
- `useAsyncData()`, `useFetch()`, `createUseFetch()`
- `createHttp()`, `http`
- `usePolling()`
- `usePaginatedFetch()`, `useInfiniteFetch()`
- `useWebSocket()`, `useWebSocketChannel()`
- `useEventSource()`
- `useResource()`, `useResourceList()`
- `useSubmit()`
- `createRestClient()`
- `createRequestQueue()`
- `deduplicateRequest()`

Important reminder:
`watchDebounce()` and `watchThrottle()` should be treated like `watch()`
with the same cleanup-safe callback style.

### Concurrency

Use `concurrency` for CPU-heavy work or isolated execution:

- `runTask()`
- `createTaskWorker()`, `createTaskPool()`
- `createRpcWorker()`, `createRpcPool()`
- `createReactiveTaskWorker()`, `createReactiveTaskPool()`
- `createReactiveRpcWorker()`, `createReactiveRpcPool()`
- `callWorkerMethod()`
- `batchTasks()`
- `parallel()`, `pipeline()`
- `map()`, `filter()`, `reduce()`, `find()`, `every()`, `some()`
- `getConcurrencySupport()`

Prefer this for:

- parsing
- indexing
- transforms
- large collections
- worker-monitored UI workloads

Do not use worker orchestration for tiny UI-only tasks.

### Component

Use `component` for reusable Web Components:

- `component(tag, def)`
- `defineComponent(tag, def)`
- `html`
- `safeHtml`
- `bool()`
- `registerDefaultComponents()`

Prefer this for:

- design-system primitives
- reusable widgets
- shadow DOM components
- framework-agnostic distribution

### Motion

Use `motion` for browser-native animation:

- `animate()`
- `transition()`
- `flip()`, `flipElements()`, `flipList()`
- `spring()`
- `timeline()`, `sequence()`
- `stagger()`
- `scrollAnimate()`
- `prefersReducedMotion()`

Always account for reduced motion.

### Security

Use `security` whenever HTML is dynamic:

- `sanitize()`, `sanitizeHtml()`
- `trusted()`
- `escapeHtml()`
- `stripTags()`
- nonce/CSP helpers
- Trusted Types helpers

Hard rule:
never inject untrusted HTML without sanitizing it first.

### Router

Use `router` for SPA navigation:

- `createRouter()`
- `navigate()`
- `back()`, `forward()`
- `currentRoute`
- `link()`
- `interceptLinks()`
- `resolve()`

### Store

Use `store` for app-level state:

- `createStore()`
- `defineStore()`
- `createPersistedStore()`
- `mapState`, `mapGetters`, `mapActions`
- `watchStore()`

Store patterns commonly include:

- `$state`
- `$reset`
- `$patch`
- `$patchDeep`
- `$subscribe`
- `$onAction`

### View

Use `view` for declarative HTML binding:

- `mount()`
- `createTemplate()`
- `clearExpressionCache()`

Current directive surface to remember includes:

- `bq-text`
- `bq-html`
- `bq-if`
- `bq-for`
- `bq-model`
- `bq-class`
- `bq-style`
- `bq-show`
- `bq-bind`
- `bq-on:event`
- `bq-error`
- `bq-aria`

Important:
the view module uses `new Function()` internally. Mention that strict CSP
setups need `unsafe-eval`.

### Forms, i18n, a11y, dnd, media

Use:

- `createForm()` and validators from `forms`
- `createI18n()` from `i18n`
- `trapFocus()`, `releaseFocus()`, `rovingTabIndex()` from `a11y`
- `draggable()`, `droppable()`, `sortable()` from `dnd`
- `mediaQuery()`, `useViewport()`, `clipboard`
- `useIntersectionObserver()`, `useResizeObserver()`,
  `useMutationObserver()` from `media`

## Canonical patterns

### 1. DOM enhancement

```ts
import { $, $$ } from '@bquery/bquery/core';

$('#save').on('click', () => {
  console.log('Saved');
});

$('#list').delegate('click', '.item', (_event, target) => {
  $(target).toggleClass('active');
});

$('#box').addClass('ready').css({ opacity: '0.85' });

if ($('#box').is('.ready')) {
  console.log($('#box').css('opacity'));
}

$$('.container').find('.item').addClass('found');
```

### 2. Signals and debounced search

```ts
import {
  computed,
  effect,
  signal,
  useFetch,
  watchDebounce,
} from '@bquery/bquery/reactive';

const query = signal('');
const page = signal(1);

const normalizedQuery = computed(() => query.value.trim());

const results = useFetch<{ items: string[]; total: number }>(
  () =>
    `/search?q=${encodeURIComponent(normalizedQuery.value)}&page=${
      page.value
    }`,
  {
    baseUrl: 'https://api.example.com',
    watch: [query, page],
  }
);

watchDebounce(
  query,
  () => {
    page.value = 1;
  },
  250
);

effect(() => {
  console.log(results.pending.value);
  console.log(results.data.value);
  console.log(results.error.value);
});
```

### 3. Worker offloading

```ts
import {
  createReactiveTaskPool,
  parallel,
} from '@bquery/bquery/concurrency';

const pool = createReactiveTaskPool(
  ({ value }: { value: number }) => value * 2,
  { size: 4 }
);

const output = await parallel(
  [1, 2, 3, 4].map((value) => () => pool.run({ value }))
);

console.log(output);
console.log(pool.pending$.value);
```

### 4. Web Component with safe HTML

```ts
import {
  bool,
  component,
  safeHtml,
} from '@bquery/bquery/component';
import { sanitizeHtml, trusted } from '@bquery/bquery/security';

const badge = trusted(sanitizeHtml('<span class="badge">Active</span>'));

component('user-card', {
  props: {
    username: { type: String, required: true },
  },
  state: {
    disabled: false,
  },
  render({ props, state }) {
    return safeHtml`
      <button class="user-card" ${bool('disabled', state.disabled)}>
        ${badge}
        <span>Hello ${props.username}</span>
      </button>
    `;
  },
});
```

### 5. Declarative view with `bq-error` and `bq-aria`

```html
<section id="profile-form">
  <input
    id="email"
    bq-model="email"
    bq-aria="{ invalid: fieldState.value.invalid, 'aria-describedby': fieldState.value.describedBy }"
    type="email"
  />
  <p id="email-error" bq-error="formError"></p>
  <button bq-on:click="submit">Save</button>
</section>
```

```ts
import { mount } from '@bquery/bquery/view';
import { signal } from '@bquery/bquery/reactive';

const email = signal('');
const formError = signal('');
const fieldState = signal({
  invalid: false,
  describedBy: '',
});

mount('#profile-form', {
  email,
  formError,
  fieldState,
  submit: () => {
    const value = email.value.trim();
    const invalid = !value.includes('@');

    formError.value = invalid ? 'Please enter a valid email address.' : '';
    fieldState.value = {
      invalid,
      describedBy: invalid ? 'email-error' : '',
    };
  },
});
```

Note:
if this is used in a strict CSP environment, mention that `@bquery/bquery/view`
needs `unsafe-eval`.

## Response policy

When answering bQuery questions:

- explain which bQuery module you chose and why
- keep imports minimal
- prefer subpath imports
- preserve zero-build/browser-native patterns where appropriate
- mention cleanup for observers, workers, sockets, and effects
- mention accessibility for interactive UI
- mention reduced motion for animations
- mention sanitization for dynamic HTML
- mention CSP implications when using the `view` module
- consider concurrency for CPU-heavy work, not trivial work

## Anti-patterns to avoid

Do not:

- import the full root bundle by default
- inject untrusted HTML directly
- use `bq-html` with unsafe user content
- forget cleanup for long-lived reactive resources
- ignore keyboard and screen-reader behavior
- use workers where normal reactive code is enough
- add another framework to solve problems bQuery already solves
- omit CSP guidance when using `@bquery/bquery/view`

## Good defaults

If the task is vague, prefer:

- `core` for small DOM tasks
- `reactive` for stateful UI
- `component` for reusable widgets
- `view` for declarative plain-HTML binding
- `forms` for structured validation
- `router` + `store` for SPA structure
- `security` for any dynamic HTML
- `media` for observer-driven behavior
- `concurrency` only when heavy work justifies it

## One-line summary

Use bQuery as a modular, browser-native toolkit: choose the smallest
module, prefer subpath imports, use signals and Web Components
idiomatically, sanitize dynamic HTML, document CSP constraints for the
view layer, and include accessibility, cleanup, and reduced-motion
behavior by default.
