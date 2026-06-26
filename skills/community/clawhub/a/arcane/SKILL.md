---
name: arcane
description: Expert guidance for building and maintaining projects with the Arcane Microframework. Use when creating new projects, defining routes, managing context-aware helpers, automatic assets, or handling localization.
---

# Arcane Microframework

Arcane is a tiny (12kb) single-file PHP microframework where **location is logic**. It uses filesystem-based routing and context-aware autoloading.

## Core Functions

- `env(key, default)`: Environment variables.
- `path(locator, actual)`: Unified tool for generating URLs or absolute server paths.
- `relay(name, mixed)`: Yield data (or HTML via callable) from page to layout.
- `scribe(string|array, replace)`: Translation/localization.

## Project Structure

```text
/
├── index.php        (The framework)
├── .env             (Configuration)
├── helpers/         (Context-aware logic)
├── layouts/         (Wrappers)
├── locales/         (Translations)
├── pages/           (Filesystem routes)
├── scripts/         (Auto-injected JS)
├── styles/          (Auto-injected CSS)
└── images/          (Assets)
```

## Workflows

### 1. Routing & Dynamic Segments
Files in `pages/` map to URLs. For dynamic segments (e.g., `/blog/my-post/`), use `define('ROUTES', [...])` in the closest physical file (e.g., `pages/blog.php`).

### 2. Layouts & Data
Use `define('LAYOUT', 'name')` in a page to wrap it in `layouts/name.php`. Use `relay()` to pass data like page titles.

### 3. Context-Aware Helpers
Helpers in `helpers/` are automatically available as variables in pages. They cascade based on the directory structure, allowing section-specific overrides.

### 4. Automatic Assets
CSS/JS files in `styles/` and `scripts/` are auto-injected if they match the layout or page path. No manual `<link>` or `<script>` tags needed.

---

For detailed API references and advanced patterns, refer to [DOCUMENTATION.md](references/DOCUMENTATION.md).
