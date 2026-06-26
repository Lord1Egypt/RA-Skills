# Troubleshooting

## Common Issues

### Empty results from hover / definition / references

**Cause**: `LSP_WORKSPACE` not set or not pointing to a directory with `.sln`/`.csproj`.

```bash
# Check
echo $LSP_WORKSPACE
ls $LSP_WORKSPACE/*.sln

# Fix
export LSP_WORKSPACE=/path/to/solution/directory
```

### First query is very slow (30–60 seconds)

**Normal behavior.** Roslyn needs to load the entire solution and build the type system on first use. Subsequent queries are ~200ms.

For large solutions (100+ projects), initial load can take up to 60 seconds.

### "csharp-ls: command not found"

**Cause**: `~/.dotnet/tools` not in PATH.

```bash
export PATH="$HOME/.dotnet/tools:$PATH"

# Permanent fix
echo 'export PATH="$HOME/.dotnet/tools:$PATH"' >> ~/.bashrc
```

Or re-run setup:
```bash
bash scripts/setup.sh
```

### Stale daemon (old code still running)

**Cause**: Daemon was started before code changes and is still running the old version.

```bash
# Kill daemon
lsp-query shutdown

# Clean up
rm -f ~/.cache/lsp-query/daemon.sock ~/.cache/lsp-query/daemon.sock.pid

# Next lsp-query call will start fresh daemon
```

### "dotnet tool install fails with DotnetToolSettings.xml"

**Cause**: Some csharp-ls versions have packaging issues.

```bash
# Pin to known-good version
dotnet tool install --global csharp-ls --version 0.20.0
```

### No symbols in Unity project

**Cause**: Unity projects don't commit `.sln`/`.csproj` to version control. These are generated locally by Unity Editor.

**Options**:
1. Open the project in Unity Editor → "Regenerate project files" → commit the generated files
2. Use text search (`rg`) as fallback for Unity code

### Socket connection refused

**Cause**: Daemon died but left socket/pid files behind.

```bash
rm -f ~/.cache/lsp-query/daemon.sock ~/.cache/lsp-query/daemon.sock.pid
lsp-query hover your_file.cs 1 1  # Will start fresh daemon
```

## Debug Mode

Enable detailed logging:

```bash
export LSP_DEBUG=1
lsp-query hover file.cs 10 20

# Check log
cat /tmp/lsp-query-debug.log
```

Log includes:
- All JSON-RPC messages sent/received
- Server-to-client requests and responses
- Timing information

## Health Check

```bash
# Check if daemon is running
lsp-query servers

# Check csharp-ls binary
csharp-ls --version

# Check .NET SDK
dotnet --version

# Full verify
bash scripts/setup.sh --verify
```
