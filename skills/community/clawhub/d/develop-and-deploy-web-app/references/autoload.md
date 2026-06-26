# Autoload Integration Guide

Use this reference to make the generated app compatible with platform auto-loading from `workspaces/web-apps/`.

## Assumption

The platform exposes each generated project at:

```text
http://host:{port}/{token}/
```

The app must therefore behave correctly under a non-root base path.

## Frontend Requirements

- Set the Vite build `base` to `/${token}/`.
- Avoid hard-coded root-relative asset URLs such as `/logo.svg` unless they are rewritten through the same base path.
- If React Router is used, set its basename to `/${token}`.
- Prefer relative fetch helpers or a single computed API base so browser requests resolve to `/${token}/api/...`.

## Backend Requirements

- Mount the app router under `/${token}`.
- Keep API routes under `/${token}/api`.
- Serve static frontend assets from the built `client/dist` directory under the same mount point.
- Return the built `index.html` for non-API requests inside that mounted subpath.

## Suggested Pattern

Compute a single base path string once and reuse it in both the build config and the server:

```text
basePath = /{token}
```

Then derive:

- public page URL: `{basePath}/`
- API root: `{basePath}/api`
- static mount: `{basePath}/assets/...`

## Verification

Confirm all of the following:

1. Opening `http://host:{port}/{token}/` loads HTML successfully.
2. CSS and JS assets load without 404 errors.
3. Browser refresh on a client route still works.
4. API requests resolve to the mounted subpath rather than `/api` at the origin root.
