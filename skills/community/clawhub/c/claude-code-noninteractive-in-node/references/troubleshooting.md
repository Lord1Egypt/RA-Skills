# Remote-Specific Troubleshooting

## Diagnostics

```bash
bash -lc 'whoami && echo "HOME=$HOME" && command -v claude && claude --version'
```

## Common Remote Issues

### exec timeout ≠ process dead
The exec tool may timeout on dispatch, but Claude Code continues running on the Node.
```bash
ps aux | grep claude | grep -v grep
```

### env vars not loaded
Non-interactive shells skip `.bashrc` after the interactive guard.
**Check**: `bash -lc 'echo $ANTHROPIC_API_KEY' | head -c 10`
**Fix**: Move exports above `case $- in` in `.bashrc`

### Node write policy blocks
Some Node security policies deny multi-line commands, heredocs, and inline scripts.
**Fix**: Write script file first, then execute it.

### Cross-filesystem slowness
`/mnt/c/` on WSL is slow for Claude Code.
**Fix**: Use `git worktree` to clone project to native filesystem (`~/` or `/home/`).

### Permission approval required
`SYSTEM_RUN_DENIED: approval required`
**Fix**: The Node operator must approve the command on their end.
