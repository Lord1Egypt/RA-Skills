# Permission Mode Details

## Mode Comparison

| Mode | Flag | File Read | File Write | Shell | Git | Network |
|------|------|-----------|------------|-------|-----|---------|
| plan | `--permission-mode plan` | ✅ | ❌ | ❌ | ❌ | ❌ |
| default | (none) | ✅ | ❌ | ❌ | ❌ | ❌ |
| acceptEdits | `--permission-mode acceptEdits` | ✅ | ✅ | ✅ | ✅ | ❌ |
| bypassPermissions | `--permission-mode bypassPermissions` | ✅ | ✅ | ✅ | ✅ | ✅ |
| dangerously-skip | `--dangerously-skip-permissions` | ✅ | ✅ | ✅ | ✅ | ✅ |

## Tool Restriction Examples

### Read-only exploration
```bash
--allowedTools "Read,Glob,Grep,LSP"
```

### Read + diagnostic commands
```bash
--allowedTools "Read,Bash,Glob,Grep,LSP"
```

### Full development
```bash
--allowedTools "Read,Edit,Write,Bash,Glob,Grep,LSP"
```

## When to Use Each Level

### Level 1: Read-only
- Understanding unfamiliar code
- Documentation review
- Architecture analysis
- Preparing planning documents

### Level 2: Analyze
- Running test suites
- Checking build status
- Dependency analysis
- Linting and type checking

### Level 3: Edit
- Feature implementation
- Bug fixes
- Refactoring
- Test writing

### Level 4: Full
- Batch operations across many files
- CI/CD integration
- Project scaffolding
- Trusted codebase maintenance
