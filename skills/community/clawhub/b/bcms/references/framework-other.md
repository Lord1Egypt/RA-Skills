## Other Environments

The BCMS client SDK is framework‑agnostic and works in many JavaScript and TypeScript environments.
This guide summarises a few common patterns.

### Standard client constructor

```ts
import { Client } from '@thebcms/client';

export const bcms = new Client({
  injectSvg: true,
});
```

Set **`BCMS_API_KEY`** to the full three‑part string (`keyId.secret.instanceId`). See [thebcms.com/docs](https://thebcms.com/docs).

Always read API keys from environment variables, never hard‑code them.

---

### Standalone JavaScript / Node.js

Use BCMS in scripts, cron jobs, or CLI tools:

```ts
import { Client } from '@thebcms/client';

const bcms = new Client({ injectSvg: true });

async function run() {
  const entries = await bcms.entry.getAll('products');
  console.log(`Total products: ${entries.length}`);
}

run();
```

---

### Astro / Svelte / others without full integration

Even outside official integrations, you can:

- Create a client in a shared module.
- Use it in build scripts or server‑side rendering.
- Pass parsed data into templates/components as props.

See the dedicated framework files for concrete examples.

---

### Serverless and Docker

BCMS works in Docker and serverless environments (Vercel, Netlify, AWS Lambda, etc.) as long as:

- Secrets are provided via environment variables.
- The client is initialised per request or per container (avoid global websockets in short‑lived functions).

Example (pseudo‑Lambda handler):

```ts
export async function handler() {
  const entries = await bcms.entry.getAll('blog');
  return {
    statusCode: 200,
    body: JSON.stringify(entries),
  };
}
```

---

### Static site generators

For generators like Hugo or Eleventy, you can:

- Run a Node script that fetches BCMS data.
- Write the content to JSON/Markdown files.
- Let the static generator consume those files.

This pattern decouples BCMS from the generator and keeps the build pipeline simple.

