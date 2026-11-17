# AnyAPI - SDKs and direct HTTP

Reference for building AnyAPI into an application. The main skill is at https://getanyapi.com/SKILL.md.

### SDKs - build AnyAPI into your app

Use an official SDK when AnyAPI should become part of the product flow rather than an agent-only tool, and your app is written in TypeScript, JavaScript, Node, or Python. The SDKs are the recommended integration path for those languages: prefer them over hand-rolling HTTP. They give you a typed method per SKU, handle auth, and track the catalog because they are generated from the same `openapi.json`.

Routing rule:

- **Node, TypeScript, or JavaScript runtime** - install `@getanyapi/sdk` with `npm install @getanyapi/sdk` (zero runtime deps, ESM + CJS, Node 18+ and edge runtimes).
- **Python** - `pip install getanyapi` (httpx + pydantic v2, Python 3.10+, sync and async clients).
- **Any other language, or when you want zero dependencies** - fall back to the raw REST call below.

Build workflow, either language:

1. Inspect the project and decide where the API call belongs. For browser apps, keep the AnyAPI key on your server and expose only your own backend route to the browser.
2. Mint a **dedicated key for this app**: a dashboard key for anything that ships, or a free trial key via self-signup for a quick prototype. Store it only in the `ANYAPI_API_KEY` environment variable. Never hardcode it and never commit it.
3. Read the SKU input schema (`anyapi describe <sku>`, `GET https://api.getanyapi.com/v1/apis/{sku}`, or the SDK's typed method signature) and mirror it in your form or job.
4. Write the call site against the typed SDK method.
5. Handle HTTP 402 `trial_cap_reached` (the trial budget is spent) by surfacing the upgrade link from the error body to the human; anything that ships should run on a dashboard key.
6. Smoke-test one cheap call and verify the response shape, `provider: "AnyAPI"`, and `costUsd`.

TypeScript SDK example (reads `ANYAPI_API_KEY` from the environment):

    import { AnyAPI } from "@getanyapi/sdk";

    const client = new AnyAPI({ apiKey: process.env.ANYAPI_API_KEY });

    const res = await client.google.search({ query: "best coffee maker" });
    console.log(res.output, res.costUsd);

Every SKU is a typed method under its platform namespace (`client.amazon.reviews(...)`, `client.reddit.search(...)`); `res.costUsd` is the USD you were charged. You can also call any SKU generically by slug with `client.run("amazon.reviews", { ... })`.

Python SDK example (`AnyAPI()` reads `ANYAPI_API_KEY` from the environment):

    from getanyapi import AnyAPI

    client = AnyAPI()
    res = client.google.search(query="best coffee maker")
    print(res.output, res.cost_usd)

An `AsyncAnyAPI` variant offers the same methods with `await`. Input keyword arguments mirror the wire API; output attributes are snake_case (`res.cost_usd`).

**Fallback - raw REST fetch** (other languages, or when you want zero dependencies). Mint the key as above, then call `POST https://api.getanyapi.com/v1/run/{sku}` directly:

    type RunResponse<TOutput> = {
      output: TOutput;
      provider: "AnyAPI";
      costUsd: number;
      items?: number;
      resultId?: string; // free re-read via GET /v1/results/{id} (section 4)
      jqError?: string;  // set when a jq expression failed; output is then unshaped
    };

    export async function runAnyApi<TOutput>(
      sku: string,
      input: Record<string, unknown>,
    ): Promise<RunResponse<TOutput>> {
      const apiKey = process.env.ANYAPI_API_KEY;
      if (!apiKey) throw new Error("Missing ANYAPI_API_KEY");

      const res = await fetch(
        "https://api.getanyapi.com/v1/run/" + encodeURIComponent(sku),
        {
          method: "POST",
          headers: {
            Authorization: "Bearer " + apiKey,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(input),
        },
      );

      if (res.status === 402) {
        throw new Error("AnyAPI trial budget spent. Open the upgrade link in the error body.");
      }
      if (!res.ok) {
        throw new Error("AnyAPI run failed: " + res.status + " " + (await res.text()));
      }
      return (await res.json()) as RunResponse<TOutput>;
    }

For a fully typed client in a language without an official SDK, generate one from https://api.getanyapi.com/openapi.json.

### REST - direct HTTP

Use REST when you want direct HTTP calls from scripts, backends, jobs, or custom agent tooling.

Base URL `https://api.getanyapi.com/v1`, Bearer auth on every request.

    curl -X POST https://api.getanyapi.com/v1/run/{sku} \
      -H "Authorization: Bearer aa_live_..." \
      -H "Content-Type: application/json" \
      -d '{ ...input matching the API schema... }'

Provider-job APIs require a unique `Idempotency-Key`. They wait 10 seconds by default; use `Prefer: respond-async` for immediate acceptance or `Prefer: wait=N` (maximum 90 seconds). A `202 Accepted` returns a durable `requestId`, `Location`, and `Retry-After`: poll `GET /requests/{requestId}` and never repeat the paid POST. Successful output is retrievable there for 24 hours; request metadata remains after `resultExpired: true`. These async APIs require an authenticated wallet and are unavailable through x402, MPP, and anonymous/public-tool payment.

Other endpoints: `GET /apis?category=...` (browse), `GET /apis/{sku}` (describe, including nullable latency observations), `GET /balance`. Ranked public search is `GET /catalog/search?q=...`; the public browse catalog (no auth) is at https://api.getanyapi.com/catalog. A typed OpenAPI document is at https://api.getanyapi.com/openapi.json.
