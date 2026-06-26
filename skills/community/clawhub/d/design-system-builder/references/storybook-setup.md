# Storybook Setup Reference

## Table of Contents
1. [Installation & Bootstrap](#installation--bootstrap)
2. [Configuration Files](#configuration-files)
3. [Essential Addons](#essential-addons)
4. [Writing Stories](#writing-stories)
5. [Autodocs](#autodocs)
6. [MDX Documentation Pages](#mdx-documentation-pages)
7. [Theme Switcher Integration](#theme-switcher-integration)
8. [Deployment](#deployment)

---

## Installation & Bootstrap

```bash
cd apps/docs

# Bootstrap Storybook (choose React + Vite)
pnpm dlx storybook@latest init

# Add essential addons
pnpm add -D \
  @storybook/addon-essentials \
  @storybook/addon-a11y \
  @storybook/addon-themes \
  storybook-addon-pseudo-states
```

**Recommended Storybook version:** 8.x

---

## Configuration Files

### `.storybook/main.ts`

```ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: [
    '../../packages/components/src/**/*.stories.@(js|jsx|ts|tsx|mdx)',
    '../../packages/*/src/**/*.stories.@(js|jsx|ts|tsx|mdx)',
    './src/**/*.mdx',
  ],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-themes',
    'storybook-addon-pseudo-states',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',   // generate docs for stories with tags: ['autodocs']
  },
  typescript: {
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) =>
        prop.parent ? !/node_modules/.test(prop.parent.fileName) : true,
    },
  },
};

export default config;
```

### `.storybook/preview.ts`

```ts
import type { Preview } from '@storybook/react';
import '@myds/tokens/dist/tokens.css';   // load design tokens
import './preview.css';                   // global storybook styles

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    layout: 'centered',
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: 'var(--ds-color-neutral-bg-base)' },
        { name: 'dark', value: '#0f172a' },
        { name: 'white', value: '#ffffff' },
      ],
    },
    a11y: {
      config: {
        rules: [{ id: 'color-contrast', enabled: true }],
      },
    },
  },
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        title: 'Theme',
        icon: 'circlehollow',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (Story, context) => {
      const theme = context.globals.theme || 'light';
      return (
        <div data-theme={theme} style={{ padding: '1rem' }}>
          <Story />
        </div>
      );
    },
  ],
};

export default preview;
```

---

## Essential Addons

| Addon | Purpose |
|---|---|
| `addon-essentials` | Controls, Actions, Docs, Viewport, Backgrounds, Toolbars |
| `addon-a11y` | axe-core accessibility audit panel |
| `addon-themes` | Theme switching toolbar |
| `storybook-addon-pseudo-states` | Force CSS pseudo-states (`:hover`, `:focus`, `:active`) |

### Addon Details

**Controls** — automatically generates UI controls from prop types. Works best with TypeScript + `react-docgen-typescript`.

**Actions** — logs event handler calls. Auto-configured for props matching `on[A-Z].*`.

**Viewport** — switch between device sizes. Add custom breakpoints:

```ts
// preview.ts
parameters: {
  viewport: {
    viewports: {
      mobile: { name: 'Mobile', styles: { width: '390px', height: '844px' } },
      tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
      desktop: { name: 'Desktop', styles: { width: '1440px', height: '900px' } },
    },
  },
}
```

---

## Writing Stories

### CSF3 Format (recommended)

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect } from '@storybook/test';
import { Button } from '@myds/components';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
};
export default meta;

type Story = StoryObj<typeof Button>;

// ✅ Basic story
export const Primary: Story = {
  args: {
    children: 'Click me',
    variant: 'primary',
  },
};

// ✅ Story with play function (interaction test)
export const ClickTest: Story = {
  args: { children: 'Submit', onClick: fn() },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button'));
    await expect(args.onClick).toHaveBeenCalledOnce();
  },
};

// ✅ Render function story (multiple variants)
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      {(['primary', 'secondary', 'ghost', 'danger'] as const).map((v) => (
        <Button key={v} variant={v}>{v}</Button>
      ))}
    </div>
  ),
};
```

### Story Organization

Use the `title` field to build a navigation tree:

```
Components/
  Button
  Input
  Select
Feedback/
  Alert
  Toast
  Badge
Navigation/
  Tabs
  Breadcrumb
  Pagination
Layout/
  Card
  Divider
  Stack
```

---

## Autodocs

Enable per-component with `tags: ['autodocs']` in the meta.

What autodocs generates:
- Props table from TypeScript types + JSDoc comments
- Live interactive example using `args`
- All named exports as story previews

**Enhance props documentation with JSDoc:**

```tsx
export interface ButtonProps {
  /**
   * Visual style variant of the button.
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';

  /**
   * When true, shows a loading spinner and prevents interaction.
   * @default false
   */
  isLoading?: boolean;
}
```

---

## MDX Documentation Pages

Use MDX for design guidelines, overview pages, and token documentation.

**`apps/docs/src/introduction.mdx`:**

```mdx
import { Meta } from '@storybook/blocks';

<Meta title="Introduction" />

# My Design System

Built with React + TypeScript.

## Getting Started

\`\`\`bash
npm install @myds/components @myds/tokens
\`\`\`

Import the tokens CSS in your app entry:

\`\`\`ts
import '@myds/tokens/dist/tokens.css';
\`\`\`
```

**`apps/docs/src/tokens/colors.mdx`:**

```mdx
import { Meta, ColorPalette, ColorItem } from '@storybook/blocks';

<Meta title="Tokens/Colors" />

# Color Tokens

<ColorPalette>
  <ColorItem
    title="Primary"
    subtitle="Used for primary actions"
    colors={{
      Default: 'var(--ds-color-primary-default)',
      Hover: 'var(--ds-color-primary-hover)',
    }}
  />
</ColorPalette>
```

---

## Theme Switcher Integration

With `@storybook/addon-themes`, wrap your theme provider:

```ts
// preview.ts
import { withThemeByDataAttribute } from '@storybook/addon-themes';

export const decorators = [
  withThemeByDataAttribute({
    themes: { light: 'light', dark: 'dark' },
    defaultTheme: 'light',
    attributeName: 'data-theme',
  }),
];
```

---

## Deployment

### Static Build

```bash
pnpm build-storybook
# Output: storybook-static/
```

### Chromatic (Recommended)

Chromatic provides visual regression + hosted Storybook:

```bash
pnpm add -D chromatic

# Publish
npx chromatic --project-token=<token>
```

**GitHub Actions integration:**

```yaml
# .github/workflows/chromatic.yml
name: Chromatic

on: [push]

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm build
      - uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          workingDir: apps/docs
```

### Vercel / Netlify

Point the build command to `pnpm build-storybook` and publish dir to `storybook-static`.
