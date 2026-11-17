---
name: ghost-theme-builder
description: Build, customize, review, debug, migrate, and optimize Ghost CMS Handlebars themes. Use for Ghost theme templates and partials, package.json custom settings, routes.yaml, memberships, Portal, comments, search, GScan, or converting a design into a Ghost theme.
license: MIT
metadata:
  author:
    name: frontendweb
    email:  contact@frontendweb.agency
  version: "1.0.1"
---

# Ghost Theme Builder

Inspect the target theme before changing it. Make the smallest coherent change that satisfies the request and preserves the theme's existing conventions.

## Resource routing

Search `examples/` and `snippets/` for the requested feature before writing code. Reuse a suitable pattern; otherwise create the smallest reusable partial, style, or utility needed.

Read only the references relevant to the task:

- Theme structure or validation: `docs/structure.md` and `docs/gscan.md`
- Template selection or data scope: `reference/contexts.md`, then the matching file in `docs/contexts/`
- Handlebars helpers: `reference/helpers.md`, then the exact helper file in `docs/helpers/`
- Responsive images and assets: `docs/responsive-images.md`
- Custom theme settings: `docs/custom-settings.md`
- Memberships, Portal, comments, or paid content: `docs/members.md`
- Search or sharing: `docs/search.md` or `docs/share.md`
- Custom URLs, collections, channels, or redirects: `docs/routing.md`
- Rich editor cards and content styling: `docs/content.md`

Read `docs/.source.json` before relying on a version-sensitive local reference. Treat the local snapshot as the default source and verify a version-sensitive point against official Ghost documentation when browsing is available.

Use `prompts/build.md` for builds, fixes, migrations, and design conversions. Use `prompts/review.md` for reviews. For a narrow question, answer it directly without proposing an unrequested implementation.

## Implementation rules

- Map URLs to Ghost contexts and templates. Keep the base document in `default.hbs`; use partials for shared headers, cards, loops, pagination, and footers.
- Start new themes from the minimum valid structure or `examples/starter-kit.md`. Add context-specific templates only when their layout differs.
- Preserve and use `{{ghost_head}}`, `{{ghost_foot}}`, `{{body_class}}`, `{{post_class}}`, and `{{asset}}` where applicable.
- Use `{{img_url}}`, useful alternative text, and responsive image dimensions when available. Do not hard-code site URLs, navigation, member state, or post counts when Ghost provides data.
- Use `{{#is}}`, `{{#match}}`, and template contexts for server-rendered variations; do not recreate them in client-side JavaScript.
- Add memberships, Portal, comments, and search only after checking the relevant site settings and graceful fallbacks. Treat member UI as authorization-aware presentation, never access control.
- Implement semantic landmarks, a logical heading hierarchy, visible keyboard focus, sufficient contrast, descriptive links, reduced motion, and layouts that work at 320px and with zoom.
- Make metadata context-aware with Ghost `meta_*` helpers. Avoid SEO tags that conflict with Ghost output.
- Change `routes.yaml` only when a requested URL or collection/channel behavior cannot be expressed through templates.

## Review and handoff

For reviews, use `prompts/review.md`. Prioritize rendering or Theme API faults, accessibility, membership confusion, SEO regressions, and costly assets before style preferences. Report severity, exact file and line, user impact, and a concrete correction; separate confirmed faults from suggestions.

For builds and fixes, use `prompts/build.md`. Report changed filenames, relevant Ghost helpers or admin settings, validation actually run, and outstanding admin configuration. Run GScan and any available theme build or lint command separately. Do not claim either passed unless it completed successfully.
