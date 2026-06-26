# Testing Strategy Reference

## Table of Contents
1. [Testing Pyramid](#testing-pyramid)
2. [Setup: Vitest + Testing Library](#setup-vitest--testing-library)
3. [Unit & Interaction Tests](#unit--interaction-tests)
4. [Storybook Interaction Tests](#storybook-interaction-tests)
5. [Visual Regression with Chromatic](#visual-regression-with-chromatic)
6. [Accessibility Testing](#accessibility-testing)
7. [Coverage Requirements](#coverage-requirements)
8. [CI Pipeline Integration](#ci-pipeline-integration)

---

## Testing Pyramid

```
         ┌─────────────────────────────┐
         │     Visual Regression       │  Chromatic / Percy
         │   (screenshot diffing)      │  ~Few per component
         ├─────────────────────────────┤
         │    Interaction Tests        │  @testing-library or
         │  (user events, flows)       │  Storybook play()
         ├─────────────────────────────┤
         │    Unit / Logic Tests       │  Vitest
         │  (props, states, utils)     │  ~Many per component
         └─────────────────────────────┘
```

**Minimum per component:**
- [ ] Renders without errors
- [ ] Default props match snapshot/expectation
- [ ] Key prop variations produce correct output
- [ ] Interactive states (click, focus, disable) work
- [ ] No critical a11y violations

---

## Setup: Vitest + Testing Library

```bash
# Install
pnpm add -D \
  vitest \
  @vitest/ui \
  jsdom \
  @testing-library/react \
  @testing-library/user-event \
  @testing-library/jest-dom \
  jest-axe \
  -w
```

**`packages/components/vitest.config.ts`:**

```ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: { lines: 80, functions: 80, branches: 70 },
    },
  },
});
```

**`src/test-setup.ts`:**

```ts
import '@testing-library/jest-dom';
import { expect } from 'vitest';
import { toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);
```

---

## Unit & Interaction Tests

### Button Test Example

```tsx
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import { vi, describe, it, expect } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  // Smoke test
  it('renders without crashing', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  // Content
  it('renders children as button label', () => {
    render(<Button>Submit</Button>);
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  // Variants
  it.each(['primary', 'secondary', 'ghost', 'danger'] as const)(
    'renders %s variant without errors',
    (variant) => {
      render(<Button variant={variant}>Button</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('data-variant', variant);
    }
  );

  // Disabled state
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Button</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  // Loading state
  it('is disabled and aria-busy when isLoading', () => {
    render(<Button isLoading>Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-busy', 'true');
  });

  // Click interaction
  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Button</Button>);
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  // Does not fire click when disabled
  it('does not call onClick when disabled', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<Button disabled onClick={handleClick}>Button</Button>);
    await user.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  // Ref forwarding
  it('forwards ref to button element', () => {
    const ref = { current: null };
    render(<Button ref={ref}>Button</Button>);
    expect(ref.current).toBeInstanceOf(HTMLButtonElement);
  });

  // Accessibility
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Accessible button</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Input Test Example

```tsx
describe('Input', () => {
  it('updates value on user input', async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<Input label="Name" onChange={handleChange} />);
    await user.type(screen.getByLabelText('Name'), 'John');
    expect(handleChange).toHaveBeenCalled();
    expect(screen.getByLabelText('Name')).toHaveValue('John');
  });

  it('shows error message when isInvalid', () => {
    render(<Input label="Email" isInvalid errorMessage="Invalid email" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('aria-invalid', 'true');
    expect(screen.getByText('Invalid email')).toBeInTheDocument();
  });

  it('is associated with label via htmlFor', () => {
    render(<Input label="Username" />);
    const label = screen.getByText('Username');
    const input = screen.getByLabelText('Username');
    expect(label).toBeInTheDocument();
    expect(input).toBeInTheDocument();
  });
});
```

---

## Storybook Interaction Tests

Use Storybook's `play` function for higher-level interaction scenarios. These run in browser context and can be executed in CI via Storybook Test Runner.

```tsx
// Select.stories.tsx
import { within, userEvent, expect, fn } from '@storybook/test';

export const SelectAnOption: Story = {
  args: {
    options: [
      { label: 'Option A', value: 'a' },
      { label: 'Option B', value: 'b' },
    ],
    onChange: fn(),
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // Open dropdown
    await userEvent.click(canvas.getByRole('combobox'));

    // Select an option
    await userEvent.click(canvas.getByRole('option', { name: 'Option B' }));

    // Verify onChange called with correct value
    await expect(args.onChange).toHaveBeenCalledWith('b');

    // Verify display updated
    await expect(canvas.getByRole('combobox')).toHaveTextContent('Option B');
  },
};
```

**Run Storybook interaction tests in CI:**

```bash
pnpm add -D @storybook/test-runner

# package.json
"test:storybook": "test-storybook --url http://localhost:6006"
```

---

## Visual Regression with Chromatic

Chromatic captures screenshots of every story and detects pixel-level regressions.

### Setup

```bash
pnpm add -D chromatic
```

```bash
# First run — establishes baselines
npx chromatic --project-token=<TOKEN> --auto-accept-changes

# Subsequent runs — diffs against baseline
npx chromatic --project-token=<TOKEN>
```

### What Chromatic Tests

- Every story = one screenshot per viewport
- Diffs shown in Chromatic UI
- Reviewers approve or reject changes
- PRs blocked until visual changes are approved

### Chromatic Configuration

```js
// chromatic.config.js
module.exports = {
  // Skip stories with these tags from visual testing
  // (useful for very complex animated stories)
  disableSnapshot: false,

  // Delay before screenshot (for animations to settle)
  delay: 200,

  // Viewports to capture
  viewports: [375, 768, 1440],
};
```

### Story-level overrides

```tsx
export const AnimatedCard: Story = {
  parameters: {
    chromatic: { delay: 500, viewports: [768, 1440] },
  },
};

// Skip visual regression for this story
export const LoadingSpinner: Story = {
  parameters: {
    chromatic: { disableSnapshot: true },
  },
};
```

---

## Accessibility Testing

### Automated (jest-axe)

```tsx
it('has no a11y violations', async () => {
  const { container } = render(
    <Select
      label="Country"
      options={[{ label: 'US', value: 'us' }]}
      value="us"
      onChange={() => {}}
    />
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Storybook a11y Addon

- Automatically runs axe-core on every story in dev
- Shows violations in the Accessibility panel
- Fails CI when configured:

```ts
// .storybook/test-runner.ts
import { checkA11y } from 'axe-playwright';

module.exports = {
  async postVisit(page) {
    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  },
};
```

### Manual Checklist

- [ ] All interactive elements reachable by keyboard (Tab, Shift+Tab)
- [ ] Enter/Space activate buttons; Enter follows links
- [ ] Modals trap focus
- [ ] `aria-live` regions announce dynamic content
- [ ] Test with screen reader: VoiceOver (macOS), NVDA (Windows)
- [ ] Zoom to 200% — layout must not break

---

## Coverage Requirements

| Metric | Threshold |
|---|---|
| Line coverage | ≥ 80% |
| Function coverage | ≥ 80% |
| Branch coverage | ≥ 70% |
| New components | 100% smoke tests |

Configure in `vitest.config.ts`:
```ts
coverage: {
  thresholds: { lines: 80, functions: 80, branches: 70 }
}
```

---

## CI Pipeline Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm build
      - run: pnpm test --coverage
      - run: pnpm test:storybook
        env:
          STORYBOOK_URL: http://localhost:6006
```
