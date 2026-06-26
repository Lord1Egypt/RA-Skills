# Component Patterns Reference

## Table of Contents
1. [File Structure](#file-structure)
2. [Naming Conventions](#naming-conventions)
3. [Props API Design](#props-api-design)
4. [TypeScript Patterns](#typescript-patterns)
5. [Compound Components](#compound-components)
6. [Polymorphic Components](#polymorphic-components)
7. [Accessibility Requirements](#accessibility-requirements)
8. [Documentation Template](#documentation-template)
9. [Vue 3 Patterns](#vue-3-patterns)

---

## File Structure

```
packages/components/src/
├── Button/
│   ├── Button.tsx
│   ├── Button.types.ts
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   └── index.ts
├── Input/
│   └── ...
└── index.ts            # Root barrel — exports everything
```

**`index.ts` (component barrel):**
```ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

---

## Naming Conventions

| What | Convention | Example |
|---|---|---|
| Component file | PascalCase | `Button.tsx` |
| Component name | PascalCase | `export const Button` |
| Props interface | `{Name}Props` | `ButtonProps` |
| Variants | string union | `'primary' \| 'secondary' \| 'ghost'` |
| Size prop | `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl'` |
| State props | semantic booleans | `isDisabled`, `isLoading`, `isSelected` |
| Event handlers | `on{Event}` | `onClick`, `onChange`, `onDismiss` |
| CSS classes | `ds-{component}-{element}` | `ds-button-icon` |
| Data attributes | `data-{state}` | `data-loading`, `data-variant` |

---

## Props API Design

### Core Principles

1. **Extend native HTML element props** — spread `React.HTMLAttributes` or element-specific types
2. **Use string unions over enums** — better ergonomics and tree-shaking
3. **Provide sensible defaults** — `size="md"`, `variant="primary"`
4. **`className` always accepted** — never block it
5. **`children` explicit** — include in interface, not just implicit
6. **Event naming** — follow React conventions (`onClick`, not `handleClick`)

### Button Example (React)

```tsx
// Button.types.ts
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Show loading spinner and disable interaction */
  isLoading?: boolean;
  /** Render as full-width block element */
  isFullWidth?: boolean;
  /** Icon to render before the label */
  leftIcon?: React.ReactElement;
  /** Icon to render after the label */
  rightIcon?: React.ReactElement;
  /** Accessible label when using icon-only */
  'aria-label'?: string;
}
```

```tsx
// Button.tsx
import * as React from 'react';
import type { ButtonProps } from './Button.types';
import { cn } from '../utils/cn';

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      isFullWidth = false,
      leftIcon,
      rightIcon,
      children,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || isLoading;

    return (
      <button
        ref={ref}
        disabled={isDisabled}
        data-variant={variant}
        data-size={size}
        data-loading={isLoading || undefined}
        aria-busy={isLoading}
        className={cn(
          'ds-button',
          `ds-button--${variant}`,
          `ds-button--${size}`,
          isFullWidth && 'ds-button--full-width',
          className
        )}
        {...props}
      >
        {isLoading && <span className="ds-button__spinner" aria-hidden="true" />}
        {leftIcon && <span className="ds-button__icon ds-button__icon--left">{leftIcon}</span>}
        {children && <span className="ds-button__label">{children}</span>}
        {rightIcon && <span className="ds-button__icon ds-button__icon--right">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### Form Input Example

```tsx
export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  helperText?: string;
  errorMessage?: string;
  isRequired?: boolean;
  isInvalid?: boolean;
  size?: 'sm' | 'md' | 'lg';
  leftAddon?: React.ReactNode;
  rightAddon?: React.ReactNode;
}
```

---

## TypeScript Patterns

### Discriminated Unions for Variants

```ts
// Icon button requires aria-label; text button requires children
type ButtonWithLabel = {
  children: React.ReactNode;
  'aria-label'?: string;
};

type IconOnlyButton = {
  children?: never;
  'aria-label': string;
};

export type ButtonProps = (ButtonWithLabel | IconOnlyButton) & BaseButtonProps;
```

### Generic Components

```ts
// Select component with typed value
interface SelectProps<T extends string | number> {
  value: T;
  onChange: (value: T) => void;
  options: Array<{ label: string; value: T }>;
}
```

### `cn` Utility (className merging)

```ts
// packages/utils/src/cn.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## Compound Components

Use compound components for complex UI with multiple related parts.

```tsx
// Dialog compound component
interface DialogContextValue {
  isOpen: boolean;
  onClose: () => void;
}

const DialogContext = React.createContext<DialogContextValue | null>(null);

function useDialogContext() {
  const ctx = React.useContext(DialogContext);
  if (!ctx) throw new Error('Dialog subcomponent used outside <Dialog>');
  return ctx;
}

// Root
export function Dialog({ children, isOpen, onClose }: DialogRootProps) {
  return (
    <DialogContext.Provider value={{ isOpen, onClose }}>
      {children}
    </DialogContext.Provider>
  );
}

// Subcomponents
Dialog.Trigger = function DialogTrigger({ children }: { children: React.ReactNode }) {
  const { onClose } = useDialogContext();
  return <button onClick={onClose}>{children}</button>;
};

Dialog.Content = function DialogContent({ children }: { children: React.ReactNode }) {
  const { isOpen } = useDialogContext();
  if (!isOpen) return null;
  return <div role="dialog" aria-modal>{children}</div>;
};

Dialog.Title = function DialogTitle({ children }: { children: React.ReactNode }) {
  return <h2>{children}</h2>;
};

// Usage:
// <Dialog isOpen={open} onClose={() => setOpen(false)}>
//   <Dialog.Trigger>Open</Dialog.Trigger>
//   <Dialog.Content>
//     <Dialog.Title>Hello</Dialog.Title>
//   </Dialog.Content>
// </Dialog>
```

---

## Polymorphic Components

Allow components to render as different HTML elements or components.

```tsx
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithRef<C>, PropsToOmit<C, Props>>;

// Text component that can render as any element
interface TextOwnProps {
  size?: 'sm' | 'md' | 'lg';
  weight?: 'regular' | 'medium' | 'bold';
  color?: string;
}

type TextProps<C extends React.ElementType = 'span'> = PolymorphicComponentProp<C, TextOwnProps>;

export function Text<C extends React.ElementType = 'span'>({
  as,
  size = 'md',
  weight = 'regular',
  color,
  children,
  className,
  ...props
}: TextProps<C>) {
  const Component = as || 'span';
  return (
    <Component className={cn('ds-text', `ds-text--${size}`, className)} {...props}>
      {children}
    </Component>
  );
}

// Usage:
// <Text as="h1" size="lg" weight="bold">Heading</Text>
// <Text as="p">Paragraph</Text>
// <Text as={Link} href="/about">Link text</Text>
```

---

## Accessibility Requirements

Every component must meet WCAG 2.1 AA.

### Checklist

- [ ] **Keyboard navigation** — all interactive elements reachable and operable via keyboard
- [ ] **Focus management** — visible focus ring, correct tab order
- [ ] **ARIA roles** — correct semantic role (`button`, `dialog`, `menu`, etc.)
- [ ] **ARIA labels** — `aria-label` or `aria-labelledby` for unlabeled elements
- [ ] **ARIA states** — `aria-expanded`, `aria-selected`, `aria-disabled`, `aria-checked` as appropriate
- [ ] **Color contrast** — minimum 4.5:1 for normal text, 3:1 for large text
- [ ] **No color-only information** — don't use color as the sole error indicator
- [ ] **Motion** — respect `prefers-reduced-motion`
- [ ] **Screen reader testing** — test with VoiceOver (Mac) + NVDA (Windows)

### Reduced Motion Pattern

```css
@media (prefers-reduced-motion: reduce) {
  .ds-button__spinner {
    animation: none;
  }
  .ds-transition {
    transition: none !important;
  }
}
```

---

## Documentation Template

Every component's Storybook `stories.tsx` should include:

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],          // enables auto-generated docs page
  parameters: {
    docs: {
      description: {
        component: 'Triggers an action or navigates. Use for primary user actions.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      description: 'Visual style of the button',
    },
    size: {
      control: 'select',
    },
    isLoading: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

// Default story (shown in docs as the primary example)
export const Default: Story = {
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'md',
  },
};

// All variants
export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};

// Loading state
export const Loading: Story = {
  args: { children: 'Saving...', isLoading: true },
};

// Disabled state
export const Disabled: Story = {
  args: { children: 'Disabled', disabled: true },
};
```

---

## Vue 3 Patterns

### Props with TypeScript

```vue
<!-- Button.vue -->
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  isLoading: false,
  isDisabled: false,
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

// Expose ref for parent access
defineExpose({ focus: () => buttonRef.value?.focus() });
</script>

<template>
  <button
    :class="['ds-button', `ds-button--${variant}`, `ds-button--${size}`]"
    :disabled="isDisabled || isLoading"
    :aria-busy="isLoading"
    @click="emit('click', $event)"
  >
    <slot />
  </button>
</template>
```

### Provide/Inject for Context

```ts
// composables/useFormContext.ts
import { provide, inject, type InjectionKey } from 'vue';

interface FormContext {
  isDisabled: Ref<boolean>;
  size: Ref<'sm' | 'md' | 'lg'>;
}

const FormContextKey: InjectionKey<FormContext> = Symbol('FormContext');

export function provideFormContext(ctx: FormContext) {
  provide(FormContextKey, ctx);
}

export function useFormContext() {
  return inject(FormContextKey);
}
```
