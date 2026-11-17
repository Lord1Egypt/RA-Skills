# Storybook configuration and examples

## Initialization

```bash
npx storybook@latest init
```

## main.ts

```ts
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
  ],
  framework: { name: "@storybook/react-vite", options: {} },
  docs: { autodocs: "tag" },
};

export default config;
```

## Story

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary", "ghost"] },
    onClick: { action: "clicked" },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { variant: "primary", children: "Primary Button" },
};
```

## Decorators

```tsx
import type { Preview } from "@storybook/react";
import { MemoryRouter } from "react-router-dom";
import { ThemeProvider } from "../src/app/providers";

const preview: Preview = {
  decorators: [
    (Story) => <ThemeProvider>{Story()}</ThemeProvider>,
    (Story) => <MemoryRouter initialEntries={["/"]}>{Story()}</MemoryRouter>,
  ],
};

export default preview;
```

## MDX

```mdx
import { Meta, Canvas, Controls, Source } from "@storybook/blocks";
import * as InputStories from "./Input.stories";

<Meta of={InputStories} />

#Input input box

Used for user text input, supporting verification prompts, suffix and suffix icons, word count, etc.

### When to use

- Single line text input
- Form fields that require real-time verification feedback

<Canvas of={InputStories.Default} />

### Properties

<Controls />

### Source code

<Source of={InputStories.Default} />
```

## Interaction Test

```tsx
import { expect, userEvent, within } from "@storybook/test";

export const FormSubmission: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
await userEvent.type(canvas.getByLabelText("username"), "admin");
    await userEvent.click(canvas.getByRole("button", { name: /login/ }));
    await expect(canvas.findByText("Login successful")).resolves.toBeInTheDocument();
  },
};
```

## Visual Regression

```bash
npx chromatic --project-token=<token>
npx test-storybook
```
