---
name: building-components
description: React component building and composition best practices. Use when creating, reviewing, or refactoring React components. Covers component structure, props patterns, composition techniques, and reusability guidelines.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Building React Components

Best practices for building reusable, maintainable React components.

## When to Apply

Reference these guidelines when:
- Creating new React components
- Reviewing component structure and API design
- Refactoring components for better reusability
- Implementing component composition patterns
- Designing props interfaces

## Core Principles

### 1. Single Responsibility
Each component should do one thing well. Split large components into smaller, focused pieces.

### 2. Composition Over Inheritance
Prefer composing components together rather than complex inheritance hierarchies.

```jsx
// ✅ Good: Composition
function Page() {
  return (
    <Layout>
      <Header />
      <Main>
        <Article />
      </Main>
      <Footer />
    </Layout>
  );
}

// ❌ Avoid: Deep nesting
function Page() {
  return <LayoutWithHeaderAndFooter><MainContent /></LayoutWithHeaderAndFooter>;
}
```

### 3. Props Design
- Use TypeScript for props typing
- Keep props interfaces simple and focused
- Prefer many small props over few large objects
- Use children prop for content composition

### 4. Component Structure
```tsx
// ✅ Recommended structure
import { FC } from 'react';

interface Props {
  title: string;
  children?: React.ReactNode;
}

export const Card: FC<Props> = ({ title, children }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
};
```

### 5. State Management
- Keep state as close to where it's used as possible
- Lift state up only when necessary
- Consider custom hooks for reusable state logic

## Common Patterns

### Compound Components
For flexible APIs like Select/Option, Tabs/TabList/Tab/TabPanel.

### Render Props
For sharing behavior while keeping rendering control.

### Hooks
For sharing stateful logic across components.

## Related Skills
- vercel-react-best-practices
- next-best-practices
- vercel-composition-patterns
