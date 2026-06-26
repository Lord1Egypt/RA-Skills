# Beyond-UI Setup Reference

## Install the package

Beyond-UI ships as `@beyondcorp/beyond-ui` with `react`, `react-dom`, and `tailwindcss` declared as peer dependencies. Install it using the package manager already in the project:

```bash
# npm
npm install @beyondcorp/beyond-ui

# pnpm
pnpm add @beyondcorp/beyond-ui

# yarn
yarn add @beyondcorp/beyond-ui
```

For monorepos, install the dependency in the application package that renders the UI. The distributed bundle includes ESM/CJS builds plus declaration files.

### Optional peer dependencies

Tailwind is only required if you want to override semantic tokens or author custom utilities. The compiled CSS works even without Tailwind in the host build. When Tailwind is present, ensure the content paths include Beyond-UI (`./node_modules/@beyondcorp/beyond-ui/dist/**/*`).

## Import the generated CSS

Import the packaged stylesheet once in the application entry point so components render with the default theme:

```tsx
// src/main.tsx or src/index.tsx
import '@beyondcorp/beyond-ui/dist/styles.css';
```

The Stylesheet contains all component tokens and utilities. Keep this import above app-specific CSS to allow overrides via Tailwind.

## Integrate components

With the dependency installed and CSS imported, components can be used immediately:

```tsx
import { Card, CardHeader, CardTitle, CardContent, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function WelcomeCard() {
  return (
    <Card className="max-w-md">
      <CardHeader>
        <CardTitle>Welcome to Beyond-UI</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-muted-foreground">
          Build production dashboards faster with ready-made components, hooks, and layouts.
        </p>
        <Button variant="primary">View components</Button>
      </CardContent>
    </Card>
  );
}
```

For dashboard layouts or Storybook examples, run `npm run dev` or `npm run storybook` as outlined in [workflow.md](workflow.md).
