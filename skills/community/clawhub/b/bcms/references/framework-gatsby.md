## Gatsby Integration

This guide summarises how to integrate BCMS with a Gatsby project.

### Client initialization

Use the same pattern as [BCMS integration docs](https://thebcms.com/docs/integrations): one three‑part key per env var.

```ts
import { Client } from '@thebcms/client';

export const bcms = new Client({
  injectSvg: true,
});
// Requires BCMS_API_KEY=keyId.secret.instanceId at build/runtime where Gatsby exposes it
```

### Quick start (CLI)

```bash
npx @thebcms/cli create gatsby starter simple-blog
```

The CLI provisions a BCMS project, content, and a Gatsby blog starter.

### Manual setup

1. Create a Gatsby project:

   ```bash
   gatsby new
   ```

2. Install BCMS packages:

   ```bash
   npm i --save @thebcms/cli @thebcms/types @thebcms/utils @thebcms/client @thebcms/components-react
   ```

3. Add scripts to `package.json`:

   ```json
   {
     "scripts": {
       "develop": "bcms --pull types --lng ts && gatsby develop",
       "start": "bcms --pull types --lng ts && gatsby develop",
       "build": "bcms --pull types --lng ts && gatsby build",
       "serve": "bcms --pull types --lng ts && gatsby serve",
       "clean": "gatsby clean",
       "typecheck": "tsc --noEmit"
     }
   }
   ```

4. Configure `bcms.config.cjs` for `@thebcms/cli` per [BCMS docs](https://thebcms.com/docs) and your dashboard.

5. In `gatsby-node.ts`, use the BCMS client to fetch entries and create pages.

