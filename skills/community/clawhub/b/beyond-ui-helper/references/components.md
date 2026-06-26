# Beyond-UI Component Catalogue

This quick reference highlights the most-used exports from `@beyondcorp/beyond-ui`. All components share these characteristics:

- Built with class-variance-authority (CVA) for variants/sizes.
- Accept `className` for Tailwind overrides.
- Are fully typed with TypeScript definitions emitted in the package.
- Have Storybook stories in the upstream repo under `stories/*.stories.tsx` for live examples.

## Core layout primitives

- **Navbar** – Flexible top navigation with slot-based children. Example: [`landing/page-layout-landing.tsx`](../assets/examples/components/layout/page-layout-landing.tsx) baseline header.
- **Sidebar** – Collapsible navigation tree with badges and nested items. Example: [`layout/sidebar-navigation.tsx`](../assets/examples/components/layout/sidebar-navigation.tsx).
- **DashboardLayout** – Composes `Sidebar`, `DashboardHeader`, and main content, exposing props for menu items, header actions, and responsive behaviour. Example: [`layout/dashboard-page.tsx`](../assets/examples/components/layout/dashboard-page.tsx).
- **DashboardGrid** – Responsive layout helper for metric cards and charts. See the dashboard page example above for grid usage in context.
- **PageLayout** – Generic multi-section layout with hero/content/footer options. Example hero shell: [`layout/page-layout-landing.tsx`](../assets/examples/components/layout/page-layout-landing.tsx).

## Forms & inputs

- **Button** – Variants `primary`, `secondary`, `danger`, `ghost`, etc.; sizes `sm`–`xl`. Snippets: [`forms/button-showcase.tsx`](../assets/examples/components/forms/button-showcase.tsx).
- **Input / Textarea** – Form controls with validation states. Full profile form composition: [`forms/input-with-validation.tsx`](../assets/examples/components/forms/input-with-validation.tsx).
- **Select** – Styled dropdown. Filter panel example: [`forms/select-filter-panel.tsx`](../assets/examples/components/forms/select-filter-panel.tsx).
- **Checkbox / Radio / Switch** – Accessible toggles. Notification preferences card: [`forms/radio-preferences-card.tsx`](../assets/examples/components/forms/radio-preferences-card.tsx).
- **NightModeSwitch** – Theme toggle with optional toolbar composition: [`utilities/night-mode-toolbar.tsx`](../assets/examples/components/utilities/night-mode-toolbar.tsx).
- **Auth form panel** – Login view composed from primitives: [`forms/auth-login-panel.tsx`](../assets/examples/components/forms/auth-login-panel.tsx).

## Data display & dashboards

- **Card** family – Structure metric or content blocks. Metric grid example: [`data-display/card-metrics-grid.tsx`](../assets/examples/components/data-display/card-metrics-grid.tsx).
- **StatsCard** – Dashboard KPI tile. Leaderboard snippet: [`data-display/statscard-leaderboard.tsx`](../assets/examples/components/data-display/statscard-leaderboard.tsx).
- **DataTable** – Sortable, filterable table. Users table composition: [`data-display/datatable-users.tsx`](../assets/examples/components/data-display/datatable-users.tsx).
- **Tabs** – Sectioned content for analytics views (see dashboard layout example).
- **ComponentShowcase** – Prebuilt playground with clipboard and responsive preview. Dashboard integration: [`data-display/component-showcase-dashboard.tsx`](../assets/examples/components/data-display/component-showcase-dashboard.tsx).
- **Image** – Utility wrapper for responsive imagery. Captioned hero card: [`data-display/image-with-caption.tsx`](../assets/examples/components/data-display/image-with-caption.tsx).

## Feedback & overlays

- **Alert** – Inline callouts with action buttons: [`feedback/alert-inline-callout.tsx`](../assets/examples/components/feedback/alert-inline-callout.tsx).
- **Toast** – Imperative notifications via `showToast`. Multi-type stack: [`feedback/toast-notifications.tsx`](../assets/examples/components/feedback/toast-notifications.tsx).
- **Modal** – Confirmation dialog scaffolding: [`feedback/modal-confirmation.tsx`](../assets/examples/components/feedback/modal-confirmation.tsx).
- **Skeleton / Spinner** – Loading placeholders and overlays: [`feedback/skeleton-loading.tsx`](../assets/examples/components/feedback/skeleton-loading.tsx), [`feedback/spinner-overlay.tsx`](../assets/examples/components/feedback/spinner-overlay.tsx).

## Auth & account surfaces

- **Auth** – Login, signup, reset flows. Full security dashboard: [`auth/auth-dashboard.tsx`](../assets/examples/components/auth/auth-dashboard.tsx).
- **ProfileManagement** – Summary card composition: [`auth/profile-summary.tsx`](../assets/examples/components/auth/profile-summary.tsx).

## Marketing & storytelling

- **LandingPage** – Hero, features, CTA patterns: [`marketing/landing-hero.tsx`](../assets/examples/components/marketing/landing-hero.tsx).
- **Blog / SingleBlogView** – Feature article layout: [`marketing/blog-feature.tsx`](../assets/examples/components/marketing/blog-feature.tsx).
- **Marketplace / SingleProductView** – Product showcase components (see repo `stories/` for product grids and docs).

## Utilities & documentation aids

- **CodeHighlight** – Syntax highlighting blocks: [`utilities/code-highlight-snippet.tsx`](../assets/examples/components/utilities/code-highlight-snippet.tsx).
- **DashboardHeader / Toast / Badge** – See layout/dashboard examples for combination patterns.

## Usage notes

- All exports live in the package root (`import { Button } from '@beyondcorp/beyond-ui'`). Keep `@beyondcorp/beyond-ui/dist/styles.css` imported once at the app entry.
- Snippets assume Tailwind token overrides live in your project; adjust utilities as needed.
- For composite dashboards or landing pages, mix layout primitives with component snippets above.
- Charts: pair metric cards with your preferred charting lib (e.g., `ChartWrapper` under `src/components`).

See [references/hooks.md](hooks.md) for complementary hooks/utilities and [references/workflow.md](workflow.md) for lint/storybook/test scripts while iterating. Reload snippets from `assets/examples/` when scaffolding new screens.
