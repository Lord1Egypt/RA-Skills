# Contributor Workflow Reference

Align skill users with the Beyond-UI repo’s conventions and automation expectations.

## Environment checks

- Node.js ≥ 18.0.0
- npm ≥ 9.0.0 (pnpm/yarn acceptable if project standard)
- Git CLI + GitHub access for PRs

## Local commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies (run after pulling main). |
| `npm run dev` | Launch Vite playground for landing/showcase demos. |
| `npm run storybook` | Start Storybook at http://localhost:6006. |
| `npm run build` | Build component library and CSS assets. |
| `npm run build-storybook` | Generate static Storybook output. |
| `npm test` | Run Jest + React Testing Library suites. |
| `npm run lint` | Lint source, stories, tests. |

Run lint, test, and build before packaging or publishing the skill to Clawhub.

## Git workflow (from CONTRIBUTING)

1. Stay off `main`: create a feature branch using `ft|rf|bg-#ticket-id-title` naming.
2. Make changes, commit with `ft|rf|bg-#ticket-id: message` format.
3. Fetch upstream main, rebase or merge to stay current.
4. Run `npm run build && npm test` (and lint) before pushing.
5. Push branch and open PR with Trello link in body (`Trello: https://trello.com/c/...`).
6. Request reviewer approval before merge; never self-merge to `main`.

## Storybook & docs

- Storybook stories live in `/stories`. Keep them updated as components change.
- Public Storybook: https://storybook.ui.beyondsoftwares.com
- Library landing page: https://ui.beyondsoftwares.com

## Packaging this skill

- From repo root: `scripts/package_skill.py skills/public/beyond-ui-helper`.
- Artifacts: `.skill` file stored in the specified output (default `dist/`).
- Publish via Clawhub CLI (`clawhub publish`) once validation passes and PR is merged.

## Active Trello tasks (2026-03-24)

- **#8 Landing Page Polish** – Navigation, CTAs, accessibility improvements.
- **#9 Component Showcase Fixes** – Tabs keyboard support, clipboard docs.
- **#10 Security & DX Notes** – Surface npm audit findings, env prerequisites.
- **#11 Fix Storybook/Test lint failures** – Address hook warnings, ensure green CI.
- **#12 Refresh browserslist/caniuse-lite** – Update build pipeline data.

Reference these when planning upgrades or doc updates so the skill reflects the latest priorities.
