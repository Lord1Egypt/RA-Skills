## Nuxt Integration

Aligned with [Getting Started with Nuxt.js and BCMS](https://thebcms.com/docs/integrations/nuxt-js).

### Quick start (CLI)

```bash
npx @thebcms/cli create nuxt starter simple-blog
```

The CLI sets up BCMS sample content, scaffolds Nuxt, and writes env configuration.

### Manual setup

1. Create a Nuxt app: `npx nuxi@latest init <project-name>`
2. Install: `npm i --save @thebcms/nuxt @thebcms/types`
3. Configure `nuxt.config.ts` as in the official guide (API keys as **strings** inside `options`):

   ```ts
   export default defineNuxtConfig({
     bcms: {
       privateClientOptions: {
         options: {
           apiKey: process.env.BCMS_API_KEY!,
           injectSvg: true,
         },
       },
       publicClientOptions: {
         options: {
           apiKey: process.env.NUXT_PUBLIC_BCMS_API_KEY!,
           injectSvg: true,
         },
       },
     },
     modules: ['@thebcms/nuxt'],
   });
   ```

4. `.env`:

   ```bash
   BCMS_API_KEY=<YOUR.API.KEY>
   NUXT_PUBLIC_BCMS_API_KEY=<YOUR.PUBLIC.API.KEY>
   ```

5. Use composables anywhere in the app:

   ```ts
   const bcms = useBcmsPrivate();
   const blogs = (await bcms.entry.getAll('blog')) as BlogEntry[];
   ```

If a future `@thebcms/nuxt` version documents a different config shape, follow that module’s readme—the [published Nuxt integration](https://thebcms.com/docs/integrations/nuxt-js) above is the default reference.
