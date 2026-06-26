# Framework Adapters

How to apply agent-friendly transformations per framework.

## Table of Contents
- [React (JSX/TSX)](#react-jsx--tsx)
- [Vue (SFC)](#vue-sfc)
- [Svelte](#svelte)
- [General Rules](#general-rules)

---

## React (JSX / TSX)

### Syntax mapping
| HTML | JSX |
|------|-----|
| `class` | `className` |
| `for` | `htmlFor` |
| `tabindex` | `tabIndex` |
| `aria-*` | `aria-*` (same) |
| `data-*` | `data-*` (same) |

### data-testid
```jsx
<button data-testid="submit-btn" onClick={handleSubmit}>Submit</button>

// Component that forwards props
<SearchBar data-testid="search-bar" />

// Component that doesn't forward — wrap
<div data-testid="search-bar-container">
  <SearchBar />
</div>
```

### JSON-LD
```jsx
<Head>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{
      __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title
      })
    }}
  />
</Head>
```

### Considerations
- Don't add `aria-label` to non-DOM components
- ARIA booleans: `aria-expanded={isOpen ? "true" : "false"}` (string, not boolean)
- Keep `key` props untouched
- Don't modify `ref` callbacks

---

## Vue (SFC)

### Template syntax
```vue
<template>
  <button data-testid="submit-btn" @click="handleSubmit">Submit</button>

  <!-- Dynamic ARIA -->
  <button :aria-expanded="isOpen.toString()" :aria-controls="panelId">Toggle</button>

  <!-- v-for with data-testid -->
  <li v-for="item in items" :key="item.id"
      :data-testid="`item-${item.id}`"
      :data-entity-id="item.id" data-entity-type="product">
    {{ item.name }}
  </li>
</template>
```

### JSON-LD (Nuxt / @vueuse/head)
```vue
<script setup>
useHead({
  script: [{
    type: 'application/ld+json',
    innerHTML: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": props.title
    })
  }]
})
</script>
```

### Considerations
- Don't modify `v-model`, `v-if`, `v-show`, `v-for` logic
- Use `:aria-expanded` (v-bind) for dynamic states
- Don't interfere with `<slot>` definitions
- Don't modify `defineProps`, `defineEmits`

---

## Svelte

### Template syntax
```svelte
<button data-testid="submit-btn" on:click={handleSubmit}>Submit</button>

<!-- Dynamic ARIA -->
<button aria-expanded={isOpen ? 'true' : 'false'} aria-controls="panel-1">Toggle</button>

<!-- Each with data-testid -->
{#each items as item (item.id)}
  <li data-testid="item-{item.id}" data-entity-id={item.id} data-entity-type="product">
    {item.name}
  </li>
{/each}
```

### JSON-LD
```svelte
<svelte:head>
  {@html `<script type="application/ld+json">${JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": title
  })}</script>`}
</svelte:head>
```

### Considerations
- Don't modify `bind:` directives
- Don't change `{#if}`, `{#each}`, `{#await}` blocks
- Use string values for ARIA: `'true'`/`'false'`
- Don't modify `$:` reactive declarations
- Don't interfere with `<slot>` elements

---

## General Rules

**Do:**
- Add `data-testid` directly on HTML elements
- Use framework's head management for JSON-LD
- Keep ARIA values as strings "true"/"false"
- Preserve all existing attributes, directives, event handlers
- Match existing code style

**Don't:**
- Add HTML attributes to abstract components that don't render DOM
- Modify state management, lifecycle hooks, or logic
- Change import statements or add dependencies
- Modify CSS/style blocks
- Wrap elements in new containers unless necessary for semantics
- Touch framework config files
