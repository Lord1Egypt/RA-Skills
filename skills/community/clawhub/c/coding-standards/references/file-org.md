# File Organization & Naming

## Project Structure

```bash
src/
├── app/               # Next.js App Router
│   ├── api/           # API routes
│   ├── markets/       # Market pages
│   └── (auth)/        # Auth pages (route groups)
├── components/        # React components
│   ├── ui/            # Generic UI components
│   ├── forms/         # Form components
│   └── layouts/       # Layout components
├── hooks/             # Custom React hooks
├── lib/               # Utilities and configs
│   ├── api/           # API clients
│   ├── utils/         # Helper functions
│   └── constants/     # Constants
├── types/             # TypeScript types
└── styles/            # Global styles
```

## File Naming Conventions

```bash
components/Button.tsx         # PascalCase for components
hooks/useAuth.ts              # camelCase with 'use' prefix
lib/formatDate.ts             # camelCase for utilities
types/market.types.ts         # camelCase with .types suffix
```

## Organizing Imports

```typescript
// 1. External dependencies
import React, { useState } from 'react'
import { z } from 'zod'

// 2. Relative imports (lib, utils, config)
import { API_BASE_URL } from '@/lib/constants'
import { formatDate } from '@/lib/utils'

// 3. Components and types
import { Button } from '@/components/Button'
import type { Market } from '@/types/market.types'
```

## Collocating Related Files

Keep related files together:

```bash
components/
├── MarketCard/
│   ├── MarketCard.tsx
│   ├── MarketCard.test.tsx
│   ├── useMarketCard.ts
│   └── MarketCard.types.ts

lib/
├── api/
│   ├── markets.ts       # Market API client
│   ├── users.ts         # User API client
│   └── __tests__/       # API tests
```

## Constants Organization

```typescript
// lib/constants.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000'

export const MARKET_STATUSES = ['active', 'resolved', 'closed'] as const

export const PAGINATE = {
  DEFAULT_LIMIT: 10,
  MAX_LIMIT: 100
}

export const TIMINGS = {
  DEBOUNCE_MS: 500,
  REQUEST_TIMEOUT_MS: 10000
}
```

## Avoid These Patterns

```typescript
// Bad: Generic 'utils' folder with unrelated code
utils/
├── parseDate.ts
├── api.ts
├── math.ts
├── validation.ts
└── random.ts

// Good: Organized by domain
lib/
├── date/
│   └── parseDate.ts
├── api/
│   └── client.ts
├── math/
│   └── calculate.ts
└── validation/
    └── schema.ts
```
