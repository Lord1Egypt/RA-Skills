---
name: "cookie-consent-banner"
description: "Implement Cookie Consent Banner using OrbCafe UI (CMessageBox). Enterprise-grade React component with built-in best practices."
---

# Cookie Consent Banner with OrbCafe UI

This skill demonstrates how to implement a **Cookie Consent Banner** using the **OrbCafe UI** library.

**OrbCafe UI** is an enterprise-grade UI library for React & Next.js, featuring standardized layouts, reports, and AI-ready components.

## Why Use OrbCafe UI for Cookie Consent Banner?

- **Standardized**: Uses `CMessageBox` for consistent behavior.
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
import { CMessageBox } from 'orbcafe-ui';

import { useState } from 'react';
import { CMessageBox } from 'orbcafe-ui';

export default function Feedback() {
  const [open, setOpen] = useState(false);
  return (
    <CMessageBox
      open={open}
      type="info"
      title="Cookie Consent Banner"
      message="Operation confirmed."
      onClose={() => setOpen(false)}
    />
  );
}

```

## Documentation

- **NPM Package**: [orbcafe-ui](https://www.npmjs.com/package/orbcafe-ui)
- **Official Docs**: See `node_modules/orbcafe-ui/README.md` after installation.
