## Next.js Integration

Aligned with [Getting Started with Next.js and BCMS](https://thebcms.com/docs/integrations/next-js).

### Quick start (CLI)

```bash
npx @thebcms/cli create next starter simple-blog
```

The CLI creates a BCMS project with sample content, scaffolds Next.js, and writes `.env` with the expected variables.

### Client initialization (manual / docs pattern)

Use a **three‑part API key** in env and the **options‑only** `Client` constructor:

```ts
import { Client } from '@thebcms/client';

export const bcmsPrivate = new Client({ injectSvg: true });
// Uses BCMS_API_KEY from the environment by default

export const bcmsPublic = new Client({
  apiKey: process.env.NEXT_PUBLIC_BCMS_API_KEY,
  injectSvg: true,
});
```

`.env` (from the official guide):

```bash
BCMS_API_KEY=<YOUR.API.KEY>
NEXT_PUBLIC_BCMS_API_KEY=<YOUR.PUBLIC.API.KEY>
```

### Manual setup (summary)

1. `npx create-next-app@latest`
2. `npm i --save @thebcms/cli @thebcms/client @thebcms/components-react`
3. Add scripts so types are pulled before Next runs (official pattern):

   ```json
   {
     "scripts": {
       "dev": "bcms --pull types --lng ts && next dev",
       "build": "bcms --pull types --lng ts && next build",
       "start": "bcms --pull types --lng ts && next start",
       "lint": "bcms --pull types --lng ts && next lint"
     }
   }
   ```

   Types are written under `bcms/types/`; import entry types from there (e.g. `../../bcms/types/ts` as in the official page).

4. Configure `bcms.config.cjs` for `@thebcms/cli` as in your project and [BCMS docs](https://thebcms.com/docs) (typically aligned with the same API key / dashboard values).

5. Fetch and render with `BCMSContentManager` and `BCMSImage` from `@thebcms/components-react` (see the official guide for a full `page.tsx` example).
