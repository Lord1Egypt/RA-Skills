# JSON arguments and write safety

Use JSON mode when a create, update, batch, or nested request would require many error-prone flags.
`defineCommand` still has one `args` property and Zod remains the only schema and type source.

```ts
import * as z from "zod";
import { defineCommand } from "@renxqoo/agent-cli-sdk";

const CreateOrder = z
  .strictObject({
    customerId: z.string(),
    items: z.array(
      z.strictObject({
        sku: z.string(),
        quantity: z.number().int().positive(),
      }),
    ),
    address: z.strictObject({ country: z.string(), city: z.string(), line1: z.string() }),
    remark: z.string().optional(),
  })
  .register(z.globalRegistry, {
    sensitive: ["/remark"],
    examples: [
      {
        customerId: "c1",
        items: [],
        address: { country: "CN", city: "Shanghai", line1: "Example Road 1" },
      },
    ],
  });

export const create = defineCommand({
  name: "create",
  description: "Create an order",
  args: { type: "json", schema: CreateOrder },
  policy: {
    mode: "write",
    dryRun: true,
    confirmation: "required",
    idempotency: "required",
  },
  async run(ctx, args) {
    return { data: (await ctx.post("/orders", args)).data };
  },
});
```

Do not add `zodInput`, a validator adapter, Standard Schema, a parallel `input` contract, or a
manual Args type. The Zod output type is the `args` type in `run(ctx, args)`.

## Native invocation contract

Provide one complete JSON document:

```bash
my-cli create --input '{"customerId":"c1","items":[],"address":{"country":"CN","city":"Shanghai","line1":"Example Road 1"}}' --idempotency-key create-1 --yes
my-cli create --input-file ./order.json --idempotency-key create-1 --yes
my-cli create < ./order.json --idempotency-key create-1 --yes
generate-order | my-cli create --idempotency-key create-1 --yes
```

There is no `--input-stdin`; redirected or piped stdin is the native shell interface. `--input` and
`--input-file` are mutually exclusive. Business flags and positional operands are invalid in JSON
mode, so input is never partially merged. Prefer files or stdin for secrets.

```bash
my-cli create --input-schema | jq '.data.schema'
my-cli create --input-example | jq '.data.example'
```

## Guarantees and policy

The runtime bounds bytes, rejects symbolic-link files, decodes fatal UTF-8, strictly parses JSON,
rejects duplicate/prototype-polluting keys and unsafe integers, then validates the Zod object.
Errors never echo the raw document.

`policy` is separate from business args:

- `--dry-run` validates and redacts args, supplies a read-only preview context, and never calls `run`.
- `--yes` satisfies required confirmation.
- `--idempotency-key` is caller-owned, injected into requests, and reused for retries of the same
  operation. Never derive it from payload content.
- Root Zod metadata `sensitive` uses JSON Pointer paths for observer and preview redaction.

## Preserve the shell

Do not create a workflow DSL. Quoting, variables, pipes, redirects, `jq`, `tee`, `xargs`, `&&`, and
`||` remain shell features:

```bash
jq -n '{customerId:"c1",items:[],address:{country:"CN",city:"Shanghai",line1:"Example Road 1"}}' \
  | my-cli create --idempotency-key create-2 --yes \
  && my-cli get order-2

my-cli list --status pending | jq -r '.data[].id' | xargs -n1 my-cli get
my-cli list | tee orders.json | jq '.data | length'
```

The SDK owns deterministic mapping, validation, policy, stdout/stderr separation, and exit codes;
the shell owns orchestration.
