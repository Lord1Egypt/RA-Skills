# Advanced Patterns: Pagination, Pipes, and Human Output

Read only the section required by the task.

## Contents

1. Cursor pagination
2. Pipe consumers
3. `humanFormat`

## 1. Cursor pagination

Return truthful pagination metadata so an agent can decide whether to continue:

```ts
list: defineCommand({
  name: "list",
  description: "List items",
  args: {
    schema: z.object({
      cursor: z.string().describe("Continuation token from the previous result").optional(),
    }),
  },
  async run(ctx, args) {
    const res = await ctx.get<{ items: Item[]; hasMore: boolean; nextCursor?: string }>("/items", {
      cursor: args.cursor,
    });
    return {
      data: res.data.items,
      meta: {
        count: res.data.items.length,
        pagination: res.data.hasMore
          ? { complete: false, nextToken: res.data.nextCursor! }
          : { complete: true },
      },
    };
  },
});
```

Rules:

- `complete: true` means no more data; omit `nextToken`.
- `complete: false` requires a non-empty `nextToken` that can be passed to the next request.
- Do not hard-code page counts when the backend exposes only a cursor.
- Treat cursors as opaque strings. Never parse, normalize, or fabricate them.
- If backend fields are unknown, ask for a response sample. Do not implement `raw.items ?? raw.data ?? raw.records` fallbacks.

The wire contract is camelCase even when the backend uses `has_more` or `next_cursor`.

## 2. Pipe consumers

Branch on `ctx.pipe.isInPipe()`: read records when piped and accept explicit arguments otherwise.

```ts
generate: defineCommand({
  name: "generate",
  description: "Generate invoices",
  args: {
    schema: z.object({
      orderId: z.string().describe("Order ID when not reading from a pipe").optional(),
    }),
  },
  async run(ctx, args) {
    if (ctx.pipe.isInPipe()) {
      let generated = 0;
      for await (const record of ctx.pipe.in()) {
        if (record.type !== "orders") continue;
        const orderId = String(record.id ?? "");
        if (!orderId) continue;
        await ctx.post("/invoices", { orderId });
        generated += 1;
      }
      return { data: { generated } };
    }

    if (!args.orderId) {
      throw new errs.ValidationError({
        subtype: "missing_required",
        param: "--orderId",
        message: "Provide --orderId or pipe order records",
      });
    }
    const res = await ctx.post("/invoices", { orderId: args.orderId });
    return { data: res.data };
  },
});
```

`PipeRecord` contains `type`, optional `id`, optional `data`, and optional `meta`. `type` comes from the upstream success envelope's `source`, normally `defineCli.name`.

The reader accepts one complete successful JSON envelope up to 16 MiB. It does not accept NDJSON or a stream of separate JSON objects. Invalid JSON, failed envelopes, and values without `data` are rejected. `data: null` produces no records.

Piped execution forces JSON even when `--no-json` is present, protecting downstream parsing.

JSON-argument commands claim native stdin for their JSON document. The runtime supplies an empty `PipeApi` for that invocation, so the same stream cannot also carry a successful framework envelope. Choose JSON stdin or `ctx.pipe` explicitly; never guess from content.

## 3. `humanFormat`

The framework already renders arrays as tables and objects as key-value details. Add `humanFormat` only when human-facing output needs custom columns or labels.

```ts
import { defineCommand, printTable } from "@renxqoo/agent-cli-sdk";

list: defineCommand({
  name: "list",
  description: "List orders",
  humanFormat: (data) =>
    printTable(data as Order[], [
      { header: "ID", value: (row) => row.id },
      { header: "Total", value: (row) => `$${row.total}`, align: "right" },
      { header: "Status", value: (row) => row.status },
    ]),
  async run(ctx, args) {
    // ...
  },
});
```

`humanFormat(data, meta?)` returns a string and runs only in human mode. Agent calls use structured JSON, so do not duplicate business logic in the formatter.
