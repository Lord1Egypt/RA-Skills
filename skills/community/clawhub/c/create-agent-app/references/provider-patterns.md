# Provider Patterns

Centralize provider configuration. Do not scatter `process.env.X` outside `src/config/env.ts`.

## Shared Env Contract

Use `.env.example` with variable names only:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=

# optional OpenAI-compatible
OPENAI_COMPATIBLE_BASE_URL=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_MODEL=
```

Use `zod` in `src/config/env.ts` to validate required fields for the selected provider. Fail fast with a clear configuration error.

## openai-direct

Use the official OpenAI SDK and Responses API when the app is a minimal backend, CLI, or service and does not need a cross-provider UI abstraction.

Expected properties:

- real API key required for live smoke
- no mock fallback when the API is unavailable
- provider module exports a small typed interface used by the harness

## ai-sdk

Use Vercel AI SDK when the app is a Next.js or streaming web UI and the provider/model abstraction is useful.

Expected properties:

- provider selection remains centralized
- server code owns tool execution and approvals
- UI renders stream state; it does not bypass the harness

## mastra

Use Mastra when the app needs a richer agent/workflow/tool/memory harness.

Expected properties:

- workflow or agent definitions live in a dedicated module
- memory and artifact policy are explicit
- validation includes a harness-level smoke, not only app build

## openai-compatible

Use `baseURL + apiKey + model` for ARK, vLLM, LiteLLM, gateways, or other compatible endpoints.

Expected properties:

- no assumption that every OpenAI feature is supported
- capability checks or clear unsupported-feature errors for tools, structured output, streaming, or reasoning fields
- endpoint-specific settings stay in config, not prompt text

## custom provider adapter

Use only when none of the standard patterns fit. Keep the adapter narrow:

- `generate` or `respond`
- optional streaming
- explicit tool-call capability
- typed error surface

