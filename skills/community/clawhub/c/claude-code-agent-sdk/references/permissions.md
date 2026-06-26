# Configuring Permissions

> Control how your agent uses tools with permission modes, hooks, and declarative allow/deny rules.

## Permission Evaluation Flow

When Claude requests a tool, the SDK checks in order:

1. **Hooks** — Can directly deny the call or pass through
2. **Deny rules** — `disallowedTools` and settings.json deny rules (effective even in `bypassPermissions`)
3. **Permission mode** — `bypassPermissions` approves everything, `acceptEdits` approves file operations, etc.
4. **Allow rules** — `allowedTools` and settings.json allow rules
5. **canUseTool callback** — Prompts user for approval at runtime (skipped in `dontAsk` mode, where it's denied)

## Allow and Deny Rules

| Option | Effect |
|:---|:---|
| `allowedTools=["Read", "Grep"]` | Read and Grep auto-approved. Unlisted tools continue through the flow |
| `disallowedTools=["Bash"]` | Bash always denied (highest priority, overrides `bypassPermissions`) |

**Locked-down agent mode:**
```typescript
options: {
  allowedTools: ["Read", "Glob", "Grep"],
  permissionMode: "dontAsk"
}
```

⚠️ `allowedTools` does not constrain `bypassPermissions`. Setting `allowedTools=["Read"]` + `bypassPermissions` still approves every tool. Use `disallowedTools` to block specific tools.

## Permission Modes

| Mode | Description | Tool Behavior |
|:---|:---|:---|
| `default` | Standard permissions | No auto-approval; triggers `canUseTool` callback |
| `dontAsk` | Deny instead of prompt | Anything not pre-approved is denied; `canUseTool` never called |
| `acceptEdits` | Auto-accept file edits | File edits + filesystem operations (mkdir/rm/mv/cp/sed) auto-approved |
| `bypassPermissions` | Bypass all permissions | All tools run without prompting (use cautiously) |
| `plan` | Planning mode | Read-only tools only; Claude analyzes and plans without editing source files |
| `auto` (TS only) | Model classification approval | Model classifier approves/denies each tool call |

⚠️ **Sub-agent inheritance**: When parent agent uses `bypassPermissions`/`acceptEdits`/`auto`, all sub-agents inherit that mode, cannot be overridden.

### Setting Permission Mode

**At query time:**
```typescript
options: { permissionMode: "default" }
```

**Dynamically during streaming:**
```typescript
const q = query({ prompt: "...", options: { permissionMode: "default" } });
await q.setPermissionMode("acceptEdits");
```

### Mode Details

**`acceptEdits`**: Auto-approves file edits (Edit, Write) and filesystem commands (mkdir, touch, rm, rmdir, mv, cp, sed), only within working directory or `additionalDirectories`.

**`dontAsk`**: Turns permission prompts into denials. Tools that are already approved via `allowedTools`, settings.json allow rules, or hooks work normally. Everything else is denied.

**`bypassPermissions`**: Auto-approves all tools. Hooks still execute and can block operations. Use only in controlled environments.

**`plan`**: Claude can only read files and run read-only shell commands, may use `AskUserQuestion` to clarify requirements.

## Related Resources

- [Handling Approvals and User Input](/en/agent-sdk/user-input): Interactive approval prompts
- [Hooks Guide](/en/agent-sdk/hooks): Run custom code at key points
- [Permission Rules](/en/settings#permission-settings): Declarative rules via settings.json