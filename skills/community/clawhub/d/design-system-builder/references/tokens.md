# Design Tokens Reference

## Table of Contents
1. [Token Philosophy](#token-philosophy)
2. [Token Categories & Schema](#token-categories--schema)
3. [Naming Conventions](#naming-conventions)
4. [Style Dictionary Setup](#style-dictionary-setup)
5. [CSS Custom Properties Output](#css-custom-properties-output)
6. [JS/TS Constants Output](#jsts-constants-output)
7. [Multi-Brand Tokens](#multi-brand-tokens)

---

## Token Philosophy

Tokens exist in **two layers**:

| Layer | Purpose | Examples |
|---|---|---|
| **Primitive** | Raw values, full palette | `color.blue.500 = #3b82f6` |
| **Semantic** | Intent-based aliases | `color.primary = {color.blue.500}` |

**Rule:** Components always consume **semantic tokens**. Never reference primitive tokens directly in component code.

```
Design Decision → Primitive Token → Semantic Token → Component
"Brand blue"      blue-500          primary          <Button>
```

---

## Token Categories & Schema

### Color Tokens

**Primitives** (`packages/tokens/src/primitives/color.json`):
```json
{
  "color": {
    "blue": {
      "50":  { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "200": { "value": "#bfdbfe" },
      "300": { "value": "#93c5fd" },
      "400": { "value": "#60a5fa" },
      "500": { "value": "#3b82f6" },
      "600": { "value": "#2563eb" },
      "700": { "value": "#1d4ed8" },
      "800": { "value": "#1e40af" },
      "900": { "value": "#1e3a8a" }
    },
    "gray": { "...": "50–950 steps" },
    "red": { "...": "50–900 steps" },
    "green": { "...": "50–900 steps" }
  }
}
```

**Semantic** (`packages/tokens/src/semantic/color.json`):
```json
{
  "color": {
    "primary": {
      "default":  { "value": "{color.blue.600}" },
      "hover":    { "value": "{color.blue.700}" },
      "active":   { "value": "{color.blue.800}" },
      "disabled": { "value": "{color.blue.300}" },
      "subtle":   { "value": "{color.blue.50}" }
    },
    "neutral": {
      "text": {
        "primary":   { "value": "{color.gray.900}" },
        "secondary": { "value": "{color.gray.600}" },
        "disabled":  { "value": "{color.gray.400}" },
        "inverse":   { "value": "{color.gray.50}" }
      },
      "bg": {
        "base":    { "value": "{color.gray.50}" },
        "subtle":  { "value": "{color.gray.100}" },
        "muted":   { "value": "{color.gray.200}" }
      },
      "border": {
        "default": { "value": "{color.gray.200}" },
        "strong":  { "value": "{color.gray.400}" }
      }
    },
    "feedback": {
      "error":   { "default": { "value": "{color.red.600}" }, "subtle": { "value": "{color.red.50}" } },
      "warning": { "default": { "value": "{color.yellow.500}" }, "subtle": { "value": "{color.yellow.50}" } },
      "success": { "default": { "value": "{color.green.600}" }, "subtle": { "value": "{color.green.50}" } },
      "info":    { "default": { "value": "{color.blue.600}" }, "subtle": { "value": "{color.blue.50}" } }
    }
  }
}
```

### Typography Tokens

```json
{
  "font": {
    "family": {
      "sans":  { "value": "'Inter', system-ui, -apple-system, sans-serif" },
      "mono":  { "value": "'JetBrains Mono', 'Fira Code', monospace" }
    },
    "size": {
      "xs":   { "value": "0.75rem" },
      "sm":   { "value": "0.875rem" },
      "md":   { "value": "1rem" },
      "lg":   { "value": "1.125rem" },
      "xl":   { "value": "1.25rem" },
      "2xl":  { "value": "1.5rem" },
      "3xl":  { "value": "1.875rem" },
      "4xl":  { "value": "2.25rem" }
    },
    "weight": {
      "regular":   { "value": "400" },
      "medium":    { "value": "500" },
      "semibold":  { "value": "600" },
      "bold":      { "value": "700" }
    },
    "lineHeight": {
      "tight":   { "value": "1.25" },
      "snug":    { "value": "1.375" },
      "normal":  { "value": "1.5" },
      "relaxed": { "value": "1.625" }
    },
    "letterSpacing": {
      "tight":  { "value": "-0.025em" },
      "normal": { "value": "0em" },
      "wide":   { "value": "0.025em" }
    }
  }
}
```

### Spacing Tokens

Use a **4px base** grid:

```json
{
  "spacing": {
    "0":   { "value": "0" },
    "1":   { "value": "0.25rem" },
    "2":   { "value": "0.5rem" },
    "3":   { "value": "0.75rem" },
    "4":   { "value": "1rem" },
    "5":   { "value": "1.25rem" },
    "6":   { "value": "1.5rem" },
    "8":   { "value": "2rem" },
    "10":  { "value": "2.5rem" },
    "12":  { "value": "3rem" },
    "16":  { "value": "4rem" },
    "20":  { "value": "5rem" },
    "24":  { "value": "6rem" }
  }
}
```

### Border Radius Tokens

```json
{
  "borderRadius": {
    "none":  { "value": "0" },
    "sm":    { "value": "0.125rem" },
    "md":    { "value": "0.375rem" },
    "lg":    { "value": "0.5rem" },
    "xl":    { "value": "0.75rem" },
    "2xl":   { "value": "1rem" },
    "full":  { "value": "9999px" }
  }
}
```

### Shadow Tokens

```json
{
  "shadow": {
    "xs":  { "value": "0 1px 2px 0 rgb(0 0 0 / 0.05)" },
    "sm":  { "value": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)" },
    "md":  { "value": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)" },
    "lg":  { "value": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)" },
    "xl":  { "value": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)" }
  }
}
```

### Motion Tokens

```json
{
  "motion": {
    "duration": {
      "fast":    { "value": "100ms" },
      "normal":  { "value": "200ms" },
      "slow":    { "value": "300ms" },
      "slower":  { "value": "500ms" }
    },
    "easing": {
      "default":    { "value": "cubic-bezier(0.4, 0, 0.2, 1)" },
      "in":         { "value": "cubic-bezier(0.4, 0, 1, 1)" },
      "out":        { "value": "cubic-bezier(0, 0, 0.2, 1)" },
      "spring":     { "value": "cubic-bezier(0.34, 1.56, 0.64, 1)" }
    }
  }
}
```

### Z-Index Tokens

```json
{
  "zIndex": {
    "hide":     { "value": "-1" },
    "base":     { "value": "0" },
    "raised":   { "value": "1" },
    "dropdown": { "value": "1000" },
    "sticky":   { "value": "1100" },
    "overlay":  { "value": "1200" },
    "modal":    { "value": "1300" },
    "popover":  { "value": "1400" },
    "toast":    { "value": "1500" },
    "tooltip":  { "value": "1600" }
  }
}
```

---

## Naming Conventions

Pattern: `{category}.{variant}.{state}` or `{category}.{scale}`

| Good | Bad |
|---|---|
| `color.primary.default` | `primaryColor` |
| `color.neutral.text.secondary` | `grayText` |
| `spacing.4` | `spaceMedium` |
| `shadow.md` | `boxShadowCard` |

**Key rules:**
- Lowercase, dot-separated for JSON; kebab-case for CSS vars
- Semantic names over visual names (`color.primary` not `color.blue`)
- Scale tokens use numeric or T-shirt sizing (`sm`, `md`, `lg`)
- State suffixes: `default`, `hover`, `active`, `disabled`, `focus`

---

## Style Dictionary Setup

**`packages/tokens/style-dictionary.config.js`:**

```js
const StyleDictionary = require('style-dictionary');

module.exports = {
  source: ['src/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      prefix: 'ds',
      buildPath: 'dist/',
      files: [{
        destination: 'tokens.css',
        format: 'css/variables',
        options: { outputReferences: true }
      }]
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/',
      files: [{
        destination: 'tokens.js',
        format: 'javascript/es6'
      }]
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'dist/',
      files: [{
        destination: 'tokens.d.ts',
        format: 'typescript/es6-declarations'
      }]
    }
  }
};
```

Build: `npx style-dictionary build --config style-dictionary.config.js`

---

## CSS Custom Properties Output

Generated `dist/tokens.css`:

```css
:root {
  /* Primitives */
  --ds-color-blue-500: #3b82f6;
  --ds-color-gray-900: #111827;

  /* Semantics */
  --ds-color-primary-default: var(--ds-color-blue-600);
  --ds-color-neutral-text-primary: var(--ds-color-gray-900);

  /* Spacing */
  --ds-spacing-4: 1rem;
  --ds-spacing-8: 2rem;

  /* Typography */
  --ds-font-size-md: 1rem;
  --ds-font-weight-semibold: 600;
}
```

---

## JS/TS Constants Output

```ts
// dist/tokens.js
export const ColorBlue500 = "#3b82f6";
export const ColorPrimaryDefault = "#2563eb";
export const Spacing4 = "1rem";
export const FontSizeMd = "1rem";
```

---

## Multi-Brand Tokens

For multi-brand scenarios, create brand-specific semantic overrides:

```
packages/tokens/src/
├── primitives/         # Shared raw values
│   ├── color.json
│   └── spacing.json
└── brands/
    ├── brand-a/        # Brand A semantic mapping
    │   └── semantic.json
    └── brand-b/        # Brand B semantic mapping
        └── semantic.json
```

Build separate CSS files per brand, then load the correct one at runtime:

```js
// Load brand at app entry point
import(`@myds/tokens/dist/${brand}/tokens.css`);
```
