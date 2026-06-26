# Setup And Safety

Read this file when the runtime cannot find AtomGit tools, the request needs authentication, or the task touches destructive, organization-wide, or enterprise-wide changes.

## When Setup Happens

Connect AtomGit MCP before the first AtomGit task in a given client or runtime. Treat MCP installation and token setup as operator-managed prerequisites, not as actions the skill should perform automatically inside a task.

- If the runtime already exposes AtomGit tools, do not reinstall the server; continue with the business workflow.
- If the runtime does not expose AtomGit tools, pause the business workflow and complete MCP setup first.
- If tools exist but calls fail with auth or scope errors, keep the server and fix the token or permissions.

## Operator-Managed Prerequisites

- [Node.js](https://nodejs.org/) `>= 18`
- AtomGit MCP Server source:
  <https://atomgit.com/zkxw2008/AtomGit-MCP-Server>
- AtomGit MCP Server npm package:
  <https://www.npmjs.com/package/@atomgit.com/atomgit-mcp-server>
- Personal access token:
  `ATOMGIT_TOKEN`

Review the upstream repository or package page before installing the MCP server. This skill assumes the server has already been installed and verified outside the task runtime.

## Minimal Runtime Bring-Up

1. Review the official AtomGit MCP server source or package listing.
2. Install and configure the server manually at the client level.
3. Configure `ATOMGIT_TOKEN` in the MCP client environment.
4. Restart the MCP client if needed so the AtomGit tools appear in the runtime tool list.

## Client Configuration Pattern

Configure AtomGit MCP at the client layer rather than inside each task. Keep `ATOMGIT_ENABLE_DANGEROUS_TOOLS=false` unless the user explicitly requests an operation that needs those tools and confirms the risk.

## Token Setup

Create a token at [AtomGit personal token settings](https://atomgit.com/setting/token-classic).
Store the token in your MCP client configuration or secret store. Do not paste it into chat transcripts, prompts, or repository files.

## Recommended Permission Scope

| Task | Typical permission |
| --- | --- |
| Read public repositories | Basic access |
| Read private repositories | `repo` read |
| Create or update repository content | `repo` write |

For most users, start with the smallest repo-scoped token that supports the immediate task.

Only use elevated scopes for explicit admin workflows:

- `write:org` only when the user explicitly asks to manage organization membership or settings.
- `admin:enterprise` only for explicit enterprise administration, and preferably with a dedicated token.

## Safety Rules

- Never paste the token into chat transcripts or commit it into a repository.
- Prefer discovery calls before mutation calls.
- Confirm destructive, irreversible, or broad-scope changes with the user before executing them.
- Use a dedicated high-privilege token for org or enterprise administration instead of reusing a general token.
- If the server exposes dangerous operations behind `ATOMGIT_ENABLE_DANGEROUS_TOOLS=true`, treat that as an extra gate, not as permission to skip confirmation.
- The runtime-exposed tool set depends on `ATOMGIT_ENABLE_DANGEROUS_TOOLS`; docs may describe more tools than the current session actually exposes.
- If the MCP server is missing, pause the task and ask the operator to install or connect it manually after reviewing the upstream source.

## Common Failure Modes

### Tool not found

- Confirm the AtomGit MCP server is installed and connected to the current runtime.
- Confirm the client was restarted or reloaded after adding the MCP server entry.
- Compare the runtime tool list with the canonical names used in this skill.
- If the runtime wraps MCP tools in a namespace, use the wrapped name shown by the runtime.

### `401 Unauthorized`

- Confirm `ATOMGIT_TOKEN` is set in the environment visible to the runtime.
- Regenerate the token if it expired or was revoked.

### `403 Forbidden`

- The token is valid but does not have enough scope.
- Recreate or replace it with the minimum scope needed for the requested action.

## Cross-Platform Notes

- Keep frontmatter minimal: `name` and `description` only.
- Keep examples transport-agnostic: use canonical method names such as `atomgit_get_repository` in docs, but follow the runtime-exposed tool name at execution time.
- Avoid baking runtime-specific parser hints into the frontmatter or tool examples.
