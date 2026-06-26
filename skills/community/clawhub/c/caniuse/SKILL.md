---
name: caniuse
description: Query browser compatibility for CSS/JS features using caniuse-cli. Use when user asks about browser support, compatibility, "can I use X", "does X work in IE/Safari/Chrome", or when writing code that might have compatibility concerns. Also trigger when user mentions specific features like flexbox, grid, container queries, or any web API and wants to know browser support status.
---

# Browser Compatibility Query

Query browser compatibility data for web features using the `caniuse` CLI tool.

## Prerequisites Check

Before querying, verify caniuse-cli is installed:

```bash
which caniuse || echo "NOT_INSTALLED"
```

If not installed, tell the user:
> caniuse-cli is not installed. Install it with:
> ```bash
> npm install -g @bramus/caniuse-cli
> ```

## Querying Compatibility

Run the caniuse command with the feature name:

```bash
caniuse <feature-name>
```

**Feature name formats:**
- Hyphenated: `caniuse viewport-units`
- Quoted phrases: `caniuse "viewport units"`
- With special chars: `caniuse @property`

**Common feature name mappings** (user term → caniuse query):
- `:has()` selector → `css-has`
- `:where()` selector → `css-where`
- `:is()` selector → `css-matches-pseudo`
- container queries → `css-container-queries` (size) or `css-container-queries-style` (style)
- CSS nesting → `css-nesting`
- subgrid → `subgrid`
- aspect-ratio → `css-aspect-ratio`
- gap in flexbox → `flexbox-gap`
- CSS grid → `css-grid`
- flexbox → `flexbox`

**JS/API features:**
- ES modules → `es6-module`
- async/await → `async-functions`
- optional chaining → `mdn-javascript_operators_optional_chaining`
- fetch API → `fetch`
- service workers → `serviceworkers`
- WebGPU → `webgpu`

## Presenting Results

After running the command:

1. **Show the compatibility table** as returned by caniuse

2. **Highlight key findings:**
   - Which major browsers fully support it
   - Any browsers with partial support (note the limitations)
   - Browsers that don't support it at all

3. **Call out important notes** if the output includes numbered notes (these often contain critical info about prefixes, flags, or partial implementations)

4. **Give practical advice** based on the results:
   - If widely supported: "Safe to use in production"
   - If partial support: "Works but check the notes for limitations"
   - If poor support: "Consider a polyfill or fallback"

## Handling Unknown Features

If caniuse returns "Nothing was found":

1. **Check the mapping table above** — many features have specific caniuse names (e.g., `:has()` → `css-has`)

2. **Try common prefixes:**
   - CSS properties: try `css-` prefix (e.g., `css-grid`, `css-variables`)
   - MDN data: try `mdn-` prefix for JS features

3. **Try variations:**
   - Remove special characters: `:has()` → `has` or `css-has`
   - Use hyphens: "container queries" → `container-queries`

4. **If still not found**, tell the user:
   > This feature might not be in the caniuse database, or uses a different name.
   > Check https://caniuse.com to find the correct feature name.
