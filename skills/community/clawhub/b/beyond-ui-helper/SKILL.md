---
name: beyond-ui-helper
description: Install, configure, and troubleshoot the @beyondcorp/beyond-ui React/Tailwind component library. Use when an agent needs to add the package, wire the generated CSS, align Tailwind themes, run Storybook/tests/build, or reference Beyond-UI components, hooks, and known caveats.
---

# Beyond-UI Helper

## Quick Start Workflow

1. **Plan the environment**
   - Confirm Node ≥ 18 and npm ≥ 9 (or matching pnpm/yarn versions).
   - Decide if the host app already uses Tailwind. If not, the packaged CSS still works—Tailwind becomes optional for theme overrides.
   - When upgrading, check open Trello cards (#8–#12, #16, #17, etc.) and `docs/security-dx-notes.md` for pending fixes before bumping versions.

2. **Install the package**
   - Run the install script bundled with this skill: `scripts/install-beyond-ui.sh`. It installs `@beyondcorp/beyond-ui` plus missing peer deps.
   - For manual install, see [references/setup.md](references/setup.md) for npm/pnpm/yarn equivalents and monorepo guidance.

3. **Wire the generated stylesheet**
   - Use `scripts/add-css-import.js` to inject `import '@beyondcorp/beyond-ui/dist/styles.css';` into the app entry (main.tsx / index.jsx / etc.).
   - Confirm the import sits above app-specific CSS to keep token overrides predictable.

4. **Verify setup**
   - Execute `scripts/verify-setup.sh` to run lint, test, and build—mirrors CONTRIBUTING requirements.
   - If Storybook is needed, run `npm run storybook` (documented in [references/workflow.md](references/workflow.md)).

5. **Add components via templates**
   - Browse `assets/examples/components/**.tsx` for ready-to-drop snippets grouped by category (forms, data-display, layout, auth, marketing, utilities).
   - Load [references/components.md](references/components.md) to locate snippets per component and guidance on combining them into full screens.
   - Use [references/hooks.md](references/hooks.md) for utilities like `useDarkMode`, `useBreakpoint`, `useIntersectionObserver`.

6. **Align theming**
   - Import defaults from `@beyondcorp/beyond-ui/dist/styles.css` immediately for a working palette.
   - To brand your app, follow [references/theming.md](references/theming.md): extend Tailwind tokens (`primary`, `secondary`, `accent`, etc.) and restart the build.
   - Snippets assume semantic tokens; adjust Tailwind overrides according to your brand.

7. **Troubleshoot**
   - Consult [references/known-issues.md](references/known-issues.md) to triage npm audit advisories, Storybook upgrade gaps, browserslist refresh tasks, clipboard API fallbacks, and other DX notes.
   - For version bumps, track Storybook 10 migration, vite-plugin-dts upgrades, and tsup/rollup advisories before publishing.

## Packaging & Release Guidelines

- Keep this skill co-located with the Beyond-UI repo for shared PR review.
- Use `scripts/package_skill.py skills/public/beyond-ui-helper` (from repo root) to validate and create a `.skill` artifact.
- Publish via `clawhub sync --root skills/public/beyond-ui-helper --changelog "<notes>" --tags "latest,beyond-ui"` once tests pass. Include install instructions, change summary, and reference the Trello ticket in PRs per CONTRIBUTING.
- Consider wiring CI to run `npm run lint`, `npm test`, `npm run build`, and `npm run build-storybook` before packaging to mirror library standards.

## Resource Map

| Need | Resource |
|------|----------|
| Install commands, CSS import steps, monorepo notes | [references/setup.md](references/setup.md) |
| Theme token overrides, Sidebar/Dashboard layout tips | [references/theming.md](references/theming.md) |
| Component catalogue + snippet index | [references/components.md](references/components.md) |
| Hooks & utilities quick reference | [references/hooks.md](references/hooks.md) |
| Contributor workflow (scripts, Storybook, tests) | [references/workflow.md](references/workflow.md) |
| Security/DX caveats and Trello task context | [references/known-issues.md](references/known-issues.md) |
| Ready-to-use code snippets | `assets/examples/components/*/*.tsx` |

Scripts live under `scripts/`—open them to review parameters before running.

## Reference Usage

When using this skill:
- Load `references/setup.md` first if the host project has never seen Beyond-UI.
- Load `references/theming.md` when customizing palettes or Dashboard layout styling.
- Load `references/components.md` to pick snippet(s) for forms, dashboards, marketing, auth, utilities, etc.
- Pull actual code from `assets/examples/components/**` and adapt tokens/props as needed.
- Load `references/hooks.md` when wiring stateful utilities; check `references/known-issues.md` before publishing or when audit warnings appear.

Keep response outputs concise—link to references/snippets rather than duplicating full docs. Update references and templates as Beyond-UI evolves so downstream agents stay aligned.
