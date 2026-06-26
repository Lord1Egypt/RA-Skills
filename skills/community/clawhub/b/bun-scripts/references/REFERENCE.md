# Bun API Reference

Extended reference for Bun's built-in APIs. Consult this when you need detailed signatures,
options, or less common features.

## Bun.file()

```typescript
Bun.file(path: string | URL): BunFile
Bun.file(fd: number): BunFile
```

A `BunFile` is a lazy reference — no disk I/O until you call a reader method.

| Method | Returns | Description |
|--------|---------|-------------|
| `.text()` | `Promise<string>` | Full contents as UTF-8 string |
| `.json()` | `Promise<any>` | Parsed JSON |
| `.bytes()` | `Promise<Uint8Array>` | Raw bytes |
| `.arrayBuffer()` | `Promise<ArrayBuffer>` | Raw buffer |
| `.stream()` | `ReadableStream` | Streaming read |
| `.exists()` | `Promise<boolean>` | File existence check |
| `.delete()` | `Promise<void>` | Delete the file |
| `.writer()` | `FileSink` | Incremental writer |
| `.size` | `number` | Byte count (stat, no read) |
| `.type` | `string` | MIME type |

Special handles: `Bun.stdin`, `Bun.stdout`, `Bun.stderr`.

## Bun.write()

```typescript
Bun.write(
  dest: string | BunFile | URL,
  data: string | Blob | ArrayBuffer | TypedArray | Response | BunFile
): Promise<number>  // bytes written
```

Uses fastest platform syscall (`copy_file_range` on Linux, `clonefile` on macOS).

## Bun.$ (Shell API)

```typescript
import { $ } from "bun";
```

### Output Capture

```typescript
await $`cmd`.text()          // stdout as string
await $`cmd`.json()          // stdout parsed as JSON
await $`cmd`.lines()         // async iterable of lines
await $`cmd`.blob()          // stdout as Blob
await $`cmd`.arrayBuffer()   // stdout as ArrayBuffer
```

### Options

```typescript
await $`cmd`.cwd("/path")              // working directory
await $`cmd`.env({ KEY: "value" })     // environment variables
await $`cmd`.quiet()                   // suppress stdout/stderr
await $`cmd`.nothrow()                 // don't throw on non-zero exit
await $`cmd`.timeout(5000)             // kill after 5s
```

Chain options: `await $`cmd`.cwd("/tmp").quiet().nothrow().text()`

### Redirects

```typescript
// From JavaScript objects
await $`cmd < ${Bun.file("input.txt")}`;
await $`cmd < ${new Response("data")}`;
await $`cmd < ${Buffer.from("data")}`;

// To JavaScript objects
await $`cmd > ${Bun.file("output.txt")}`;
```

### Cross-Platform Builtins

These work on all platforms without external tools:
`cd`, `ls`, `rm`, `echo`, `pwd`, `cat`, `touch`, `mkdir`, `which`, `mv`, `exit`,
`true`, `false`, `yes`, `seq`, `dirname`, `basename`.

## Bun.spawn()

```typescript
Bun.spawn(cmd: string[], options?: SpawnOptions): Subprocess
Bun.spawnSync(cmd: string[], options?: SpawnOptions): SyncSubprocess
```

### SpawnOptions

```typescript
{
  cwd?: string,
  env?: Record<string, string>,
  stdin?: "pipe" | "inherit" | "ignore" | Blob | Response | BunFile | number,
  stdout?: "pipe" | "inherit" | "ignore" | number,
  stderr?: "pipe" | "inherit" | "ignore" | number,
  timeout?: number,              // ms, kill process after timeout
  signal?: AbortSignal,
  onExit?: (proc, exitCode, signalCode, error) => void,
}
```

### Subprocess Properties

```typescript
proc.pid          // process ID
proc.stdin        // writable stream (if stdin: "pipe")
proc.stdout       // readable stream (if stdout: "pipe")
proc.stderr       // readable stream (if stderr: "pipe")
proc.exited       // Promise<number> — resolves with exit code
proc.exitCode     // number | null
proc.kill()       // send SIGTERM
proc.kill(signal) // send specific signal
proc.ref()        // prevent process from exiting while child runs
proc.unref()      // allow process to exit even if child runs
```

### SyncSubprocess (spawnSync)

```typescript
result.stdout     // Buffer
result.stderr     // Buffer
result.exitCode   // number
result.success    // boolean
```

### IPC Between Bun Processes

```typescript
// parent.ts
const child = Bun.spawn(["bun", "child.ts"], {
  ipc(message) {
    console.log("From child:", message);
  },
});
child.send({ task: "process" });

// child.ts
process.on("message", (msg) => {
  process.send({ result: "done" });
});
```

## Bun.serve()

```typescript
const server = Bun.serve({
  port?: number,                    // default: 3000
  hostname?: string,                // default: "0.0.0.0"
  routes?: Record<string, Handler>, // static route map
  fetch: (req: Request, server: Server) => Response | Promise<Response>,
  error?: (error: Error) => Response,
  websocket?: WebSocketHandler,
  tls?: { key, cert },
  idleTimeout?: number,             // seconds, default: 10
});

server.stop();                      // graceful shutdown
server.reload({ fetch });           // hot-reload handler
server.url;                         // URL object for this server
server.port;                        // resolved port number
```

### Route Patterns

```typescript
routes: {
  "/exact": handler,              // exact match
  "/users/:id": handler,          // named parameter (req.params.id)
  "/api/*": handler,              // wildcard
  "/items/:id": {                 // per-method handlers
    GET: getHandler,
    POST: postHandler,
  },
}
```

## bun:sqlite

```typescript
import { Database } from "bun:sqlite";

const db = new Database("file.db");            // file-backed
const db = new Database(":memory:");           // in-memory
const db = new Database("file.db", { readonly: true });
```

### Query Methods

```typescript
db.run(sql, params?)                    // execute, return changes info
db.query(sql).all(params?)              // all rows as array of objects
db.query(sql).get(params?)              // first row or null
db.query(sql).values(params?)           // rows as arrays (no keys)
db.query(sql).run(params?)              // execute prepared statement
```

### Params

```typescript
// Positional
db.run("INSERT INTO t VALUES (?, ?)", [1, "hello"]);

// Named
db.run("INSERT INTO t VALUES ($id, $name)", { $id: 1, $name: "hello" });
```

### Transactions

```typescript
const insert = db.prepare("INSERT INTO t VALUES (?, ?)");
const insertMany = db.transaction((items) => {
  for (const item of items) insert.run(item.id, item.name);
});
insertMany(items); // all-or-nothing
```

## bun:test

```typescript
import {
  test, it,          // aliases
  describe,          // group tests
  expect,            // assertions
  beforeAll, afterAll, beforeEach, afterEach,  // lifecycle
  mock,              // function mocking
  spyOn,             // spy on object methods
  setSystemTime,     // fake timers
} from "bun:test";
```

### Assertions (Jest-compatible)

```typescript
expect(value).toBe(expected)
expect(value).toEqual(expected)        // deep equality
expect(value).toBeNull()
expect(value).toBeDefined()
expect(value).toBeTruthy()
expect(value).toContain(item)
expect(value).toHaveLength(n)
expect(value).toMatch(/regex/)
expect(value).toThrow()
expect(value).toMatchSnapshot()
expect(value).resolves.toBe(expected)  // async
expect(value).rejects.toThrow()        // async
```

### Mocking

```typescript
const fn = mock(() => 42);
fn();
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(1);

// Spy on methods
const obj = { method: () => "real" };
const spy = spyOn(obj, "method").mockReturnValue("mocked");

// Module mocking
mock.module("./math", () => ({
  add: mock(() => 99),
}));
```

### Fake Timers

```typescript
import { setSystemTime } from "bun:test";
setSystemTime(new Date("2025-01-01"));
// Date.now() and new Date() return the fake time
setSystemTime(); // restore real time
```

## Environment and Config

### Environment Variables

Bun loads `.env` files automatically in this order:
1. `.env.local`
2. `.env.development` / `.env.production` (based on `NODE_ENV`)
3. `.env`

Access via `Bun.env.KEY`, `process.env.KEY`, or `import.meta.env.KEY`.

### bunfig.toml

Optional configuration file. Useful settings for script directories:

```toml
[run]
bun = true          # auto-use Bun for all scripts (even those with node shebang)

[install]
exact = true        # pin exact versions (no ^ or ~ ranges)

[test]
root = "./tests"    # custom test directory
```

## CLI Reference

```bash
# Running
bun <file>                     # run a file
bun run <script>               # run package.json script or file
bun --watch run <file>         # restart on file changes
bun --hot run <file>           # HMR without full restart
bun -e "code"                  # eval
bun -p "expr"                  # eval and print

# Package management
bun init -y                    # scaffold project
bun install                    # install dependencies
bun add <pkg>                  # add dependency
bun add -d <pkg>               # add dev dependency
bun remove <pkg>               # remove dependency
bun update                     # update dependencies
bun ci                         # frozen lockfile install (CI)

# Testing
bun test                       # run all tests
bun test --watch               # watch mode
bun test --coverage            # with coverage
bun test --bail                # stop on first failure
bun test --retry 3             # retry flaky tests
bun test --timeout 10000       # per-test timeout (ms)

# Tools
bunx <pkg>                     # run package without installing
bun build <entry> --outdir dist  # bundle for production
```

## Node.js Compatibility

Bun supports most Node.js APIs. Use standard `node:*` imports:

```typescript
import { readFileSync } from "node:fs";      // works, but prefer Bun.file()
import { join } from "node:path";             // works
import { createHash } from "node:crypto";     // works
```

**Prefer Bun-native APIs when available** — they are typically faster and have simpler
ergonomics. Fall back to `node:*` modules when Bun doesn't have a built-in equivalent.
