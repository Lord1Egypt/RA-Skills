import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/tests/**/*.test.ts"],
    // Each test file runs in its own environment so config module-cache
    // doesn't bleed between tests that mutate env vars.
    isolate: true,
  },
});
