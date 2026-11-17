# JavaScript and TypeScript production pattern

Read `process.env.DATAIFY_API_TOKEN`; use `AbortSignal.timeout()` or an `AbortController`; check `response.ok` before decoding; validate unknown JSON before use. Retry only safe reads on 429/5xx with a bounded loop and jitter. Persist a Builder task ID immediately. Represent success, terminal failure, and resumable timeout as a discriminated union instead of returning only a string ID.
