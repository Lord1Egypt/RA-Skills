## Astro Integration

This guide summarises how to integrate BCMS with an Astro project.

### Quick start (CLI)

```bash
npx @thebcms/cli create astro starter simple-blog
```

The CLI:

- Sets up a BCMS project and sample content.
- Scaffolds an Astro blog.
- Generates environment configuration and clients.

### Manual setup

1. Create an Astro project:

   ```bash
   npm create astro@latest
   ```

2. Install BCMS packages:

   ```bash
   npm i --save @thebcms/cli @thebcms/client @thebcms/components-astro @thebcms/types @thebcms/utils
   ```

3. Add scripts to `package.json`:

   ```json
   {
     "scripts": {
       "dev": "bcms --pull types --lng ts && astro dev",
       "start": "bcms --pull types --lng ts && astro dev",
       "build": "bcms --pull types --lng ts && astro check && astro build",
       "preview": "bcms --pull types --lng ts && astro preview",
       "astro": "astro"
     }
   }
   ```

4. Create `bcms.config.cjs` for `@thebcms/cli` per [BCMS docs](https://thebcms.com/docs), using environment variables for secrets.

5. Initialise:

   - A **private** client for server‑side code using `import.meta.env.BCMS_*`.
   - A **public** client for client‑side code using `import.meta.env.PUBLIC_BCMS_*`.

6. Use `@thebcms/components-astro` components to render content and media in Astro pages.

