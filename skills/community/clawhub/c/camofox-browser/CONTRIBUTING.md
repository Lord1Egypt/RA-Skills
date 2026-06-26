# Contributing to camofox-browser

## Environment Variable Security

**Do not pass the host environment to child processes.** This is a hard rule.

When spawning child processes (e.g., the server from the plugin), only pass an explicit whitelist of environment variables. Never use `...process.env` or equivalent spreads.

```typescript
// WRONG — leaks all host secrets to the child process
spawn("node", [serverPath], {
  env: { ...process.env, CAMOFOX_PORT: "9377" },
});

// RIGHT — only what the child actually needs
spawn("node", [serverPath], {
  env: {
    PATH: process.env.PATH,
    HOME: process.env.HOME,
    NODE_ENV: process.env.NODE_ENV,
    CAMOFOX_PORT: "9377",
  },
});
```

If the child process needs a new env var, add it to the whitelist explicitly in both `plugin.ts` and `tests/helpers/startServer.js`.

**Do not use `dotenv` or load `.env` files.** The server reads its configuration from explicitly passed environment variables only. Users running camofox alongside other tools may have `.env` files with secrets that should never be loaded into this process.

## Testing

```bash
npm test              # e2e tests
npm run test:live     # live site tests (requires RUN_LIVE_TESTS=1)
npm run test:debug    # with server output (DEBUG_SERVER=1)
```

## Code Style

- No comments explaining what the code does — keep it readable without them
- Use `const` by default, `let` only when reassignment is needed
- Error responses: `{ error: "message" }` with appropriate HTTP status codes
- All tab operations require `userId` for session isolation
