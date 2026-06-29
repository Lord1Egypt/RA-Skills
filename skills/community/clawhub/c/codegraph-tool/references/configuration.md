# CodeGraph Configuration & Reference

## Full CLI Commands

```bash
codegraph install [--yes] [--target=claude,cursor] [--location=global|local] [--no-permissions] [--print-config <id>]
codegraph uninstall [--target=...] [--yes]
codegraph init [path] [-i|--index]
codegraph uninit [path] [--force]
codegraph index [path] [--force] [--quiet]
codegraph sync [path]
codegraph status [path]
codegraph query <search> [--kind class|method|function|...] [--limit 10] [--json]
codegraph files [path] [--format] [--filter] [--max-depth] [--json]
codegraph context <task> [--format] [--max-nodes]
codegraph callers <symbol> [--limit 20] [--json]
codegraph callees <symbol> [--limit 20] [--json]
codegraph impact <symbol> [--depth 2] [--json]
codegraph affected [files...] [--stdin] [-d 5] [-f "e2e/*"] [-j] [-q]
codegraph serve --mcp
codegraph upgrade [--check] [<version>]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEGRAPH_WATCH_DEBOUNCE_MS` | 2000 | Debounce interval (100–60000ms) |
| `CODEGRAPH_NO_DAEMON` | — | 1=disable shared daemon |
| `CODEGRAPH_EXPLORE_LINENUMS` | 1 | 0=disable line numbers |
| `CODEGRAPH_ADAPTIVE_EXPLORE` | 1 | 0=disable adaptive explore |

## Manual Agent Configuration

### Claude Code

`~/.claude.json`:
```json
{ "mcpServers": { "codegraph": { "type": "stdio", "command": "codegraph", "args": ["serve", "--mcp"] } } }
```

`~/.claude/settings.json` (optional auto-allow):
```json
{ "permissions": { "allow": ["mcp__codegraph__codegraph_search","mcp__codegraph__codegraph_explore","mcp__codegraph__codegraph_callers","mcp__codegraph__codegraph_callees","mcp__codegraph__codegraph_impact","mcp__codegraph__codegraph_node","mcp__codegraph__codegraph_status","mcp__codegraph__codegraph_files"] } }
```

### Cursor Note

Cursor launches MCP with incorrect cwd. The installer auto-injects `--path`; manual config requires explicit project path.

## TypeScript API

```typescript
import CodeGraph from '@colbymchenry/codegraph';
const cg = await CodeGraph.init('/path/to/project'); // or .open()
await cg.indexAll({ onProgress: p => console.log(`${p.phase}: ${p.current}/${p.total}`) });
cg.searchNodes('UserService');          // full-text search
cg.getCallers(nodeId); cg.getCallees(nodeId);  // call graph
cg.getImpactRadius(nodeId, 2);          // impact radius
await cg.buildContext('task', { maxNodes:20, includeCode:true, format:'markdown' });
cg.watch(); cg.unwatch(); cg.close();
```

## Supported Languages (21)

| Language | Extensions |
|----------|------------|
| TypeScript | `.ts` `.tsx` |
| JavaScript | `.js` `.jsx` `.mjs` |
| Python | `.py` |
| Go | `.go` |
| Rust | `.rs` |
| Java | `.java` |
| C# | `.cs` |
| PHP | `.php` |
| Ruby | `.rb` |
| C | `.c` `.h` |
| C++ | `.cpp` `.hpp` `.cc` |
| Swift | `.swift` |
| Kotlin | `.kt` `.kts` |
| Scala | `.scala` `.sc` |
| Dart | `.dart` |
| Svelte | `.svelte` |
| Vue | `.vue` |
| Liquid | `.liquid` |
| Pascal/Delphi | `.pas` `.dpr` `.dpk` `.lpr` |
| Lua | `.lua` |
| Luau | `.luau` |

## Framework Routes (14)

Django · Flask · FastAPI · Express · NestJS · Laravel · Drupal · Rails · Spring · Gin/chi/gorilla/mux · Axum/actix/Rocket · ASP.NET · Vapor · React Router/SvelteKit

## Cross-language Bridging

Swift↔ObjC · RN legacy bridge (`RCT_EXPORT_METHOD`) · TurboModules (`Native<X>.ts`) · RN events · Expo Modules · Fabric/Paper views

## affected Command (CI Integration)

```bash
codegraph affected src/utils.ts src/api.ts
git diff --name-only HEAD | codegraph affected --stdin --quiet
codegraph affected src/auth.ts --filter "e2e/*"
```

| Option | Default | Description |
|--------|---------|-------------|
| `--stdin` | false | Read file list from stdin |
| `-d, --depth` | 5 | Dependency traversal depth |
| `-f, --filter` | auto | Test file glob |
| `-j, --json` | false | JSON output |
| `-q, --quiet` | false | Paths only |

CI Example:
```bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
[ -n "$AFFECTED" ] && npx vitest run $AFFECTED
```