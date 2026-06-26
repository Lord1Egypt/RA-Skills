# Islands Architecture & Vue Integration

## Table of Contents
1. [How islands work](#how-islands-work)
2. [Client directives explained](#client-directives)
3. [Choosing the right directive](#choosing-directives)
4. [Vue integration setup](#vue-setup)
5. [Vue component patterns](#vue-patterns)
6. [React and Svelte islands](#other-frameworks)
7. [Common island mistakes](#mistakes)
8. [Advanced patterns](#advanced)

---

## How islands work

Astro's island architecture is its core differentiator. The mental model:

1. **Every component renders to static HTML on the server** (build time for SSG, request time for SSR).
2. **By default, zero JavaScript is shipped for any component.**
3. **Adding a `client:*` directive tells Astro to also ship the JS and hydrate that component.**

This means a page with 20 components but only 2 `client:*` directives ships JS for only those 2 components. The rest are pure HTML.

```
┌──────────────────────────────────────────────┐
│  Page (static HTML shell)                    │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Header   │  │ Article  │  │ Sidebar  │   │
│  │ (static) │  │ (static) │  │ (static) │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  ┌──────────────────┐  ┌─────────────────┐   │
│  │ Search Bar       │  │ Comment Form    │   │
│  │ (island: Vue)    │  │ (island: React) │   │
│  │ client:load      │  │ client:visible  │   │
│  └──────────────────┘  └─────────────────┘   │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Client directives explained

| Directive | When JS loads | When component hydrates | Use case |
|-----------|-------------|----------------------|---------|
| `client:load` | Immediately on page load | As soon as JS loads | Critical interactive UI (nav menus, auth forms) |
| `client:idle` | After page is idle (`requestIdleCallback`) | When browser is idle | Non-critical interactivity (newsletter signup, chat widget) |
| `client:visible` | When component enters viewport | When scrolled into view | Below-fold content (comments, carousels, charts) |
| `client:media="(query)"` | When media query matches | On match | Mobile-only menus, responsive components |
| `client:only="vue"` | Immediately | Client-only (no SSR HTML) | Components that can't SSR (uses `window`, DOM APIs) |

### Hydration flow

```
Server:  Render HTML → Send to browser
Browser: Display HTML immediately (fast!)
         ↓
         Load JS for island (based on directive timing)
         ↓
         Hydrate: Attach event listeners to existing HTML
         ↓
         Component is now interactive
```

**The hydration contract**: The HTML generated on the server must match what the client would render. If they differ, you get hydration mismatch errors.

---

## Choosing the right directive

**Decision flow**:

```
Does the component need interactivity?
├── No  → Don't use any client directive (static HTML)
├── Yes →
│   Is it above the fold / immediately needed?
│   ├── Yes → client:load
│   └── No  →
│       Is it below the fold?
│       ├── Yes → client:visible
│       └── No  →
│           Can it wait until the page is idle?
│           ├── Yes → client:idle
│           └── No  → client:load
│
│   Does it ONLY work in the browser (uses window/document)?
│   └── Yes → client:only="framework"
```

**Performance ranking** (best to worst):
1. No directive (zero JS)
2. `client:visible` (loads only if user scrolls to it)
3. `client:idle` (defers until page is idle)
4. `client:media` (loads only on matching viewport)
5. `client:load` (loads immediately)
6. `client:only` (no SSR HTML + immediate load)

---

## Vue integration setup

### Installation
```bash
npx astro add vue
```

This automatically:
- Installs `@astrojs/vue` and `vue`
- Adds the integration to `astro.config.mjs`

### Manual setup (if needed)
```bash
npm install @astrojs/vue vue
```

```js
// astro.config.mjs
import vue from '@astrojs/vue';

export default defineConfig({
  integrations: [
    vue({
      appEntrypoint: '/src/pages/_app',  // Optional: custom app setup
      jsx: false,                         // Enable JSX in Vue if needed
    }),
  ],
});
```

### Custom app entrypoint (for plugins, stores)
```ts
// src/pages/_app.ts
import type { App } from 'vue';
import { createPinia } from 'pinia';

export default (app: App) => {
  app.use(createPinia());
  // Register global components, directives, etc.
};
```

---

## Vue component patterns

### Basic Vue island
```vue
<!-- src/components/Counter.vue -->
<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  initialCount?: number;
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 0,
});

const count = ref(props.initialCount);
</script>

<template>
  <div class="counter">
    <button @click="count--">-</button>
    <span>{{ count }}</span>
    <button @click="count++">+</button>
  </div>
</template>
```

Using it in Astro:
```astro
---
import Counter from '../components/Counter.vue';
---

<!-- Static: renders HTML but buttons won't work -->
<Counter initialCount={5} />

<!-- Interactive: buttons work after hydration -->
<Counter client:load initialCount={5} />
```

### Props serialization rules

Props passed from Astro to framework islands are serialized (converted to JSON). This means:

**Works** (serializable):
- Strings, numbers, booleans
- Arrays, plain objects
- `null`, `undefined`
- Dates (serialized as ISO strings)

**Does NOT work** (not serializable):
- Functions, callbacks
- Class instances
- Symbols
- Circular references
- Reactive Vue refs/computed

```astro
---
import MyVue from '../components/MyVue.vue';

// GOOD: plain data
const items = [{ id: 1, name: 'First' }];

// BAD: functions can't cross the boundary
const onClick = () => console.log('nope');
---

<MyVue client:load items={items} />
<!-- <MyVue client:load onClick={onClick} /> ← This won't work -->
```

### Composables and state management

Vue composables work normally inside hydrated islands:

```vue
<!-- src/components/SearchBar.vue -->
<script setup>
import { ref, watch } from 'vue';
import { useDebounceFn } from '@vueuse/core'; // VueUse works

const query = ref('');
const results = ref([]);

const search = useDebounceFn(async (q) => {
  if (!q) { results.value = []; return; }
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
  results.value = await res.json();
}, 300);

watch(query, (q) => search(q));
</script>

<template>
  <input v-model="query" placeholder="Search..." />
  <ul v-if="results.length">
    <li v-for="r in results" :key="r.id">{{ r.title }}</li>
  </ul>
</template>
```

### Pinia stores across islands

Each island is an independent Vue app. Pinia stores are NOT shared between islands by default.

If you need shared state between Vue islands, use:
1. **Custom events** (`window.dispatchEvent` / `addEventListener`)
2. **Shared external store** (nanostores — works across any framework)
3. **URL state** (query params, hash)

```ts
// src/stores/cart.ts — using nanostores (framework-agnostic)
import { atom, map } from 'nanostores';

export const $cartItems = map<Record<string, number>>({});
export const $cartCount = atom(0);

export function addToCart(id: string) {
  const items = $cartItems.get();
  $cartItems.setKey(id, (items[id] || 0) + 1);
  $cartCount.set(Object.values($cartItems.get()).reduce((a, b) => a + b, 0));
}
```

---

## React and Svelte islands

The same patterns apply. Install the integration, add `client:*` directives.

```bash
npx astro add react
npx astro add svelte
```

**Mixing frameworks on the same page is fully supported**:
```astro
---
import VueCounter from '../components/Counter.vue';
import ReactChart from '../components/Chart.tsx';
import SvelteToggle from '../components/Toggle.svelte';
---

<VueCounter client:load />
<ReactChart client:visible data={chartData} />
<SvelteToggle client:idle />
```

Each island hydrates independently. They share no runtime state (unless using nanostores or similar).

---

## Common island mistakes

### 1. Forgetting the client directive
```astro
<!-- Bug: renders HTML but nothing is interactive -->
<Counter />

<!-- Fix: add the appropriate directive -->
<Counter client:load />
```
This is the #1 Astro support question. The component renders HTML fine but click handlers, reactive state, and lifecycle hooks don't run.

### 2. Using client:only when you don't need to
```astro
<!-- Avoid: No SSR HTML, shows blank until JS loads -->
<HeroSection client:only="vue" />

<!-- Better: SSR HTML shows immediately, then hydrates -->
<HeroSection client:load />
```
Only use `client:only` when the component truly cannot render on the server (uses `window`, `document`, canvas, WebGL, etc.).

### 3. Hydration mismatch errors
The server HTML must match the client render. Common causes:
- **Dates/timestamps**: Server and client format differently
- **Random values**: `Math.random()` in render
- **Conditional rendering based on `window`**: Server has no `window`
- **Browser-only APIs in template**: `localStorage.getItem()` in template

Fix: Move browser-only logic to `onMounted` (Vue) or `useEffect` (React):
```vue
<script setup>
import { ref, onMounted } from 'vue';

const theme = ref('light'); // Safe default for SSR

onMounted(() => {
  theme.value = localStorage.getItem('theme') || 'light';
});
</script>
```

### 4. Over-hydrating the page
If every component has `client:load`, you've defeated Astro's purpose. Audit:
- Does this component actually need JS? (Maybe it's just displaying data)
- Can it use `client:visible` instead of `client:load`?
- Can the interactive part be extracted into a smaller island?

### 5. Passing non-serializable props
```astro
---
// Bug: functions can't be serialized across the island boundary
const handleClick = () => alert('hi');
---
<MyVue client:load onClick={handleClick} />
```
Move the handler inside the Vue component instead.

---

## Advanced patterns

### Nested islands
An Astro component can contain multiple islands. An island can contain Astro children via slots:

```astro
---
import VueWrapper from '../components/Wrapper.vue';
import StaticContent from '../components/StaticContent.astro';
---

<VueWrapper client:load>
  <!-- This static content is passed as a slot -->
  <StaticContent />
</VueWrapper>
```

But a hydrated island cannot contain another hydrated island from a different framework. Keep islands flat.

### Island communication
Use custom events for cross-island communication:

```vue
<!-- Island A: emits event -->
<script setup>
function notify() {
  window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: 5 } }));
}
</script>
```

```vue
<!-- Island B: listens for event -->
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

const count = ref(0);
function handler(e) { count.value = e.detail.count; }

onMounted(() => window.addEventListener('cart-updated', handler));
onUnmounted(() => window.removeEventListener('cart-updated', handler));
</script>
```

### Lazy-loading heavy islands
Combine `client:visible` with dynamic imports for code-splitting:

```astro
---
// The Vue component JS only loads when scrolled into view
import HeavyChart from '../components/HeavyChart.vue';
---
<HeavyChart client:visible data={bigDataset} />
```

Astro automatically code-splits each island, so each `client:visible` component only downloads its JS when triggered.
