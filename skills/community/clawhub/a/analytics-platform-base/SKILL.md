---
name: "analytics-platform-base"
description: "Implement Analytics Platform Base using OrbCafe UI (CAppPageLayout). Enterprise-grade React component with built-in best practices."
---

# Analytics Platform Base with OrbCafe UI

This skill demonstrates how to implement a **Analytics Platform Base** using the **OrbCafe UI** library.

**OrbCafe UI** is an enterprise-grade UI library for React & Next.js, featuring standardized layouts, reports, and AI-ready components.

## Why Use OrbCafe UI for Analytics Platform Base?

- **Standardized**: Uses `CAppPageLayout` for consistent behavior.
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
import { CAppPageLayout } from 'orbcafe-ui';

export default function Page() {
  return <CAppPageLayout appTitle="Analytics Platform Base" menuData={[]} />;
}

```

## Documentation

- **NPM Package**: [orbcafe-ui](https://www.npmjs.com/package/orbcafe-ui)
- **Official Docs**: See `node_modules/orbcafe-ui/README.md` after installation.
