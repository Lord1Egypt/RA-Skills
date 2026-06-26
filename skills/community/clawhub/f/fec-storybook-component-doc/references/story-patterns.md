# Storybook 配置与示例

## 初始化

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

# Input 输入框

用于用户文本输入，支持校验提示、前后缀图标、字数统计等。

### 何时使用

- 单行文本输入
- 需要实时校验反馈的表单字段

<Canvas of={InputStories.Default} />

### 属性

<Controls />

### 源码

<Source of={InputStories.Default} />
```

## Interaction Test

```tsx
import { expect, userEvent, within } from "@storybook/test";

export const FormSubmission: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText("用户名"), "admin");
    await userEvent.click(canvas.getByRole("button", { name: /登录/ }));
    await expect(canvas.findByText("登录成功")).resolves.toBeInTheDocument();
  },
};
```

## Visual Regression

```bash
npx chromatic --project-token=<token>
npx test-storybook
```
