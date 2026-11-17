---
name: agent-payment-policy
description: Bind a buyer-owned response contract to an agent payment decision and validate the settled output before accepting delivery. Use when an agent is evaluating, authorizing, executing, or reviewing an x402, MPP, HTTP 402, paid API, paid MCP, or other machine-commerce request; when required JSON fields, types, formats, bounds, or freshness must survive from intent through receipt; or when wallet and budget controls exist but paid-output integrity is still missing.
---

# Agent payment policy

Treat payment success and delivery validity as separate decisions. Use this
workflow before an agent accepts a paid JSON response.

## Keep the trust boundary explicit

- Let the seller's OpenAPI or marketplace schema establish what it claims to
  return and whether the request is constructible.
- Define a separate buyer-owned JSON Schema for the minimum acceptable result.
- Compile and inspect that schema before network, credential, balance, signer,
  or wallet work.
- Bind the canonical schema digest into the immutable intent and signed
  authorization. Never authorize from a mutable file path alone.
- Validate the exact settled response body against the bound schema before
  treating delivery as successful.
- Preserve payment settlement and output validation as independent receipt
  fields. A paid response can still be invalid.

This skill complements wallet, budget, x402, and MPP execution tools. It does
not create a wallet, sign a payment, choose a facilitator, or authorize spend.

## Speak the package as decide, bind, and classify

A foreign agent can use this package without Pilot private buyer code, a
wallet, or a facilitator. Official clients can still pay a SameDayDesk 402
without it. Durable Ed25519 policy signing stays library-only.

| Verb | Use it to | CLI | Library |
| --- | --- | --- | --- |
| **decide** | Inspect constructibility and plan viability | `construct-request`, `plan-check`, `inspect-url`, `output-schema-check` | `constructRequest`, `createPlan`, `normalizeRequest`, `inspectOutputSchema` |
| **bind** | Bind a finished request or verify a signed plan | `construct-request`, `verify-authorization`, `verify-execution` | `constructRequest`, `verifyAuthorization`, `verifyExecutionAuthorization` |
| **classify** | Accept a local body or classify caller-verified facts | `output-accept`, `receipt-completeness-check` | `inspectOutputSchema` → `prepareOutputValidator` → `validateOutput`, `evaluateReceiptCompleteness` |

Refuse unfinished URLs. Bare `/extract` is `not_constructible`. A finished
example such as
`https://agents.samedaydesk.com/extract?url=https://example.com` binds.
`requirePurchaseEvidence` stays opt-in. `receipt-completeness-check` exits `0`
by default; pass `--fail-on conflict` only when CI must halt on conflict.

## Build the buyer contract

Write a bounded JSON Schema 2020-12 document that expresses only the fields the
buyer's decision actually needs. Require types and formats, not only field
presence. Prefer `additionalProperties: false` where the response contract is
closed. Avoid remote `$ref`, executable extensions, and unbounded recursion.

Example:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["data"],
  "properties": {
    "data": {
      "type": "object",
      "additionalProperties": false,
      "required": ["source", "value", "observedAt"],
      "properties": {
        "source": { "type": "string", "format": "uri" },
        "value": { "type": "number", "minimum": 0 },
        "observedAt": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

Inspect the schema locally with an exact package version:

```bash
npm install --save-exact agent-payment-policy@0.15.0
npx agent-payment-policy output-schema-check \
  ./output-schema.json \
  data.source,data.value,data.observedAt
```

Record the returned `schemaDigest`, canonical byte count, and required paths.
Stop before wallet access if inspection or compilation fails.

## Carry the contract through authorization

Build the immutable purchase intent with:

- exact method and normalized target;
- maximum atomic amount, asset, network, and protocol constraints;
- required media type and response byte ceiling;
- required JSON paths;
- the inspected `schemaDigest`;
- freshness or content-hash constraints when the decision needs them.

Select one exact offer, freeze it in a route lock, and authorize the plan with a
separate policy identity. Reinspect the local schema immediately before
execution and require its digest to equal the authorized digest. A changed
schema requires a new authorization.

## Validate delivery

After the paid response is received:

1. enforce the authorized media type and byte ceiling;
2. parse JSON without coercion;
3. validate the whole body against the prepared buyer schema;
4. enforce freshness or content-hash constraints;
5. create a receipt that reports payment settlement and output validation
   separately;
6. release the body to downstream reasoning only when validation passes.

For library use:

```js
import {
  inspectOutputSchema,
  prepareOutputValidator,
  validateOutput,
} from "agent-payment-policy";

const requiredFields = ["data.source", "data.value", "data.observedAt"];
const inspected = inspectOutputSchema({
  schema,
  requiredFields,
});

const contract = {
  mediaType: "application/json",
  maxResponseBytes: 65536,
  requiredFields,
  schemaDigest: inspected.schemaDigest,
};

const schemaValidator = prepareOutputValidator({
  schema,
  contract,
});

const parsedBody = JSON.parse(responseText);
const result = validateOutput(parsedBody, contract, { schemaValidator });
```

`inspectOutputSchema` returns `requiredPaths`, `schemaDigest`, and
`canonicalBytes`. It does not return `requiredFields`. Repeat the same
required-path list in the output contract. `maxResponseBytes` is the byte
ceiling; `maxBytes` is ignored. `validateOutput` takes the parsed JSON value,
not raw response bytes.

Use the package README for the complete intent, planning, authorization, and
receipt APIs.

## Reconcile incomplete receipt evidence

After the rail adapter has independently verified the provider receipt,
transaction, and buyer balance, normalize only controlled match states into
`evaluateReceiptCompleteness`. Do not pass raw headers, signatures, transaction
bodies, credentials, wallet secrets, or paid output. Treat any mismatch as a
conflict. Preserve missing facts honestly and use transaction or exact balance
evidence only to supplement the dimension it actually proves.

The completeness report does not replace output validation. A payment can be
reconciled while delivery is invalid, and valid delivery does not prove
settlement.

## Fail closed at the right stage

- Missing or invalid buyer schema: stop before network and wallet work.
- Seller schema cannot guarantee required paths: reject during procurement.
- Authorized schema digest differs from local schema: require reauthorization.
- Paid body fails schema validation: record settlement accurately, mark
  delivery invalid, and do not pass the body downstream.
- Binary or streaming response: use a separate bounded contract or leave this
  JSON workflow rather than silently weakening it.

Do not claim that seller conformance proves truth, freshness, or business
quality. The schema proves only that the delivered bytes satisfy the buyer's
declared structural acceptance contract.
