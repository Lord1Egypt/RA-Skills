import { defineConfig } from 'vitest/config';
import path from 'path';

/**
 * E2E test config — runs against a live ClawSite API (dev or prod).
 *
 * Usage:
 *   CLAWSITE_E2E_API_URL=https://api.dev.clawsite.ai \
 *   CLAWSITE_E2E_PARTNER_SECRET=<secret> \
 *   npm run test:e2e
 *
 * If env vars are unset, individual tests `describe.skip` themselves so the
 * suite still runs (and reports "skipped") rather than crashing on import.
 *
 * Each test creates a fresh account against a randomly-generated MBID UUID
 * and cleans up its sites in afterAll. Worst case (afterAll fails): a
 * leftover account row in DDB pinned to a UUID nobody else uses.
 */
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/e2e/**/*.test.ts'],
    // E2E hits the network — long timeouts. CloudFront propagation alone
    // routinely takes 5-20s, so we budget 60s per test, 120s for the
    // full lifecycle (which runs ~6 sequential network calls + cache wait).
    testTimeout: 120_000,
    hookTimeout: 60_000,
    // Run sequentially — each test creates DDB / S3 / CloudFront state, and
    // the CloudFront purge quota (5/hr per account) means parallel test
    // accounts could trip rate limits if anything reuses creds.
    fileParallelism: false,
    sequence: { concurrent: false },
  },
  resolve: {
    alias: {
      '@lib': path.resolve(__dirname, './src/lib'),
      '@handlers': path.resolve(__dirname, './src/handlers'),
      '@middleware': path.resolve(__dirname, './src/middleware'),
    },
  },
});
