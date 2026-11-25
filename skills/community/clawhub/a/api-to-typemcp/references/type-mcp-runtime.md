# TypeMCP Runtime Contract

Generated projects use the reviewed public npm package on the current 0.3.2 release line:

```json
"@theorvane/type-mcp": "0.3.2"
```

`@theorvane/type-mcp@0.3.2` is published with npm registry `gitHead` and GitHub Release `v0.3.2` both resolving to `e75bcf6a81ef4df57301b6154a0088845020886f`.

## Allowed public API

The generator's default standard ESM path uses standard decorators from the public ESM/NodeNext entrypoint:

```ts
import { McpServer, McpTool } from "@theorvane/type-mcp";
```

Generated TypeScript uses only these public exports:

- `@McpServer`
- `@McpTool`
- `createMcpServer`
- `startStdioServer`
- `zod`
- an explicit `InstanceResolver`

`createMcpServer` and `startStdioServer` are asynchronous and must be awaited. Standard decorators use TC39 semantics: generated `tsconfig.json` must not enable legacy `experimentalDecorators` or `emitDecoratorMetadata`.

`@McpTool` requires an `input` Zod object. Generated code pins Zod v4 (`^4.4.3`) because that is the compatible public runtime contract for `@theorvane/type-mcp@0.3.2`.

## Legacy decorator compatibility

Standard and legacy decorators use distinct entrypoints and distinct decorator semantics. Legacy decorators are an opt-in public entrypoint for external CommonJS/Node16 projects that intentionally use TypeScript's legacy decorator mode; those projects must enable `experimentalDecorators` and import the decorators only from:

```ts
import { McpServer, McpTool } from "@theorvane/type-mcp/legacy";
```

Do not mix this entrypoint with the standard ESM/NodeNext imports. The generator does not copy TypeMCP runtime source and must remain on its default standard ESM path; do not change its templates to legacy decorators or CommonJS.

## Prohibited runtime boundaries

Never generate or publish any of the following:

- copied TypeMCP source code;
- `file:`, `git:`, `link:`, or `portal:` dependencies;
- imports from private, undocumented, or unavailable TypeMCP APIs;
- local TypeMCP checkouts as a generated-project dependency.

Before generated lifecycle scripts run, contained verification inspects dependency metadata and the generated `package-lock.json`, then runs `npm ci --ignore-scripts` in a fresh isolated workspace with inherited npm proxy configuration disabled. It then typechecks, tests, builds, and executes a local stdio smoke test against a mock upstream. Use a host container/VM/sandbox when the dependency graph is untrusted.
