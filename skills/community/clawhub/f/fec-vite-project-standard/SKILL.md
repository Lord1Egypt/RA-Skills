---
name: fec-vite-project-standard
description: Use when creating, configuring, reviewing, or debugging Vite-based frontend projects, vite.config.ts, env variables, dev server proxy, HMR, plugin ordering, library mode, dependency pre-bundling, bundle splitting, or Vite build performance. Use framework-specific skills for React/Vue component architecture; Chinese triggers include Vite configuration, vite.config, Vite build, Vite performance.
---

# Vite Project Specifications

Design and review of Vite applications, component libraries, development servers, and build configurations.

## Purpose

Standardize Vite configurations, security boundaries, and build performance to avoid common pitfalls of development environments and production builds.

## Procedure

1. Identify the project type
   - Application projects check `root`, `base`, `server.proxy`, `envPrefix`, `build` and framework plugins first.
   - Component library projects check `build.lib`, type products, peer dependencies external and export entries first.
   - Monorepo additional checks for `server.fs.allow`, path aliases and package dependency boundaries.

2. Select plugin
   - React gives priority to `@vitejs/plugin-react-swc` by default; use `@vitejs/plugin-react` only when the Babel plug-in is required.
   - The Vue project uses `@vitejs/plugin-vue`, and path aliases are given priority to `vite-tsconfig-paths`.
   - TypeScript projects must complete type checking via `tsc --noEmit`, CI or `vite-plugin-checker`.

3. Manage environment variables
   - Clients only read explicitly exposed prefixes, such as `VITE_`.
   - The third parameter of `loadEnv` uses an explicit prefix array and does not use an empty string to load all variables.
   - Keys, database addresses, and private tokens must stay on the server or build system and not enter the client bundle.

4. Optimize development experience
   - Use `vite --profile` to locate plug-in, parsing or pre-built bottlenecks before slow start.
   - Use `optimizeDeps.include` for CJS/UMD dependencies to handle interop issues.
   - Large projects can use `server.warmup.clientFiles` to warm up the core entrance.

5. Optimize production builds
   - Run `vite build` before release and use `vite preview` to do local build smoke testing.
   - Prioritize manual subcontracting by using stable object forms to avoid splitting each dependency into independent small chunks.
   - The production sourcemap is turned off by default; if uploaded to the error tracking platform, it will not be published with the site after uploading.
   - Motion effects, 3D, charts, editors, maps, and audio and video processing libraries are prioritized for isolation through dynamic import or route-level unpacking.
   - Check whether static resources go into the correct directory, have been hashed/cache, have placeholder URLs, or are too large uncompressed media.

## Minimal Config

```ts
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), ["VITE_"]);

  return {
    plugins: [react(), tsconfigPaths()],
    define: {
      __PUBLIC_API_URL__: JSON.stringify(env.VITE_API_URL),
    },
    server: {
      proxy: {
        "/api": {
          target: "http://localhost:8080",
          changeOrigin: true,
        },
      },
    },
  };
});
```

## Constraints

- `vite build` only translates and packages, not type checking; CI must run typecheck separately.
- `VITE_` is not a security boundary; any `VITE_` variable goes into the client package.
- Do not set `envPrefix: ""`, do not use `loadEnv(mode, root, "")` and then `define` at will.
- Legacy plugins are not introduced by default; only enable them when needed for real user data.
- Don't use `vite preview` as a production server.
- Component libraries must externalize peer dependencies and produce `.d.ts` separately.
- Do not inject server keys into clients via `define`, `import.meta.env` or empty prefix `loadEnv`.
- Do not put heavy libraries such as GSAP, Three.js, Lottie, Monaco, and Map SDK into all page sharing entries; first evaluate the impact of async chunk and first screen.

## Expected Output

The output should include project type judgment, key configuration changes, environment variable security instructions, and build/development performance verification methods. When completed, the Vite configuration should be type-checked, buildable, secret-secure, and explain the differences between dev and build.
