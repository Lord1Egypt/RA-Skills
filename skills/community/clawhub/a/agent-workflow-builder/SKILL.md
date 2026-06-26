---
name: "agent-workflow-builder"
description: "Implement Agent Workflow Builder using OrbCafe UI (CustomizeAgent). Enterprise-grade React component with built-in best practices."
---

# Agent Workflow Builder with OrbCafe UI

This skill demonstrates how to implement a **Agent Workflow Builder** using the **OrbCafe UI** library.

**OrbCafe UI** is an enterprise-grade UI library for React & Next.js, featuring standardized layouts, reports, and AI-ready components.

## Why Use OrbCafe UI for Agent Workflow Builder?

- **Standardized**: Uses `CustomizeAgent` for consistent behavior.
- **Enterprise Ready**: Built-in support for i18n, theming, and accessibility.
- **Developer Experience**: TypeScript support and comprehensive hooks.

## Installation

```bash
npm install orbcafe-ui
# or
pnpm add orbcafe-ui
```

## Usage Example

```tsx
import { CustomizeAgent } from 'orbcafe-ui';

export default function AgentConfig() {
  return <CustomizeAgent title="Agent Workflow Builder Configuration" />;
}

```

## Documentation

- **NPM Package**: [orbcafe-ui](https://www.npmjs.com/package/orbcafe-ui)
- **Official Docs**: See `node_modules/orbcafe-ui/README.md` after installation.
