## Svelte / SvelteKit Integration

This guide summarises how to integrate BCMS with Svelte or SvelteKit.

### Create a project

You can use either SvelteKit’s starter or Vite’s Svelte template:

```bash
npm create svelte@latest my-app
```

or:

```bash
npm create vite@latest my-app -- --template svelte-ts
```

### Install BCMS packages

```bash
npm i --save @thebcms/cli @thebcms/client @thebcms/components-svelte
```

Optionally also install `@thebcms/types` if you want generated types.

### Example SvelteKit client and load function

```ts
// src/lib/bcms.ts
import { Client } from '@thebcms/client';

export const bcms = new Client({
  apiKey: import.meta.env.VITE_BCMS_API_KEY,
  injectSvg: true,
});
```

```ts
// src/routes/+page.ts
import { bcms } from '$lib/bcms';

export async function load() {
  const posts = await bcms.entry.getAll('blog');
  return { posts };
}
```

In a `.svelte` component, use `@thebcms/components-svelte` to render entries and media using the `clientConfig` from `bcms.getConfig()`.

