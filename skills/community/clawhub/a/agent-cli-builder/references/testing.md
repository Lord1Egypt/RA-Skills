# Testing and Real-Task Evaluation

Code tests verify the CLI contract. Forward evaluation verifies that an agent can use the Skill to complete a task. Neither replaces the other.

## Contents

1. Test matrix
2. Command tests with `createTestCtx`
3. End-to-end tests with `app.run(argv)`
4. Security and package validation
5. Skill forward evaluation

## 1. Test matrix

| Layer              | Verifies                                      | Minimum coverage                             |
| ------------------ | --------------------------------------------- | -------------------------------------------- |
| Command unit tests | Request mapping, transformation, typed errors | Happy path, empty, boundary, backend failure |
| CLI end-to-end     | argv, routes, plugins, output, exit code      | JSON success, validation error, HTTP error   |
| Structured input   | sources, Zod, redaction, write policy, stdin  | Valid source, limits, discovery, policy      |
| Build and package  | ESM entry, bin, file list                     | Build, `--help`, package dry-run             |
| Skill validation   | Frontmatter, links, AUTO-GEN                  | Validator                                    |
| Forward evaluation | Triggering, calls, safety, final result       | Typical, paraphrase, exclusion, failure      |

Use mocks, sandboxes, or dedicated records for every write. Never use production credentials or data without explicit authorization.

## 2. Command tests with `createTestCtx`

`createTestCtx` mocks the low-level request, so every `get/post/...` call uses the same transport:

```ts
import { createTestCtx } from "@renxqoo/agent-cli-sdk";

it("maps limit and returns items", async () => {
  let captured: { path?: string; query?: Record<string, unknown> } = {};
  const ctx = createTestCtx({
    request: async (options) => {
      captured = options;
      return { status: 200, data: { items: [{ id: "t_1" }] }, headers: {} };
    },
  });

  const result = await todoCommands.list.run(ctx, { limit: 5 });
  expect(captured).toMatchObject({ path: "/todos", query: { limit: 5 } });
  expect(result?.data).toEqual([{ id: "t_1" }]);
});
```

Reject unexpected requests immediately:

```ts
request: async (options) => {
  if (options.path === "/todos") {
    return { status: 200, data: { items: [] }, headers: {} };
  }
  throw new Error(`unexpected ${options.method} ${options.path}`);
};
```

Rules:

- Return `status`, `data`, and `headers` in every mock response.
- `createTestCtx` does not run `defineCli` assembly, plugin lifecycle, or `errorOnStatus`; cover them end to end.
- Inject explicit state, log, credential, and pipe mocks when required.
- Never snapshot tokens, headers, or complete sensitive responses.

For pipe tests, provide `PipeApi`:

```ts
const pipe = {
  async *in() {
    yield { type: "orders", id: "o_1", data: { id: "o_1" } };
  },
  isInPipe: () => true,
};
```

## 3. End-to-end tests with `app.run(argv)`

Cover:

- Global and command argument parsing.
- Top-level and namespaced routing.
- Plugin command, request, output, and error hooks.
- `defaultFormat`, `--json`, stdout/stderr, and exit codes.
- `errorOnStatus`, unknown commands, and output-contract violations.

Intercept process output and restore it after every test:

```ts
let stdout = "";
let stderr = "";

beforeEach(() => {
  vi.spyOn(process.stdout, "write").mockImplementation((chunk) => {
    stdout += String(chunk);
    return true;
  });
  vi.spyOn(process.stderr, "write").mockImplementation((chunk) => {
    stderr += String(chunk);
    return true;
  });
});

afterEach(() => {
  vi.restoreAllMocks();
  process.exitCode = undefined;
  stdout = "";
  stderr = "";
});
```

Minimum assertion:

```ts
await app.run(["list", "--json"]);
expect(process.exitCode).toBe(0);
expect(JSON.parse(stdout)).toMatchObject({ ok: true, source: "my-cli" });
expect(stderr).toBe("");
```

Also test an unknown command, missing argument, one mapped HTTP status, scalar data rejection, and every plugin ordering dependency. Do not test only `command.run`.

For every JSON-argument command family, cover:

- Cover inline and regular-file success, their mutual-exclusion failure, and native stdin success when neither explicit transport is supplied. Empty stdin must fail; an explicit transport takes precedence and does not consume unrelated stdin.
- Byte/depth/property/array limits, duplicate keys, unsafe keys, invalid UTF-8, and representative Zod issues without echoing raw payloads.
- `--input-schema` and `--input-example` without a payload.
- Sensitive JSON Pointer redaction in dry-run and `observeInput`.
- Dry-run never reaching `run`, required confirmation, and required caller-owned idempotency header injection.
- Native redirected/piped stdin owning the stream instead of `PipeRecord` input.

## 4. Security and package validation

Before release:

1. Run format, lint, typecheck, build, unit tests, and end-to-end tests.
2. Execute `<bin> --help`, one success, and one failure from `dist`.
3. Verify redaction of token, cookie, Authorization, and personal data in logs and errors.
4. Verify preview, confirmation, permission failure, and rollback hints for writes.
5. Dry-run the package and confirm bin, minified/bundled dist, README, Skills, and references; install the artifact and import its public API.
6. Install the package artifact in a temporary directory and read a Skill from the artifact, not the source tree.

Use a live API only in an explicitly authorized environment. Record the service and account scope, whether data is created, and how test records are cleaned up.

## 5. Skill forward evaluation

Evaluate complex or public Skills with:

1. A direct should-trigger request.
2. A paraphrase that omits command names.
3. A neighboring should-not-trigger request.
4. Missing-bin installation guidance.
5. A non-obvious argument or multi-command workflow.
6. Sensitive input, a high-risk write, or missing permission.
7. Empty data, partial failure, and insufficient evidence.

Use fresh contexts or subagents. Give them the Skill path and a realistic user request, but do not reveal the expected command, suspected bug, or intended fix. Use mocks or a sandbox if execution could mutate an external system.

Record whether the agent:

- Selected the correct Skill.
- Used the correct commands, arguments, and order.
- Respected installation, credential, and write boundaries.
- Recovered without fabricating data.
- Delivered a directly usable final result.

“Called the CLI” is not a sufficient assertion. Test non-obvious value: default traps, domain mapping, multi-step workflows, and safety boundaries.

Report what remains unverified, including security-lab scans, target-network access, production permissions, and external API stability.
